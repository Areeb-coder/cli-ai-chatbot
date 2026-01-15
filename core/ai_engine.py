"""
NovaMind AI Engine Module
=========================
Modular AI integration with support for OpenRouter.
Handles conversation, context, and response generation.
"""

import os
import time
import requests
from typing import Optional, List, Dict, Any
from dataclasses import dataclass


@dataclass
class AIConfig:
    """AI configuration"""
    model: str = "mistralai/mistral-7b-instruct:free"  # Free OpenRouter model
    max_tokens: int = 1024
    temperature: float = 0.8
    mode: str = "friendly"


# OpenRouter API endpoint
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Mode-specific system prompts
MODE_PROMPTS = {
    "friendly": """You are NovaMind, a friendly and helpful AI assistant in a terminal chatbot.
You are warm, casual, and conversational while being informative.
Use emojis occasionally but don't overdo it.
Keep responses concise but engaging.
Adapt your tone based on the user's mood and message style.""",
    
    "creative": """You are NovaMind, a highly creative and imaginative AI assistant.
You think outside the box, use colorful language, and bring artistic flair to conversations.
You love metaphors, wordplay, and unexpected perspectives.
You're playful and inventive while still being helpful.
Use emojis expressively to enhance your creative responses.""",
    
    "serious": """You are NovaMind, a professional and focused AI assistant.
You provide clear, accurate, and well-structured responses.
You stay on topic and prioritize substance over style.
You're respectful and efficient in your communication.
Minimal emoji usage - only when truly appropriate.""",
    
    "sarcastic": """You are NovaMind, a witty AI assistant with a sarcastic edge.
You're helpful but deliver responses with clever humor and occasional sass.
You make playful observations and aren't afraid of gentle teasing.
Balance wit with genuine helpfulness - don't be mean, just clever.
Use emojis to soften the sarcasm when needed.""",
}


class AIEngine:
    """
    AI Engine for NovaMind.
    Handles all AI-related functionality with OpenRouter support.
    """
    
    def __init__(self):
        self.config = AIConfig()
        self.api_keys: List[str] = []
        self.current_key_index = 0
        self.initialized = False
        self.last_error: Optional[str] = None
    
    def initialize(self) -> bool:
        """Initialize the AI engine with API keys"""
        try:
            # Load API keys from environment
            keys = []
            
            # Check for OpenRouter key first
            openrouter_key = os.getenv("OPENROUTER_API_KEY")
            if openrouter_key:
                keys.append(openrouter_key)
            
            # Also check GEMINI_API_KEY (in case user stored OpenRouter key there)
            main_key = os.getenv("GEMINI_API_KEY")
            if main_key and main_key.startswith("sk-or-"):
                # This is actually an OpenRouter key
                if main_key not in keys:
                    keys.append(main_key)
            
            # Load backup OpenRouter keys
            for i in range(1, 5):
                key = os.getenv(f"OPENROUTER_API_KEY{i}")
                if key and key not in keys:
                    keys.append(key)
            
            if not keys:
                self.last_error = "No OpenRouter API key found. Set OPENROUTER_API_KEY in .env file."
                return False
            
            self.api_keys = keys
            self.initialized = True
            return True
            
        except Exception as e:
            self.last_error = str(e)
            return False
    
    def _get_current_api_key(self) -> str:
        """Get the current API key"""
        if self.api_keys:
            return self.api_keys[self.current_key_index]
        return ""
    
    def _switch_to_next_key(self) -> bool:
        """Switch to next available API key"""
        if len(self.api_keys) > 1:
            self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
            return True
        return False
    
    def set_mode(self, mode: str) -> bool:
        """Set the AI personality mode"""
        if mode.lower() in MODE_PROMPTS:
            self.config.mode = mode.lower()
            return True
        return False
    
    def get_available_modes(self) -> List[str]:
        """Get list of available modes"""
        return list(MODE_PROMPTS.keys())
    
    def _make_api_request(self, messages: List[Dict]) -> Dict:
        """Make a request to OpenRouter API"""
        headers = {
            "Authorization": f"Bearer {self._get_current_api_key()}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://novamind-cli.local",  # Required by OpenRouter
            "X-Title": "NovaMind CLI Chatbot"  # Optional but recommended
        }
        
        payload = {
            "model": self.config.model,
            "messages": messages,
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature,
            "frequency_penalty": 1.2,  # Strongly penalize repeated tokens
            "presence_penalty": 1.0,   # Strongly encourage new topics
            "repetition_penalty": 1.2,  # Additional repetition penalty (if model supports it)
            "stop": ["User:", "Human:", "\n\n\n"],  # Stop sequences
        }
        
        response = requests.post(
            OPENROUTER_API_URL,
            headers=headers,
            json=payload,
            timeout=60
        )
        
        return response.json()
    
    def _remove_repetition(self, text: str) -> str:
        """Remove repeated sentences/phrases from response"""
        if not text:
            return text
        
        # First, handle line-by-line repetitions (most common issue)
        lines = text.split('\n')
        unique_lines = []
        seen_lines = set()
        
        for line in lines:
            line_stripped = line.strip()
            # Normalize the line for comparison (lowercase, remove extra spaces)
            line_normalized = ' '.join(line_stripped.lower().split())
            
            if line_normalized and line_normalized not in seen_lines:
                unique_lines.append(line)
                seen_lines.add(line_normalized)
            elif not line_normalized:
                # Keep empty lines for formatting, but limit consecutive empty lines
                if not unique_lines or unique_lines[-1].strip():
                    unique_lines.append(line)
        
        # If after line deduplication we only have one line, also check for 
        # sentence-level repetition within that line
        if len([l for l in unique_lines if l.strip()]) <= 1:
            text = '\n'.join(unique_lines)
            
            # Handle sentence-level repetitions
            sentences = []
            seen_sentences = set()
            current = ""
            
            for char in text:
                current += char
                if char in ".!?":
                    sentence = current.strip()
                    # Normalize for comparison
                    sentence_normalized = ' '.join(sentence.lower().split())
                    if sentence and sentence_normalized not in seen_sentences:
                        sentences.append(sentence)
                        seen_sentences.add(sentence_normalized)
                    current = ""
            
            # Add any remaining text
            if current.strip():
                remaining = current.strip()
                remaining_normalized = ' '.join(remaining.lower().split())
                if remaining_normalized not in seen_sentences:
                    sentences.append(remaining)
            
            if sentences:
                text = " ".join(sentences)
        else:
            # Multiple unique lines - preserve line structure
            text = '\n'.join(unique_lines)
        
        # Final check: if the result still looks repetitive (same phrase repeated),
        # try to extract just the first occurrence
        words = text.split()
        if len(words) > 20:
            # Check if the first third roughly equals the second third
            third = len(words) // 3
            first_third = ' '.join(words[:third]).lower()
            second_third = ' '.join(words[third:third*2]).lower() if len(words) >= third*2 else ''
            third_third = ' '.join(words[third*2:third*3]).lower() if len(words) >= third*3 else ''
            
            # If any two thirds are similar, likely repetitive
            if first_third and second_third:
                # Compare first 80 chars of normalized text
                if len(first_third) > 30 and len(second_third) > 30:
                    if first_third[:80] == second_third[:80]:
                        # Return just the first portion plus any remaining unique content
                        text = ' '.join(words[:third])
                    elif second_third and third_third and second_third[:80] == third_third[:80]:
                        text = ' '.join(words[:third*2])
        
        return text.strip()
    
    def generate_response(
        self, 
        user_message: str, 
        context: List[Dict] = None,
        mood_hint: str = None
    ) -> str:
        """
        Generate AI response to user message.
        
        Args:
            user_message: The user's input message
            context: Previous conversation context
            mood_hint: Detected mood to help tone adjustment
        
        Returns:
            AI response string
        """
        if not self.initialized:
            return "⚠️ AI is not initialized. Please check your API key configuration."
        
        try:
            # Build the system prompt
            system_prompt = MODE_PROMPTS.get(self.config.mode, MODE_PROMPTS["friendly"])
            
            if mood_hint:
                system_prompt += f"\n\nThe user seems to be feeling {mood_hint}. Adjust your tone accordingly."
            
            # Build messages array
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add context/history if provided
            if context:
                for msg in context[:-1]:  # Exclude the current message
                    role = msg.get("role", "user")
                    if role == "model":
                        role = "assistant"
                    content = msg.get("content", msg.get("parts", [{}])[0].get("text", ""))
                    if content:
                        messages.append({"role": role, "content": content})
            
            # Add the current user message
            messages.append({"role": "user", "content": user_message})
            
            # Make API request
            response_data = self._make_api_request(messages)
            
            # Debug: print actual response for troubleshooting
            # print(f"DEBUG Response: {response_data}")
            
            # Check for errors
            if "error" in response_data:
                error_obj = response_data["error"]
                if isinstance(error_obj, dict):
                    error_msg = error_obj.get("message", str(error_obj))
                    error_code = error_obj.get("code", "")
                else:
                    error_msg = str(error_obj)
                    error_code = ""
                
                self.last_error = f"Code: {error_code}, Message: {error_msg}"
                
                # Check for quota/rate limit errors (very specific matching)
                error_lower = error_msg.lower()
                if error_code == 429 or "rate limit" in error_lower or "quota exceeded" in error_lower:
                    if self._switch_to_next_key():
                        return self.generate_response(user_message, context, mood_hint)
                    return "😅 Rate limit reached. Please try again in a moment!"
                
                # Check for invalid/unauthorized key
                if error_code == 401 or "unauthorized" in error_lower or "invalid api key" in error_lower:
                    if self._switch_to_next_key():
                        return self.generate_response(user_message, context, mood_hint)
                    return f"⚠️ API key issue: {error_msg[:150]}"
                
                # Check for model not found
                if "model" in error_lower and ("not found" in error_lower or "invalid" in error_lower):
                    return f"⚠️ Model not available: {error_msg[:150]}"
                
                # Show actual error for debugging
                return f"😓 API Error: {error_msg[:200]}"
            
            # Extract response text
            if "choices" in response_data and len(response_data["choices"]) > 0:
                raw_response = response_data["choices"][0]["message"]["content"].strip()
                # Remove any repetitive content
                return self._remove_repetition(raw_response)
            
            return "😓 No response received from AI."
            
        except requests.exceptions.Timeout:
            return "⏱️ Request timed out. Please try again."
        except requests.exceptions.ConnectionError:
            return "🌐 Connection error. Please check your internet connection."
        except Exception as e:
            self.last_error = str(e)
            return f"😓 Something went wrong: {str(e)[:100]}"
    
    def generate_streaming_response(
        self, 
        user_message: str, 
        context: List[Dict] = None,
        mood_hint: str = None
    ):
        """
        Generate streaming AI response (yields chunks).
        
        Yields:
            Response text chunks
        """
        if not self.initialized:
            yield "⚠️ AI is not initialized."
            return
        
        try:
            system_prompt = MODE_PROMPTS.get(self.config.mode, MODE_PROMPTS["friendly"])
            
            if mood_hint:
                system_prompt += f"\n\nThe user seems to be feeling {mood_hint}."
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
            
            headers = {
                "Authorization": f"Bearer {self._get_current_api_key()}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://novamind-cli.local",
                "X-Title": "NovaMind CLI Chatbot"
            }
            
            payload = {
                "model": self.config.model,
                "messages": messages,
                "max_tokens": self.config.max_tokens,
                "temperature": self.config.temperature,
                "stream": True
            }
            
            response = requests.post(
                OPENROUTER_API_URL,
                headers=headers,
                json=payload,
                timeout=60,
                stream=True
            )
            
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith("data: "):
                        data = line[6:]
                        if data == "[DONE]":
                            break
                        try:
                            import json
                            chunk_data = json.loads(data)
                            if "choices" in chunk_data and len(chunk_data["choices"]) > 0:
                                delta = chunk_data["choices"][0].get("delta", {})
                                if "content" in delta:
                                    yield delta["content"]
                        except:
                            pass
                            
        except Exception as e:
            yield f"😓 Error: {str(e)[:100]}"
    
    def get_quick_response(self, prompt: str) -> str:
        """Get a quick response without context (for games, etc.)"""
        if not self.initialized:
            return "AI not available"
        
        try:
            messages = [{"role": "user", "content": prompt}]
            response_data = self._make_api_request(messages)
            
            if "choices" in response_data and len(response_data["choices"]) > 0:
                return response_data["choices"][0]["message"]["content"].strip()
            return "No response"
        except Exception as e:
            return f"Error: {str(e)[:50]}"
    
    def generate_trivia_question(self) -> Dict[str, str]:
        """Generate a random trivia question"""
        prompt = """Generate a random trivia question with 4 multiple choice options.
Format your response exactly like this:
QUESTION: [Your question here]
A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]
ANSWER: [Correct letter]

Make it fun and interesting! Topics can be science, history, pop culture, geography, etc."""
        
        response = self.get_quick_response(prompt)
        return {"content": response}
    
    def get_status(self) -> Dict[str, Any]:
        """Get AI engine status"""
        return {
            "initialized": self.initialized,
            "mode": self.config.mode,
            "model": self.config.model,
            "keys_available": len(self.api_keys),
            "current_key_index": self.current_key_index,
            "last_error": self.last_error,
            "provider": "OpenRouter"
        }


# Global AI engine instance
ai_engine = AIEngine()


def get_ai_engine() -> AIEngine:
    """Get the global AI engine"""
    return ai_engine
