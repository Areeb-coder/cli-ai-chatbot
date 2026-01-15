import time
from core.sounds import get_sound_simulator

s = get_sound_simulator()
s.set_enabled(True)

print("Simulating AI typing with sound...")
for c in "Hello World":
    print(c, end="", flush=True)
    if c.isalnum():
        s.play_keystroke_sound()
    time.sleep(0.05)

print()
print("Test complete")
