"""
NovaMind Styles Module
======================
Dynamic theme system with multiple visual modes.
Handles colors, gradients, and styling tokens.
"""

from rich.style import Style
from rich.theme import Theme
from dataclasses import dataclass
from typing import Dict, Optional, Tuple
import random


@dataclass
class ThemeColors:
    """Color palette for a theme"""
    name: str
    primary: str          # Main accent color
    secondary: str        # Secondary accent
    user_text: str        # User message color
    ai_text: str          # AI response color
    system_text: str      # System messages
    error_text: str       # Error messages
    border: str           # Box borders
    background: str       # Background hint
    highlight: str        # Highlighted text
    muted: str            # Subtle text
    emoji: str            # Theme emoji
    bg_rgb: Tuple[int, int, int] = (0, 0, 0)  # RGB Background color


# ============================================
# THEME DEFINITIONS - 6 Unique Visual Themes
# ============================================

THEMES: Dict[str, ThemeColors] = {
    "dark": ThemeColors(
        name="Dark Mode",
        primary="white",
        secondary="#b3b3b3",
        user_text="white",
        ai_text="#d9d9d9",
        system_text="#808080",
        error_text="red",
        border="#4d4d4d",
        background="black",
        highlight="white",
        muted="#4d4d4d",
        emoji="🌑",
        bg_rgb=(10, 10, 10)
    ),
    "light": ThemeColors(
        name="Light Mode",
        primary="black",
        secondary="blue",
        user_text="black",
        ai_text="blue",
        system_text="#808080",
        error_text="red",
        border="#b3b3b3",
        background="white",
        highlight="black",
        muted="#999999",
        emoji="☀️",
        bg_rgb=(250, 250, 250)
    ),
    "neon": ThemeColors(
        name="Neon Cyberpunk",
        primary="bright_magenta",
        secondary="bright_cyan",
        user_text="bright_green",
        ai_text="bright_magenta",
        system_text="bright_cyan",
        error_text="bright_red",
        border="magenta",
        background="black",
        highlight="bright_yellow",
        muted="#b3b3b3",
        emoji="🌆",
        bg_rgb=(15, 5, 20)
    ),
    "hacker": ThemeColors(
        name="Hacker Matrix",
        primary="green",
        secondary="bright_green",
        user_text="bright_green",
        ai_text="green",
        system_text="green4",
        error_text="red",
        border="green",
        background="black",
        highlight="bright_white",
        muted="green4",
        emoji="🖥️",
        bg_rgb=(0, 15, 0)
    ),
    "zen": ThemeColors(
        name="Zen Garden",
        primary="cyan",
        secondary="white",
        user_text="bright_cyan",
        ai_text="white",
        system_text="cyan3",
        error_text="yellow",
        border="cyan3",
        background="black",
        highlight="bright_white",
        muted="#b3b3b3",
        emoji="🧘",
        bg_rgb=(20, 25, 30)
    ),
    "retro": ThemeColors(
        name="Retro Amber",
        primary="yellow",
        secondary="bright_yellow",
        user_text="bright_yellow",
        ai_text="yellow",
        system_text="orange3",
        error_text="red",
        border="yellow",
        background="black",
        highlight="bright_white",
        muted="yellow4",
        emoji="📺",
        bg_rgb=(30, 20, 5)
    ),
    "ocean": ThemeColors(
        name="Deep Ocean",
        primary="blue",
        secondary="bright_blue",
        user_text="bright_cyan",
        ai_text="bright_blue",
        system_text="blue3",
        error_text="bright_red",
        border="blue",
        background="black",
        highlight="bright_white",
        muted="cyan3",
        emoji="🌊",
        bg_rgb=(5, 15, 30)
    ),
    "sunset": ThemeColors(
        name="Warm Sunset",
        primary="bright_red",
        secondary="bright_yellow",
        user_text="bright_yellow",
        ai_text="bright_red",
        system_text="yellow",
        error_text="red",
        border="bright_red",
        background="black",
        highlight="bright_white",
        muted="yellow4",
        emoji="🌅",
        bg_rgb=(40, 10, 10)
    ),
    "midnight": ThemeColors(
        name="Midnight Blue",
        primary="blue",
        secondary="bright_blue",
        user_text="white",
        ai_text="bright_blue",
        system_text="#808080",
        error_text="red",
        border="blue",
        background="black",
        highlight="white",
        muted="#4d4d4d",
        emoji="🌙",
        bg_rgb=(5, 5, 25)
    ),
    "calm": ThemeColors(
        name="Calm Slate",
        primary="white",
        secondary="cyan",
        user_text="white",
        ai_text="cyan",
        system_text="#999999",
        error_text="red",
        border="#808080",
        background="black",
        highlight="white",
        muted="#666666",
        emoji="☁️",
        bg_rgb=(40, 45, 50)
    ),
    "warning": ThemeColors(
        name="Red Alert",
        primary="bright_red",
        secondary="red",
        user_text="bright_white",
        ai_text="bright_red",
        system_text="red",
        error_text="bright_yellow",
        border="bright_red",
        background="red",
        highlight="bright_yellow",
        muted="red",
        emoji="⚠️",
        bg_rgb=(50, 0, 0)
    ),
}


class StyleManager:
    """
    Manages the current theme and provides styling utilities.
    Supports dynamic theme switching and mood-reactive colors.
    """
    
    def __init__(self, theme_name: str = "dark"):
        self.current_theme_name = theme_name
        self.theme = THEMES.get(theme_name, THEMES["dark"])
        self._build_rich_theme()
    
    def _build_rich_theme(self):
        """Build Rich library theme from current colors"""
        self.rich_theme = Theme({
            "primary": Style(color=self.theme.primary),
            "secondary": Style(color=self.theme.secondary),
            "user": Style(color=self.theme.user_text, bold=True),
            "ai": Style(color=self.theme.ai_text),
            "system": Style(color=self.theme.system_text, italic=True),
            "error": Style(color=self.theme.error_text, bold=True),
            "border": Style(color=self.theme.border),
            "highlight": Style(color=self.theme.highlight, bold=True),
            "muted": Style(color=self.theme.muted),
            "success": Style(color="bright_green", bold=True),
            "warning": Style(color="bright_yellow"),
            "info": Style(color="bright_cyan"),
        })
    
    def switch_theme(self, theme_name: str) -> bool:
        """Switch to a different theme"""
        if theme_name.lower() in THEMES:
            self.current_theme_name = theme_name.lower()
            self.theme = THEMES[theme_name.lower()]
            self._build_rich_theme()
            return True
        return False
    
    def get_theme_names(self) -> list:
        """Get list of available theme names"""
        return list(THEMES.keys())
    
    def get_random_theme(self) -> str:
        """Get a random theme name"""
        return random.choice(list(THEMES.keys()))
    
    def get_mood_color(self, mood: str) -> str:
        """Get color based on detected mood"""
        mood_colors = {
            "happy": "bright_yellow",
            "excited": "bright_magenta",
            "sad": "blue",
            "angry": "bright_red",
            "calm": "cyan",
            "curious": "bright_cyan",
            "confused": "yellow",
            "neutral": self.theme.ai_text,
        }
        return mood_colors.get(mood.lower(), self.theme.ai_text)
    
    def get_gradient_chars(self) -> list:
        """Get gradient block characters for visual effects"""
        return ["░", "▒", "▓", "█"]
    
    def get_waveform_chars(self) -> list:
        """Get waveform characters for voice visualization"""
        return ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"]
    
    def get_spinner_frames(self, style: str = "dots") -> list:
        """Get spinner animation frames"""
        spinners = {
            "dots": ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],
            "braille": ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"],
            "moon": ["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"],
            "arrows": ["←", "↖", "↑", "↗", "→", "↘", "↓", "↙"],
            "bounce": ["⠁", "⠂", "⠄", "⡀", "⢀", "⠠", "⠐", "⠈"],
            "pulse": ["█", "▓", "▒", "░", "▒", "▓"],
        }
        return spinners.get(style, spinners["dots"])
    
    def get_box_chars(self, style: str = "rounded") -> dict:
        """Get box drawing characters"""
        boxes = {
            "rounded": {
                "tl": "╭", "tr": "╮", "bl": "╰", "br": "╯",
                "h": "─", "v": "│", "cross": "┼"
            },
            "sharp": {
                "tl": "┌", "tr": "┐", "bl": "└", "br": "┘",
                "h": "─", "v": "│", "cross": "┼"
            },
            "double": {
                "tl": "╔", "tr": "╗", "bl": "╚", "br": "╝",
                "h": "═", "v": "║", "cross": "╬"
            },
            "heavy": {
                "tl": "┏", "tr": "┓", "bl": "┗", "br": "┛",
                "h": "━", "v": "┃", "cross": "╋"
            },
        }
        return boxes.get(style, boxes["rounded"])


# Global style manager instance
style_manager = StyleManager()


def get_style_manager() -> StyleManager:
    """Get the global style manager"""
    return style_manager
