
import sys
import os
import time
import threading

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.sound_engine import get_sound_engine

def test_sound_latency():
    engine = get_sound_engine()
    engine.set_enabled(True)
    
    print("Testing sound engine...")
    print(f"Backend: {engine.system}")
    
    start_time = time.time()
    
    # Simulate fast typing
    print("Simulating fast typing (100 chars)...")
    for i in range(100):
        # This loop should complete almost instantly if non-blocking
        engine.queue_keystroke_sound()
        time.sleep(0.01) # 10ms typing speed (very fast)
        
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"Typing simulation took: {duration:.4f}s")
    
    # If 100 * 0.01 = 1.0s, and duration is close to 1.0s, it means sound didn't block.
    # If duration is > 2.0s or more, sound blocked.
    
    if duration < 1.5:
        print("✅ PASS: Sound system is NON-BLOCKING")
    else:
        print("❌ FAIL: Sound system is BLOCKING")
        
    # Give time for queue to drain (or not, if throttled)
    time.sleep(1)
    engine.stop()
    print("Test complete.")

if __name__ == "__main__":
    test_sound_latency()
