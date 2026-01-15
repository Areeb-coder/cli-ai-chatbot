
import sys
import os

# Ensure we can import core modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.ai_engine import AIEngine

class MockResponse:
    def __init__(self, content):
        self.content = content
    
    def json(self):
        return {
            "choices": [
                {
                    "message": {
                        "content": self.content
                    }
                }
            ]
        }

def test_s_token_removal():
    engine = AIEngine()
    
    # Test case 1: <s> at the start (Current bug: might return empty string via split)
    print("\nTest Case 1: <s> at start")
    content_start = "<s>Hello world"
    # We need to test the logic inside generate_response effectively.
    # Since we can't easily mock requests.post in a simple script without extra libs or heavy patching,
    # let's just test the logic directly if we can, BUT the logic is inside generate_response.
    # Alternatively, we can subclass and override _make_api_request.
    
    class TestEngine(AIEngine):
        def _make_api_request(self, messages):
            return {
                "choices": [{"message": {"content": self.next_content}}]
            }
    
    test_engine = TestEngine()
    test_engine.initialized = True # Bypass init check
    
    test_engine.next_content = "<s>Hello world"
    response = test_engine.generate_response("test")
    print(f"Input: '{test_engine.next_content}'")
    print(f"Output: '{response}'")
    
    if response == "Hello world":
        print("PASS: <s> removed correctly.")
    elif response == "":
        print("FAIL: Content deleted (split bug).")
    elif "<s>" in response:
        print("FAIL: <s> not removed.")
    else:
        print(f"FAIL: Unexpected output '{response}'")

    # Test case 2: <s> in middle (unlikely but good to check)
    print("\nTest Case 2: <s> in middle")
    test_engine.next_content = "Hello <s> world"
    response = test_engine.generate_response("test")
    print(f"Input: '{test_engine.next_content}'")
    print(f"Output: '{response}'")

    # Test case 3: [/INST] tag
    print("\nTest Case 3: [/INST] tag")
    test_engine.next_content = "Response[/INST] Garbage"
    response = test_engine.generate_response("test")
    print(f"Input: '{test_engine.next_content}'")
    print(f"Output: '{response}'")

if __name__ == "__main__":
    test_s_token_removal()
