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
    
    def apply_full_background(self, r: int = None, g: int = None, b: int = None):
        """
        ================================================================
        CRITICAL: Fill the ENTIRE visible terminal with background color.
        ================================================================
        
        This is the CORE function that fixes the partial background issue.
        It implements true TUI-style full-screen painting.
        
        MUST BE CALLED:
        1. On application startup (before welcome screen)
        2. After ANY theme change
        3. After ANY cls/clear command
        4. After terminal resize (if detected)
        
        ALGORITHM:
        1. Get terminal dimensions: width (columns) × height (rows)
        2. Build ANSI background escape sequence: \033[48;2;R;G;Bm
        3. Clear screen with \033[2J
        4. Move cursor to home with \033[H
        5. FILL EVERY CELL: Print 'height' lines of 'width' spaces
        6. Move cursor back to home position
        7. Set background code for subsequent output
        
        WHY THIS WORKS:
        ANSI background codes only color PRINTED characters.
        Empty/unprinted cells use terminal default background.
        By printing a space in EVERY cell, we color EVERY cell.
        
        Args:
            r: Red component (0-255), or None to use current_bg
            g: Green component (0-255), or None to use current_bg  
            b: Blue component (0-255), or None to use current_bg
        """
        if not self.supports_color:
            return
        
        # ============================================
        # STEP 1: Determine RGB values to use
        # ============================================
        if r is not None and g is not None and b is not None:
            # New color provided - save to state
            self.current_bg = (r, g, b)
        elif self.current_bg is not None:
            # Use existing saved color
            r, g, b = self.current_bg
        else:
            # No color specified and no saved color - nothing to do
            return
        
        # ============================================
        # STEP 2: Build ANSI escape sequence
        # Format: ESC[48;2;R;G;Bm (24-bit TrueColor background)
        # 48 = background, 2 = RGB mode, R;G;B = color values
        # ============================================
        bg_code = f"\033[48;2;{r};{g};{b}m"
        
        # ============================================
        # STEP 3: Get terminal dimensions
        # This tells us how many cells we need to fill
        # ============================================
        try:
            term_size = shutil.get_terminal_size()
            width = term_size.columns   # Number of columns (horizontal cells)
            height = term_size.lines    # Number of rows (vertical lines)
        except Exception:
            # Fallback dimensions if terminal size detection fails
            width = 120
            height = 30
        
        # ============================================
        # STEP 4: Apply background and clear screen
        # Write bg code BEFORE clear so clear inherits the color
        # ============================================
        sys.stdout.write(bg_code)              # Set background color
        sys.stdout.write("\033[2J")            # Clear entire screen
        sys.stdout.write("\033[H")             # Move cursor to home (1,1)
        
        # ============================================
        # STEP 5: FILL THE ENTIRE SCREEN
        # This is the CRITICAL fix - we print a space in EVERY cell
        # Each line is 'width' spaces with the background code
        # We print 'height' such lines to cover the viewport
        # ============================================
        blank_line = " " * width  # Line of spaces (will have bg color)
        
        for row in range(height):
            # Write background code + blank line
            # The background code ensures this line is colored
            # We use \r\n for proper line handling on Windows
            sys.stdout.write(f"{bg_code}{blank_line}")
            if row < height - 1:
                sys.stdout.write("\n")
        
        # ============================================
        # STEP 6: Move cursor back to top-left
        # After filling, cursor is at bottom - move it home
        # ============================================
        sys.stdout.write("\033[H")
        
        # ============================================
        # STEP 7: Ensure background persists for future output
        # Write the bg code one more time so subsequent prints inherit it
        # ============================================
        sys.stdout.write(bg_code)
        
        # Flush all output to terminal
        sys.stdout.flush()
    
    def apply_background(self, r: int, g: int, b: int):
        """
        Apply RGB background color to terminal - FULL SCREEN FILL.
        
        This is the main entry point for changing background color.
        It now delegates to apply_full_background() for complete coverage.
        
        Args:
            r: Red component (0-255)
            g: Green component (0-255)
            b: Blue component (0-255)
        """
        # Delegate to full background fill for complete coverage
        self.apply_full_background(r, g, b)
    
    def repaint_background(self):
        """
        Re-apply the current background without full screen fill.
        
        Use this for quick refreshes after Rich library operations
        that might reset the ANSI state. This only writes the ANSI code,
        it doesn't repaint all cells.
        
        For full repaint after clear, use apply_full_background() instead.
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
        
        Call this after:
        - Rich library console.print() operations
        - Any external library that might reset terminal state
        - Before critical output sections
        
        This writes the ANSI code but doesn't repaint cells.
        For full repaint, use apply_full_background().
        """
        if not self.supports_color or self.current_bg is None:
            return
        
        r, g, b = self.current_bg
        sys.stdout.write(f"\033[48;2;{r};{g};{b}m")
        sys.stdout.flush()
    
    def get_bg_ansi_code(self) -> str:
        """
        Get the ANSI escape sequence for current background.
        
        Use this to prefix output lines to ensure they have the correct
        background color, especially when using print() instead of console.
        
        Returns:
            ANSI escape sequence string, or empty string if no theme set
        """
        if self.current_bg is None:
            return ""
        r, g, b = self.current_bg
        return f"\033[48;2;{r};{g};{b}m"
    
    def clear_screen_safe(self):
        """
        SAFE screen clear that preserves theme with FULL REPAINT.
        
        This is the ONLY way to clear the screen in NovaMind.
        It performs a complete full-screen background fill after clearing.
        
        IMPORTANT: This now calls apply_full_background() to ensure
        the entire terminal viewport is painted with the theme color.
        """
        if not self.supports_color:
            # Fallback for non-color terminals
            os.system('cls' if os.name == 'nt' else 'clear')
            return
        
        if self.current_bg is not None:
            # Full repaint with current background color
            self.apply_full_background()
        else:
            # No theme set - standard clear
            sys.stdout.write("\033[2J\033[H")
            sys.stdout.flush()
    
    def reset_background(self):
        """
        Reset terminal to default colors.
        
        Call this on application exit to restore user's terminal.
        """
        if not self.supports_color:
            return
        
        # \033[0m = reset all attributes (colors, styles)
        sys.stdout.write("\033[0m")
        
        # Clear screen to remove any lingering background
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()
        
        # Clear our state
        self.current_bg = None
    
    def flash_background(self, r: int, g: int, b: int, duration: float = 0.1):
        """
        Briefly flash background color (for alerts/effects).
        
        Args:
            r, g, b: Flash color RGB
            duration: How long to show flash (seconds)
        """
        import time
        
        # Save current background
        saved_bg = self.current_bg
        
        # Flash with full background fill
        self.apply_full_background(r, g, b)
        time.sleep(duration)
        
        # Restore original (if any) with full background fill
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
