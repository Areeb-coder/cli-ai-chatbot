
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from core.logos import get_colored_logo

def verify():
    with open("verification_result.txt", "w", encoding="utf-8") as f:
        f.write("RULER (80 chars):\n")
        f.write("1234567890" * 8 + "\n")
        f.write("-" * 80 + "\n")
        
        f.write("\n>>> HACKER LOGO <<<\n")
        # Strip ansi for checking width roughly, or keep it?
        # get_colored_logo returns ANSI.
        # Let's write the raw logo string from logos key just in case, 
        # but better to test the function.
        # However, `print_logo` does centering logic.
        # I will replicate print_logo logic or just grab the raw text from logos.py
        
        from core.logos import THEME_LOGOS
        f.write(THEME_LOGOS["hacker"])
        
        f.write("\n\n>>> OCEAN LOGO <<<\n")
        f.write(THEME_LOGOS["ocean"])
        
        f.write("\n" + "-" * 80 + "\n")

if __name__ == "__main__":
    verify()
