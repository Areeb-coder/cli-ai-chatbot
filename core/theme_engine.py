"""
NovaMind Theme Engine - FULL SCREEN BACKGROUND FIX
====================================================
LAYER 1: VISUAL-ONLY THEME MANAGEMENT

This module implements TRUE FULL-SCREEN terminal background painting,
similar to professional TUI applications like htop, neovim, and midnight commander.

KEY FIX: The background color MUST fill the ENTIRE visible terminal viewport,
not just printed areas. This is achieved by:
1. Detecting terminal dimensions (rows × columns)
2. Filling EVERY cell with a background-colored space
3. Moving cursor back to home position
4. Persisting background state for all subsequent output

CRITICAL: ANSI background codes (\033[48;2;R;G;Bm) only affect PRINTED text.
Unprinted terminal cells remain at default background. Therefore, we MUST
paint every cell with a space character to achieve full coverage.

Windows-specific: We explicitly enable ANSI escape sequences using
ctypes to call SetConsoleMode, as Windows consoles don't enable
ANSI by default.
"""

import sys
import os
import shutil
from typing import Tuple, Optional


def _enable_windows_ansi():
    """
    WINDOWS-SPECIFIC: Explicitly enable ANSI escape code processing.
    
    Windows consoles do NOT process ANSI codes by default.
    We must call SetConsoleMode with ENABLE_VIRTUAL_TERMINAL_PROCESSING.
    
    This function uses ctypes to make the necessary Win32 API calls.
    colorama.init() just wraps stdout - this actually enables native ANSI.
    """
    if os.name != 'nt':
        return True  # Not Windows, ANSI typically works
    
    try:
        import ctypes
        
        # Get handle to stdout
        # STD_OUTPUT_HANDLE = -11
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)
        
        # Get current console mode
        mode = ctypes.c_ulong()
        kernel32.GetConsoleMode(handle, ctypes.byref(mode))
        
        # ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
        # This flag enables ANSI escape sequence processing
        ENABLE_VT = 0x0004
        kernel32.SetConsoleMode(handle, mode.value | ENABLE_VT)
        
        return True
    except Exception:
        return False


class ThemeEngine:
    """
    Global theme engine singleton.
    Manages terminal background colors with TRUE FULL-SCREEN coverage.
    
    KEY DESIGN PRINCIPLES:
    1. Theme state is GLOBAL and PERSISTED
    2. Background MUST fill the ENTIRE terminal viewport
    3. All screen clears MUST re-paint the full background
    4. Windows ANSI must be explicitly enabled
    
    CRITICAL DIFFERENCE FROM NORMAL ANSI:
    Simply setting \033[48;2;R;G;Bm only colors PRINTED text.
    For full-screen coverage, we must PRINT A SPACE IN EVERY CELL.
    """
    
    # Class-level singleton instance
    _instance = None
    
    def __new__(cls):
        """Ensure only one ThemeEngine instance exists (singleton pattern)"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        # Only initialize once (singleton protection)
        if self._initialized:
            return
            
        # ============================================
        # WINDOWS-SPECIFIC: Enable ANSI escape codes
        # This MUST happen before any ANSI output
        # ============================================
        _enable_windows_ansi()
            
        # ============================================
        # PERSISTENT STATE - survives all operations
        # ============================================
        self.current_bg: Optional[Tuple[int, int, int]] = None  # RGB background
        self.supports_color: bool = self._check_color_support()
        self._initialized = True
        
    def _check_color_support(self) -> bool:
        """
        Check if terminal supports ANSI color codes.
        
        Modern terminals (Windows Terminal, VS Code, most Linux terminals)
        support 24-bit TrueColor via the ANSI 48;2;R;G;B sequence.
        """
        # Check for terminal environment
        if not sys.stdout.isatty():
            return False
        
        # Most modern terminals support ANSI - return True by default
        # Windows Terminal sets WT_SESSION env var
        # COLORTERM=truecolor indicates 24-bit support
        return True
    
    def get_current_bg(self) -> Optional[Tuple[int, int, int]]:
        """
        Get the current background RGB.
        Used by other modules to check active theme.
        
        Returns:
            Tuple of (R, G, B) or None if no theme applied
        """
        return self.current_bg
    
    def paint_full_terminal_background(self, theme=None):
        """
        MANDATORY FIX STRATEGY:
        1. Clear scrollback (ESC[3J)
        2. Clear screen (ESC[2J)
        3. Move cursor home (ESC[H)
        4. Paint ENTIRE viewport
        5. Reset cursor
        
        This makes the application behave like a real TUI (htop, neovim).
        
        Args:
            theme: Optional theme object with .bg_rgb attribute. 
                   If None, uses self.current_bg.
        """
        if not self.supports_color:
            return

        # Determine RGB
        r, g, b = None, None, None
        if theme and hasattr(theme, 'bg_rgb'):
             r, g, b = theme.bg_rgb
        elif self.current_bg:
             r, g, b = self.current_bg
        
        if r is None:
            return  # No color to paint

        # Save to state if it's new
        self.current_bg = (r, g, b)
        
        # Build ANSI Background Code
        bg_code = f"\033[48;2;{r};{g};{b}m"
        
        # Get dimensions
        try:
            term_size = shutil.get_terminal_size()
            width = term_size.columns
            height = term_size.lines
        except Exception:
            width = 120
            height = 30
            
        # ============================================
        # MANDATORY STEP 1: FULL BUFFER RESET
        # 1. Clear scrollback (ESC[3J)
        # 2. Clear screen (ESC[2J)
        # 3. Move cursor home (ESC[H)
        # ============================================
        sys.stdout.write(bg_code)
        sys.stdout.write("\033[3J")  # Clear scrollback buffer
        sys.stdout.write("\033[2J")  # Clear visible viewport
        sys.stdout.write("\033[H")   # Move cursor to top-left
        
        # ============================================
        # MANDATORY STEP 2: TRUE FULL VIEWPORT PAINT
        # Fill strictly (rows) lines with (columns) spaces
        # ============================================
        blank_line = " " * width
        
        for row in range(height):
            # Write background code explicit on every line
            sys.stdout.write(f"{bg_code}{blank_line}")
            
            # Use \r\n to ensure we start at column 0 of next line
            # But for the last line, we prevent auto-scroll if possible
            if row < height - 1:
                sys.stdout.write("\n")
                
        # ============================================
        # MANDATORY STEP 4: CURSOR POSITION CONTROL
        # Move cursor back to safe UI start row (0,0) / Home
        # ============================================
        sys.stdout.write("\033[H")
        
        # ============================================
        # MANDATORY STEP 3: FORCE BACKGROUND ON EVERY PRINT
        # Set background attribute strictly for future output
        # ============================================
        sys.stdout.write(bg_code)
        sys.stdout.flush()

    def apply_full_background(self, r: int = None, g: int = None, b: int = None):
        """
        Apply RGB background color to terminal - FULL SCREEN FILL.
        DEPRECATED: Use paint_full_terminal_background(theme) where possible.
        Kept for compatibility with existing calls.
        """
        # Create a temporary dummy object if needed or just update state 
        # so paint_full_terminal_background picks it up
        if r is not None and g is not None and b is not None:
            self.current_bg = (r, g, b)
            
        self.paint_full_terminal_background()

    def apply_background(self, r: int, g: int, b: int):
        """
        Apply RGB background color to terminal.
        """
        self.apply_full_background(r, g, b)

    def repaint_background(self):
        """
        Re-apply the current background without full screen fill.
        """
        if not self.supports_color or self.current_bg is None:
            return
        
        r, g, b = self.current_bg
        bg_sequence = f"\033[48;2;{r};{g};{b}m"
        sys.stdout.write(bg_sequence)
        sys.stdout.flush()

    def ensure_background(self):
        """
        Ensure background color is active for subsequent output.
        """
        if not self.supports_color or self.current_bg is None:
            return
        
        r, g, b = self.current_bg
        # FORCE background ANSI
        sys.stdout.write(f"\033[48;2;{r};{g};{b}m")
        sys.stdout.flush()

    def get_bg_ansi_code(self) -> str:
        """
        Get the ANSI escape sequence for current background.
        """
        if self.current_bg is None:
            return ""
        r, g, b = self.current_bg
        return f"\033[48;2;{r};{g};{b}m"

    def clear_screen_safe(self):
        """
        SAFE screen clear that preserves theme with FULL REPAINT.
        MUST Clear scrollback too.
        """
        if not self.supports_color:
            os.system('cls' if os.name == 'nt' else 'clear')
            return
        
        if self.current_bg is not None:
            self.paint_full_terminal_background()
        else:
            sys.stdout.write("\033[3J\033[2J\033[H")
            sys.stdout.flush()

    def reset_background(self):
        """
        Reset terminal to default colors.
        """
        if not self.supports_color:
            return
        
        sys.stdout.write("\033[0m")
        sys.stdout.write("\033[3J\033[2J\033[H") # Clear scrollback + screen
        sys.stdout.flush()
        self.current_bg = None

    def flash_background(self, r: int, g: int, b: int, duration: float = 0.1):
        """
        Briefly flash background (uses partial repaint for speed if needed, 
        but user requires full fill).
        """
        import time
        saved_bg = self.current_bg
        self.apply_full_background(r, g, b)
        time.sleep(duration)
        if saved_bg:
            self.apply_full_background(*saved_bg)
        else:
            self.reset_background()


# ============================================
# GLOBAL SINGLETON INSTANCE
# ============================================
# This ensures all modules share the same theme state
_theme_engine_instance = None


def get_theme_engine() -> ThemeEngine:
    """
    Get the global ThemeEngine singleton.
    
    This is the ONLY way to access the theme engine.
    Ensures single source of truth for theme state.
    """
    global _theme_engine_instance
    if _theme_engine_instance is None:
        _theme_engine_instance = ThemeEngine()
    return _theme_engine_instance
