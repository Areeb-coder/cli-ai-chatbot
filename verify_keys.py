
import os
from dotenv import load_dotenv
from core.ai_engine import AIEngine

load_dotenv()

print("Testing AI Engine Key Loading...")
ai = AIEngine()
success = ai.initialize()

if success:
    status = ai.get_status()
    print(f"Success: {success}")
    print(f"Keys available: {status['keys_available']}")
    if status['keys_available'] >= 2:
        print("VERIFICATION PASSED: Multiple keys loaded.")
    else:
        print("VERIFICATION FAILED: Only 1 key loaded.")
else:
    print(f"Initialization failed: {ai.last_error}")
