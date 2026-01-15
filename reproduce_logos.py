import sys
import os

# Ensure we can import core
sys.path.append(os.getcwd())

from core.logos import THEME_LOGOS, get_colored_logo

def check_logos():
    print("CHECKING ALL LOGOS IN core/logos.py")
    print("="*60)
    
    for theme, logo in THEME_LOGOS.items():
        print(f"\n[{theme.upper()} LOGO]")
        print("-" * 40)
        
        # Print raw logo to see shape
        for line in logo.split('\n'):
            if not line: continue
            # Strip ANSI just in case, though raw string shouldn't have them in dictionary (usually)
            # Actually core.logos definitions don't have ANSI in the dict keys, they are added by get_colored_logo
            # But the 'warning' logo might rely on specific spacing.
            
            # Check width
            width = len(line)
            status = "OK" if width <= 80 else f"TOO WIDE ({width})"
            print(f"{line}  <-- {status}")
            
        print("-" * 40)

if __name__ == "__main__":
    check_logos()
