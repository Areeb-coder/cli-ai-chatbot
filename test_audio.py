import winsound
import time

print("Testing 440Hz beep for 500ms...")
try:
    winsound.Beep(440, 500)
    print("Beep successful.")
except Exception as e:
    print(f"Beep failed: {e}")

print("Testing MessageBeep...")
try:
    winsound.MessageBeep()
    print("MessageBeep successful.")
except Exception as e:
    print(f"MessageBeep failed: {e}")
