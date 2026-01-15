
import os
import unittest
from unittest.mock import MagicMock, patch
from core.ai_engine import AIEngine, get_ai_engine

class TestRateLimitLoop(unittest.TestCase):
    def setUp(self):
        self.ai = AIEngine()
        # Manually inject keys for testing
        self.ai.api_keys = ["key1", "key2"]
        self.ai.initialized = True
        
    def test_infinite_loop_prevention(self):
        print("Testing infinite loop prevention...")
        
        # Mock _make_api_request to always return 429
        mock_response = {
            "error": {
                "message": "Rate limit exceeded",
                "code": 429
            }
        }
        
        with patch.object(self.ai, '_make_api_request', return_value=mock_response):
            # This should NOT hang or crash
            response = self.ai.generate_response("Hello")
            
            print(f"Response: {response}")
            self.assertIn("All API keys are currently overloaded", response)
            self.assertLessEqual(self.ai.current_key_index, 1) # Should handle indices correctly
            
if __name__ == "__main__":
    unittest.main()
