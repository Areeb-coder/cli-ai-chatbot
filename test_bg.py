import os
import sys
import time
from rich.console import Console

if sys.platform == 'win32':
    os.system('')

console = Console()
console.print("Testing background colors...")

print("Attempting to prevent auto-close...")
# Method 1: ANSI Escape Codes (Standard)
# Set background to Blue (44)
print("\033[44m")
print("This should represent blue background text (ANSI).")
print("Does it fill the screen? Probably not, just text background.")
print("\033[0m") # Reset

# Method 2: OS System Color (Windows only)
# 1 = Blue, 7 = White
print("Changing system color to 17 (Blue background, White text) in 2 seconds...")
time.sleep(2)
os.system('color 17')
print("System color changed? This should fill screen.")

time.sleep(2)
print("Changing back to 07 (Black background, White text)...")
os.system('color 07')

# Method 3: Rich Console Style
print("Testing Rich Console style...")
console_blue = Console(style="white on blue")
console_blue.clear() # Maybe this fills?
console_blue.print("This is printed with 'white on blue' style.")
console_blue.print("Does clear() fill the background?")
