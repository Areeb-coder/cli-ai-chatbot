
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.logos import get_all_theme_names, print_logo, get_compact_logo

def test_logos():
    themes = get_all_theme_names()
    print(f"Testing {len(themes)} themes...\n")
    
    for theme in themes:
        print(f"\n{'='*50}")
        print(f"THEME: {theme.upper()}")
        print(f"{'='*50}\n")
        
        try:
            print_logo(theme)
            print("\nCompact Version:")
            print(get_compact_logo(theme))
        except Exception as e:
            print(f"ERROR displaying {theme}: {e}")
            
    print("\nDone.")

if __name__ == "__main__":
    test_logos()
