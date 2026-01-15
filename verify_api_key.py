
import os
import requests
from dotenv import load_dotenv

# Load env vars
load_dotenv()

def test_key():
    key = os.getenv("OPENROUTER_API_KEY")
    if not key:
        print("❌ No OPENROUTER_API_KEY found in .env")
        return

    print(f"Found key: {key[:10]}...{key[-5:]}")
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://test.local", 
        "X-Title": "Test Script"
    }
    
    payload = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": [{"role": "user", "content": "Hello! Are you working?"}],
    }
    
    try:
        print("Sending request...")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("API Key is valid!")
            print(f"Response: {response.json()}")
        else:
            print(f"API Request failed: {response.text}")
            
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_key()
