import sys
import os
from rich.style import Style as RichStyle

# Add current dir to path
sys.path.insert(0, os.getcwd())

from core.styles import THEMES, ThemeColors

def test_themes():
    # Only test light
    name = "light"
    theme = THEMES[name]
    print(f"Testing theme: {name}")
    fields = [
        ("primary", theme.primary),
        ("secondary", theme.secondary),
        ("user_text", theme.user_text),
        ("ai_text", theme.ai_text),
        ("system_text", theme.system_text),
        ("error_text", theme.error_text),
        ("border", theme.border),
        ("highlight", theme.highlight),
        ("muted", theme.muted),
    ]
    
    for field, color in fields:
        print(f"  Checking {field}: repr={repr(color)}")
        try:
            s = RichStyle(color=color)
            print(f"    -> OK")
        except Exception as e:
            print(f"    -> ERROR: {e}")

if __name__ == "__main__":
    test_themes()
