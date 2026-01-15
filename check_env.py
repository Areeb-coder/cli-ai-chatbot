
import os
from dotenv import load_dotenv

load_dotenv()

print("Checking Environment Variables...")
keys = []
for k, v in os.environ.items():
    if k.startswith("OPENROUTER") or k.startswith("GEMINI"):
        print(f"{k}: {v[:10]}... (len={len(v)})")
        keys.append(k)

if not keys:
    print("No relevant keys found.")
