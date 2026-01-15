"""
Quick test script to debug OpenRouter API connection
Run this to see what the actual API response/error is
"""
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("GEMINI_API_KEY")
print(f"API Key found: {'Yes' if api_key else 'No'}")
if api_key:
    print(f"Key starts with: {api_key[:20]}...")

# OpenRouter API endpoint
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Test request
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://novamind-cli.local",
    "X-Title": "NovaMind CLI Chatbot"
}

# Try with a simple model first
test_models = [
    "google/gemini-2.0-flash-exp:free",
    "google/gemma-2-9b-it:free", 
    "meta-llama/llama-3.2-3b-instruct:free",
    "mistralai/mistral-7b-instruct:free",
]

for model in test_models:
    print(f"\n{'='*50}")
    print(f"Testing model: {model}")
    print('='*50)
    
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": "Hello! Just say 'Hi' back in one word."}
        ],
        "max_tokens": 50,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(
            OPENROUTER_API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        
        data = response.json()
        
        if "error" in data:
            print(f"ERROR: {data['error']}")
        elif "choices" in data and len(data["choices"]) > 0:
            print(f"SUCCESS! Response: {data['choices'][0]['message']['content']}")
            print(f"\n✅ Working model found: {model}")
            print("Update AIConfig.model in ai_engine.py to use this model")
            break
        else:
            print(f"Unexpected response: {data}")
            
    except Exception as e:
        print(f"Exception: {e}")

print("\n" + "="*50)
print("Test complete!")
