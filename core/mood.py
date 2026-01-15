"""
NovaMind Mood Detection Module
==============================
Analyzes user input to detect emotional tone.
Adapts UI and AI responses based on detected mood.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
import re
import random


@dataclass
class MoodState:
    """Represents current mood state"""
    name: str
    emoji: str
    intensity: float  # 0.0 to 1.0
    color_hint: str
    speed_modifier: float  # Typing speed modifier


# ============================================
# MOOD DEFINITIONS
# ============================================

MOODS: Dict[str, MoodState] = {
    "happy": MoodState("happy", "😊", 0.7, "bright_yellow", 0.8),
    "excited": MoodState("excited", "🎉", 0.9, "bright_magenta", 0.5),
    "sad": MoodState("sad", "😢", 0.6, "blue", 1.3),
    "angry": MoodState("angry", "😠", 0.8, "bright_red", 0.6),
    "calm": MoodState("calm", "😌", 0.5, "cyan", 1.2),
    "curious": MoodState("curious", "🤔", 0.6, "bright_cyan", 1.0),
    "confused": MoodState("confused", "😕", 0.5, "yellow", 1.1),
    "grateful": MoodState("grateful", "🙏", 0.7, "bright_green", 0.9),
    "playful": MoodState("playful", "😄", 0.8, "bright_magenta", 0.7),
    "neutral": MoodState("neutral", "🙂", 0.3, "white", 1.0),
}


# Keyword patterns for mood detection
MOOD_PATTERNS: Dict[str, List[str]] = {
    "happy": [
        r"\bhappy\b", r"\bglad\b", r"\bjoy\b", r"\byay\b", r"\bawesome\b",
        r"\bgreat\b", r"\bwonderful\b", r"\bamazing\b", r"\blove\b", r"\bfantastic\b",
        r":D", r":\)", r"😊", r"😄", r"🎉", r"\bhaha\b", r"\blol\b"
    ],
    "excited": [
        r"\bexcited\b", r"\bwow\b", r"\bomg\b", r"\bamazing\b", r"\bincredible\b",
        r"!!+", r"\bcan't wait\b", r"\bso cool\b", r"🔥", r"🚀", r"⚡"
    ],
    "sad": [
        r"\bsad\b", r"\bunhappy\b", r"\bdepressed\b", r"\bdown\b", r"\bmiserable\b",
        r"\bcrying\b", r"\btears\b", r"\bhurt\b", r":\(", r"😢", r"😭", r"\bsigh\b"
    ],
    "angry": [
        r"\bangry\b", r"\bfurious\b", r"\bmad\b", r"\bannoyed\b", r"\bfrustrated\b",
        r"\bhate\b", r"\bterrible\b", r"\bawful\b", r"😠", r"😡", r"\bugh\b"
    ],
    "calm": [
        r"\bcalm\b", r"\bpeaceful\b", r"\brelaxed\b", r"\bserene\b", r"\bchill\b",
        r"\bzen\b", r"\btranquil\b", r"😌", r"🧘", r"\bnice\b"
    ],
    "curious": [
        r"\bwhy\b", r"\bhow\b", r"\bwhat\b", r"\bwhen\b", r"\bwhere\b",
        r"\binteresting\b", r"\bcurious\b", r"\bwonder\b", r"🤔", r"\?{2,}",
        r"\btell me\b", r"\bexplain\b"
    ],
    "confused": [
        r"\bconfused\b", r"\bdon't understand\b", r"\bwhat\?\b", r"\bhuh\b",
        r"\bwait\b", r"\bi don't get\b", r"😕", r"🤷", r"\?\?+"
    ],
    "grateful": [
        r"\bthank\b", r"\bthanks\b", r"\bgrateful\b", r"\bappreciate\b",
        r"\bhelpful\b", r"🙏", r"❤️", r"\bawesome\b"
    ],
    "playful": [
        r"\bhehe\b", r"\blol\b", r"\bjk\b", r"\bjust kidding\b", r"\bfunny\b",
        r"\bhaha\b", r"😄", r"😜", r"🤣", r"\bsilly\b", r"\bwanna play\b"
    ],
}


class MoodDetector:
    """
    Detects and tracks user mood across conversation.
    Provides mood-reactive suggestions for UI adaptation.
    """
    
    def __init__(self):
        self.current_mood = MOODS["neutral"]
        self.mood_history: List[Tuple[str, float]] = []  # (mood_name, timestamp)
        self.message_count = 0
    
    def analyze(self, text: str) -> MoodState:
        """
        Analyze text and return detected mood.
        Uses pattern matching and contextual analysis.
        """
        text_lower = text.lower()
        mood_scores: Dict[str, float] = {mood: 0.0 for mood in MOODS}
        
        # Check patterns for each mood
        for mood_name, patterns in MOOD_PATTERNS.items():
            for pattern in patterns:
                matches = re.findall(pattern, text_lower, re.IGNORECASE)
                mood_scores[mood_name] += len(matches) * 0.3
        
        # Analyze punctuation for intensity
        exclamation_count = text.count("!")
        question_count = text.count("?")
        caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
        
        # High caps might indicate excitement or anger
        if caps_ratio > 0.5 and len(text) > 5:
            mood_scores["excited"] += 0.2
            mood_scores["angry"] += 0.1
        
        # Multiple exclamations suggest excitement
        if exclamation_count > 2:
            mood_scores["excited"] += 0.3
        
        # Multiple questions suggest curiosity
        if question_count > 1:
            mood_scores["curious"] += 0.3
        
        # Check for emojis
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # Emoticons
            "\U0001F300-\U0001F5FF"  # Symbols & pictographs
            "\U0001F680-\U0001F6FF"  # Transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # Flags
            "\U00002702-\U000027B0"  # Dingbats
            "\U000024C2-\U0001F251" 
            "]+",
            flags=re.UNICODE
        )
        emojis = emoji_pattern.findall(text)
        if emojis:
            mood_scores["playful"] += 0.1 * len(emojis)
        
        # Find highest scoring mood
        best_mood = max(mood_scores.keys(), key=lambda m: mood_scores[m])
        
        # If no strong signal, stay neutral
        if mood_scores[best_mood] < 0.2:
            best_mood = "neutral"
        
        self.current_mood = MOODS[best_mood]
        self.message_count += 1
        
        return self.current_mood
    
    def get_current_mood(self) -> MoodState:
        """Get the current detected mood"""
        return self.current_mood
    
    def get_mood_emoji(self) -> str:
        """Get emoji for current mood"""
        return self.current_mood.emoji
    
    def get_typing_speed_modifier(self) -> float:
        """Get typing speed modifier based on mood"""
        return self.current_mood.speed_modifier
    
    def get_contextual_emoji(self, context: str = "") -> str:
        """Get a contextually appropriate emoji"""
        # Context-aware emoji selection
        context_emojis = {
            "greeting": ["👋", "🙌", "✨", "🌟"],
            "farewell": ["👋", "🌙", "✨", "💫"],
            "question": ["🤔", "💭", "❓", "🔍"],
            "answer": ["💡", "✨", "📝", "🎯"],
            "thanks": ["🙏", "❤️", "✨", "💖"],
            "error": ["😅", "🔧", "💭", "🤷"],
            "success": ["✅", "🎉", "🌟", "💪"],
            "thinking": ["🤔", "💭", "🧠", "⏳"],
        }
        
        if context in context_emojis:
            return random.choice(context_emojis[context])
        
        # Fall back to mood emoji
        return self.current_mood.emoji
    
    def get_mood_journey(self) -> str:
        """Get visual representation of mood journey"""
        if not self.mood_history:
            return self.current_mood.emoji
        
        journey = " → ".join([
            MOODS.get(m[0], MOODS["neutral"]).emoji 
            for m in self.mood_history[-5:]
        ])
        return journey + f" → {self.current_mood.emoji}"
    
    def record_mood(self, timestamp: float):
        """Record current mood to history"""
        self.mood_history.append((self.current_mood.name, timestamp))
        # Keep only last 20 entries
        if len(self.mood_history) > 20:
            self.mood_history = self.mood_history[-20:]
    
    def get_dominant_mood(self) -> str:
        """Get the most frequent mood in history"""
        if not self.mood_history:
            return "neutral"
        
        mood_counts: Dict[str, int] = {}
        for mood_name, _ in self.mood_history:
            mood_counts[mood_name] = mood_counts.get(mood_name, 0) + 1
        
        return max(mood_counts.keys(), key=lambda m: mood_counts[m])
    
    def suggest_response_tone(self) -> str:
        """Suggest AI response tone based on detected mood"""
        tone_suggestions = {
            "happy": "cheerful and enthusiastic",
            "excited": "energetic and excited",
            "sad": "empathetic and supportive",
            "angry": "calm and understanding",
            "calm": "relaxed and thoughtful",
            "curious": "informative and engaging",
            "confused": "clear and patient",
            "grateful": "warm and appreciative",
            "playful": "fun and witty",
            "neutral": "friendly and helpful",
        }
        return tone_suggestions.get(self.current_mood.name, "friendly and helpful")


# Global mood detector instance
mood_detector = MoodDetector()


def get_mood_detector() -> MoodDetector:
    """Get the global mood detector"""
    return mood_detector
