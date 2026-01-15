"""
NovaMind Animator Module
========================
Handles all animation effects: typing, thinking, transitions.
Creates the "alive" feeling of the chatbot.
"""

import time
import random
import sys
import shutil
from typing import Optional, Callable
from rich.console import Console
from rich.live import Live
from rich.text import Text
from rich.panel import Panel

from .styles import get_style_manager
from .sounds import get_sound_simulator


class Animator:
    """
    Animation engine for NovaMind.
    Provides typing effects, spinners, and visual transitions.
    """
    
    def __init__(self, console: Console):
        self.console = console
        self.style_manager = get_style_manager()
        self.typing_speed = 0.03  # Base typing speed (seconds per char)
        self.sound_enabled = True
        self.focus_mode = False
    
    # ============================================
    # TYPING ANIMATION
    # ============================================
    
    def type_text(
        self, 
        text: str, 
        style: str = "ai",
        speed_multiplier: float = 1.0,
        mood: str = "neutral"
    ):
        """
        Display text character by character with typing animation.
        Speed varies based on mood and character type.
        """
        if self.focus_mode:
            # In focus mode, just print without animation
            self.console.print(text, style=style)
            return
        
        # Adjust speed based on mood
        mood_speeds = {
            "excited": 0.5,    # Faster when excited
            "happy": 0.7,
            "calm": 1.2,       # Slower when calm
            "thoughtful": 1.5,
            "sad": 1.3,
            "neutral": 1.0,
        }
        mood_modifier = mood_speeds.get(mood, 1.0)
        
        current_text = ""
        for i, char in enumerate(text):
            current_text += char
            
            # Calculate delay with variation
            base_delay = self.typing_speed * speed_multiplier * mood_modifier
            
            # Punctuation delays
            if char in ".!?":
                delay = base_delay * 3
            elif char in ",;:":
                delay = base_delay * 2
            elif char == " ":
                delay = base_delay * 0.5
            else:
                # Add slight randomness for natural feel
                delay = base_delay * random.uniform(0.8, 1.2)
            
            # Print with carriage return for smooth update
            sys.stdout.write(f"\r{current_text}")
            sys.stdout.flush()
            
            # Sound effect (text-based)
            if self.sound_enabled and char.isalnum():
                self._typing_sound(char)
            
            time.sleep(delay)
        
        print()  # New line after complete
    
    def type_text_rich(
        self, 
        text: str, 
        style: str = "ai",
        speed_multiplier: float = 1.0,
        mood: str = "neutral",
        prefix: str = ""
    ):
        """
        Rich-formatted typing animation using Live display.
        Better for styled text and panels.
        """
        if self.focus_mode:
            self.console.print(f"{prefix}{text}", style=style)
            return
        
        mood_speeds = {
            "excited": 0.5,
            "happy": 0.7,
            "calm": 1.2,
            "thoughtful": 1.5,
            "neutral": 1.0,
        }
        mood_modifier = mood_speeds.get(mood, 1.0)
        
        current_text = ""
        with Live(Text(prefix, style=style), console=self.console, refresh_per_second=60) as live:
            for char in text:
                current_text += char
                
                # Calculate delay
                base_delay = self.typing_speed * speed_multiplier * mood_modifier
                if char in ".!?":
                    delay = base_delay * 3
                elif char in ",;:":
                    delay = base_delay * 2
                elif char == " ":
                    delay = base_delay * 0.5
                else:
                    delay = base_delay * random.uniform(0.8, 1.2)
                
                live.update(Text(f"{prefix}{current_text}", style=style))
                time.sleep(delay)
    
    def _typing_sound(self, char: str):
        """Generate typing sound effect"""
        if self.sound_enabled:
            get_sound_simulator().play_keystroke_sound()
    
    # ============================================
    # THINKING ANIMATION
    # ============================================
    
    def thinking_animation(
        self, 
        message: str = "Thinking",
        duration: Optional[float] = None,
        spinner_style: str = "dots"
    ):
        """
        Display animated thinking indicator.
        Returns a context manager for async thinking display.
        """
        frames = self.style_manager.get_spinner_frames(spinner_style)
        theme = self.style_manager.theme
        
        if duration:
            # Fixed duration thinking
            start_time = time.time()
            frame_idx = 0
            while time.time() - start_time < duration:
                frame = frames[frame_idx % len(frames)]
                styled_text = Text(f"  {frame} {message}...", style=theme.system_text)
                self.console.print(styled_text, end="\r")
                frame_idx += 1
                time.sleep(0.1)
            # Clear the line
            self.console.print(" " * 50, end="\r")
        else:
            # Single frame (for use in loops)
            return ThinkingContext(self.console, message, frames, theme.system_text)
    
    # ============================================
    # VOICE VISUALIZATION
    # ============================================
    
    def voice_waveform(self, intensity: float = 0.5, width: int = 20):
        """
        Generate voice waveform visualization.
        Intensity: 0.0 to 1.0
        """
        wave_chars = self.style_manager.get_waveform_chars()
        waveform = ""
        
        for i in range(width):
            # Create wave pattern with some randomness
            position = i / width
            wave_value = abs(
                intensity * 
                (0.5 + 0.5 * random.random()) * 
                (1 - abs(position - 0.5) * 2)
            )
            char_idx = int(wave_value * (len(wave_chars) - 1))
            char_idx = max(0, min(char_idx, len(wave_chars) - 1))
            waveform += wave_chars[char_idx]
        
        return waveform
    
    def animate_waveform(self, duration: float = 2.0):
        """Animate a talking waveform"""
        theme = self.style_manager.theme
        start_time = time.time()
        
        while time.time() - start_time < duration:
            intensity = 0.3 + 0.7 * random.random()
            wave = self.voice_waveform(intensity, 30)
            styled = Text(f"    {wave}", style=theme.primary)
            self.console.print(styled, end="\r")
            time.sleep(0.1)
        
        self.console.print(" " * 40, end="\r")
    
    # ============================================
    # TRANSITION EFFECTS
    # ============================================
    
    def fade_in_text(self, text: str, style: str = "primary"):
        """Fade in text effect using gradient"""
        gradient = self.style_manager.get_gradient_chars()
        
        for i, grad_char in enumerate(gradient):
            display = grad_char * len(text)
            self.console.print(display, style=style, end="\r")
            time.sleep(0.1)
        
        self.console.print(text, style=style)
    
    def matrix_rain(self, duration: float = 3.0, density: float = 0.3):
        """Matrix-style rain animation (Easter egg)"""
        term_size = shutil.get_terminal_size()
        width = term_size.columns
        height = 15
        
        # Characters for matrix rain
        chars = "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉ0123456789"
        
        # Track dropping characters
        drops = [random.randint(-height, 0) for _ in range(width)]
        
        start_time = time.time()
        while time.time() - start_time < duration:
            lines = []
            for y in range(height):
                line = ""
                for x in range(width):
                    if drops[x] == y:
                        line += random.choice(chars)
                    elif drops[x] > y and drops[x] - y < 5:
                        line += random.choice(chars)
                    else:
                        line += " "
                lines.append(line)
            
            # Move drops down
            for x in range(width):
                if random.random() < density:
                    drops[x] += 1
                    if drops[x] > height:
                        drops[x] = random.randint(-5, 0)
            
            # Print frame
            self.console.print("\n" * height, end="")  # Clear space
            for line in lines:
                self.console.print(Text(line, style="green"), end="\n")
            
            time.sleep(0.1)
            
            # Move cursor up
            sys.stdout.write(f"\033[{height}A")
        
        # Clear the animation area
        for _ in range(height):
            self.console.print(" " * width)
    
    def celebration_animation(self):
        """Celebration animation for achievements/special moments"""
        theme = self.style_manager.theme
        confetti = ["🎉", "🎊", "✨", "🌟", "💫", "🎈", "🎁", "🏆"]
        
        term_size = shutil.get_terminal_size()
        width = min(term_size.columns, 60)
        
        for _ in range(5):
            line = ""
            for _ in range(width // 3):
                if random.random() < 0.3:
                    line += random.choice(confetti) + " "
                else:
                    line += "  "
            self.console.print(line, style=theme.primary)
            time.sleep(0.15)
    
    # ============================================
    # UTILITY METHODS
    # ============================================
    
    def set_focus_mode(self, enabled: bool):
        """Toggle focus mode (minimal animations)"""
        self.focus_mode = enabled
    
    def set_sound(self, enabled: bool):
        """Toggle sound effects"""
        self.sound_enabled = enabled
    
    def set_typing_speed(self, speed: float):
        """Set base typing speed (0.01 to 0.1)"""
        self.typing_speed = max(0.01, min(0.1, speed))
    
    def clear_line(self):
        """Clear current line"""
        term_size = shutil.get_terminal_size()
        self.console.print(" " * term_size.columns, end="\r")


class ThinkingContext:
    """Context manager for thinking animation"""
    
    def __init__(self, console: Console, message: str, frames: list, style: str):
        self.console = console
        self.message = message
        self.frames = frames
        self.style = style
        self.running = False
        self.frame_idx = 0
    
    def __enter__(self):
        self.running = True
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.running = False
        self.console.print(" " * 50, end="\r")
    
    def update(self):
        """Update the thinking animation frame"""
        if self.running:
            frame = self.frames[self.frame_idx % len(self.frames)]
            self.console.print(f"  {frame} {self.message}...", style=self.style, end="\r")
            self.frame_idx += 1


def get_animator(console: Console) -> Animator:
    """Factory function to create animator"""
    return Animator(console)
