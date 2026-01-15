import sys
import os

# Add current dir to path
sys.path.insert(0, os.getcwd())

try:
    from core.styles import get_style_manager, THEMES
    from core.theme_engine import get_theme_engine
    
    sm = get_style_manager()
    te = get_theme_engine()
    
    print("Imports successful!")
    print(f"Themes available: {list(THEMES.keys())}")
    print(f"Current theme: {sm.current_theme_name}")
    print(f"Theme BG RGB: {sm.theme.bg_rgb}")
    
    # Check if we can switch
    sm.switch_theme("light")
    print(f"Switched to light. BG RGB: {sm.theme.bg_rgb}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
