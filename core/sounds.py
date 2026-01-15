"""
NovaMind Sounds Module
======================
Text-based sound simulation for typing effects.
"""

import random
from typing import Optional


# Sound effect patterns (text-based simulation)
TYPING_SOUNDS = {
    "mechanical": ["[tick]", "[tack]", "[click]", "[clack]"],
    "soft": [".", "·", "•", "◦"],
    "typewriter": ["⌨", "✎", "✐", "⌨️"],
    "none": [],
}


class SoundSimulator:
    """
    Simulates typing sounds using text characters.
    Provides visual feedback for typing animations.
    """
    
    def __init__(self):
        self.enabled = False
        self.style = "mechanical"
    
    def set_enabled(self, enabled: bool):
        """Enable or disable sound effects"""
        self.enabled = enabled
    
    def set_style(self, style: str):
        """Set sound effect style"""
        if style.lower() in TYPING_SOUNDS:
            self.style = style.lower()
    
    def get_keystroke_sound(self) -> str:
        """Get a random keystroke sound"""
        if not self.enabled:
            return ""
        
        sounds = TYPING_SOUNDS.get(self.style, [])
        if sounds:
            return random.choice(sounds)
        return ""
    
    def get_enter_sound(self) -> str:
        """Get enter key sound"""
        if not self.enabled:
            return ""
        
        return "[ding!]" if self.style == "mechanical" else "⏎"
    
    def get_bell_sound(self) -> str:
        """Get bell/notification sound"""
        return "🔔" if self.enabled else ""


# Global sound simulator
sound_simulator = SoundSimulator()


def get_sound_simulator() -> SoundSimulator:
    """Get the global sound simulator"""
    return sound_simulator
