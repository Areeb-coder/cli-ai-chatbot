
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console
from core.styles import get_style_manager
from core.ui import UI
import time

def verify_themes():
    sm = get_style_manager()
    themes = sm.get_theme_names()
    
    print(f"Found themes: {themes}")
    
    for theme_name in themes:
        print(f"\n--- Testing Theme: {theme_name} ---")
        sm.switch_theme(theme_name)
        console = Console(theme=sm.rich_theme)
        ui = UI(console)
        
        ui.show_user_message("This is a user message with the new style!", "Tester")
        ui.show_ai_message("And this is how I respond in this theme.", "🤖")
        
        time.sleep(0.5)

if __name__ == "__main__":
    verify_themes()
