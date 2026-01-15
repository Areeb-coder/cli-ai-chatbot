"""
NovaMind Sounds Module
======================
Wrapper for the new core.sound_engine.
Maintains backward compatibility while using the new non-blocking architecture.
"""

import random
from .sound_engine import get_sound_engine

# Sound effect patterns (text-based fallback for visual effects)
TYPING_SOUNDS = {
    "mechanical": ["[tick]", "[tack]", "[click]", "[clack]"],
    "soft": [".", "·", "•", "◦"],
    "typewriter": ["⌨", "✎", "✐", "⌨️"],
    "none": [],
}

class SoundSimulator:
    """
    Adapter class for the new SoundEngine.
    Preserves the old API for compatibility.
    """
    
    def __init__(self):
        self.engine = get_sound_engine()
        self._style = "mechanical"
    
    @property
    def enabled(self):
        return self.engine.enabled
    
    @enabled.setter
    def enabled(self, value):
        self.engine.set_enabled(value)
    
    def set_enabled(self, enabled: bool):
        """Enable or disable sound effects"""
        self.engine.set_enabled(enabled)
    
    def set_style(self, style: str):
        """Set sound effect style"""
        if style.lower() in TYPING_SOUNDS:
            self._style = style.lower()
            self.engine.style = style.lower()
    
    def play_keystroke_sound(self):
        """Queue a keystroke sound (non-blocking)"""
        self.engine.queue_keystroke_sound()
    
    def play_notification_sound(self):
        """Queue a notification sound"""
        self.engine.queue_notification()
    
    def get_keystroke_sound(self) -> str:
        """Get a random keystroke visual representation"""
        if not self.enabled:
            return ""
        sounds = TYPING_SOUNDS.get(self._style, [])
        return random.choice(sounds) if sounds else ""
    
    def get_enter_sound(self) -> str:
        """Get enter key sound visual"""
        if not self.enabled:
            return ""
        return "[ding!]" if self._style == "mechanical" else "⏎"
    
    def get_bell_sound(self) -> str:
        """Get bell/notification visual"""
        return "🔔" if self.enabled else ""


# Global sound simulator adapter
sound_simulator = SoundSimulator()


def get_sound_simulator() -> SoundSimulator:
    """Get the global sound simulator"""
    return sound_simulator
