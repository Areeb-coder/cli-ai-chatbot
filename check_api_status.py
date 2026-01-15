
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# OpenRouter Endpoint
API_URL = "https://openrouter.ai/api/v1/chat/completions"

def check_key(name, key):
    if not key:
        return
        
    print(f"Testing {name}...")
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://novamind-cli.local",
    }
    
    payload = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": [{"role": "user", "content": "Hi"}],
        "max_tokens": 10
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
             print(f"  [OK] {name}: Active & Working")
        elif response.status_code == 429 or response.status_code == 402:
             print(f"  [LIMIT] {name}: Rate Limited (Quota Exceeded)")
        elif response.status_code == 401:
             print(f"  [INVALID] {name}: Invalid Key")
        else:
             print(f"  [ERROR] {name}: Error {response.status_code} - {response.text[:100]}")
             
    except Exception as e:
        print(f"  [NET-ERR] {name}: Connection Error: {e}")

# Find keys
keys_found = False
for k, v in os.environ.items():
    if (k.startswith("OPENROUTER") or k.startswith("GEMINI")) and v.startswith("sk-"):
        check_key(k, v)
        keys_found = True

if not keys_found:
    print("No valid API keys found in environment.")
