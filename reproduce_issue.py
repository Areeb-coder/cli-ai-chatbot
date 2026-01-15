
import sys
import os

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

from core.ai_engine import AIEngine

def test_repetition():
    engine = AIEngine()
    
    # Text from the screenshot (approximate) - repeating multiple times
    single_block = "Did you know that a day on Venus is longer than a year on Venus? 🌍🪐 A single rotation takes about 243 Earth days, while its orbit around the Sun takes only about 225 Earth days "
    
    # Construct a repeated string usually found in these issues (e.g. 3-4 times)
    repeated_text = single_block * 4
    
    print("--- Original Text Length ---")
    print(len(repeated_text))
    
    print("\n--- Processed ---")
    processed = engine._remove_repetition(repeated_text)
    print(processed)
    
    print("\n--- Analysis ---")
    if len(processed) < len(single_block) * 1.5:
        print("SUCCESS: Repetition removed.")
    else:
        print("FAILURE: Repetition still present.")
        print(f"Processed length: {len(processed)}")
        print(f"Single block length: {len(single_block)}")

if __name__ == "__main__":
    test_repetition()
