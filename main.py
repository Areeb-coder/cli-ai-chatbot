#!/usr/bin/env python3
"""
NovaMind - Creative CLI AI Chatbot
==================================
A highly creative, immersive terminal-based AI chatbot that feels alive.

Features:
  - 6 Dynamic visual themes
  - 18 Unlockable achievements
  - Hidden easter eggs
  - Mood-reactive interface
  - Session statistics
  - Mini-games

Run: python main.py

Author: NovaMind Team
Version: 1.0.0
"""

import sys
import os
import time
import signal
from datetime import datetime

# ============================================
# WINDOWS UNICODE FIX
# ============================================
# Configure UTF-8 encoding for Windows terminals
if sys.platform == 'win32':
    # Set console output encoding to UTF-8
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except AttributeError:
        # Python < 3.7 fallback
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    
    # Enable ANSI escape sequences on Windows
    os.system('')

# Set environment variable for Rich library
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Rich console for beautiful output
from rich.console import Console
from rich.text import Text
from rich.live import Live

# Core modules
from core.styles import get_style_manager, THEMES
from core.theme_engine import get_theme_engine
from core.animator import Animator
from core.ui import UI
from core.ai_engine import get_ai_engine
from core.memory import get_memory
from core.mood import get_mood_detector
from core.commands import get_command_parser
from core.achievements import get_achievement_tracker
from core.easter_eggs import (
    get_easter_egg_hunter, 
    get_random_joke, 
    get_random_fortune, 
    get_8ball_response
)
from core.utils import is_question, sanitize_input


class NovaMind:
    """
    Main NovaMind Chatbot Application.
    Orchestrates all components for immersive chat experience.
    """
    
    def __init__(self):
        # Initialize console with theme
        self.style_manager = get_style_manager()
        self.theme_engine = get_theme_engine()
        self.console = Console(theme=self.style_manager.rich_theme)
        
        # Initialize components
        self.ui = UI(self.console)
        self.animator = Animator(self.console)
        self.ai = get_ai_engine()
        self.memory = get_memory()
        self.mood = get_mood_detector()
        self.commands = get_command_parser()
        self.achievements = get_achievement_tracker()
        self.eggs = get_easter_egg_hunter()
        
        # State
        self.running = True
        self.focus_mode = False
        self._last_message_time = time.time()
        
        # Loop Safety Guards
        self.response_rendered = False
        
        # Setup signal handlers for graceful exit
        signal.signal(signal.SIGINT, self._handle_interrupt)
        if hasattr(signal, 'SIGTERM'):
            signal.signal(signal.SIGTERM, self._handle_interrupt)
    
    def _handle_interrupt(self, signum, frame):
        """Handle Ctrl+C gracefully"""
        self.console.print("\n")
        self.exit_gracefully()
        sys.exit(0)
    
    # ============================================
    # STARTUP
    # ============================================
    
    def start(self):
        """Start NovaMind chatbot"""
        # Apply initial theme background FIRST (before welcome screen)
        # This ensures the welcome screen displays with the correct background
        self._apply_current_theme_bg()
        
        # Show welcome screen (no longer clears - we already cleared above)
        self.ui.show_welcome(animate=not self.focus_mode)
        
        # Initialize AI
        if not self.ai.initialize():
            self.ui.show_error(f"AI initialization failed: {self.ai.last_error}")
            self.ui.show_system_message("Running in limited mode. Check your API key in .env file.")
        else:
            self.ui.show_success("AI engine ready!")
        
        # Ensure background is active after all welcome screen output
        self.theme_engine.ensure_background()
        
        self.console.print()
        
        # Award first contact achievement
        self._check_achievements({"message_count": 1})
        
        # Main loop
        self._main_loop()
    
    def _main_loop(self):
        """Main conversation loop"""
        while self.running:
            try:
                # Reset state for new turn
                self.response_rendered = False
                
                # Get input
                user_input = self._get_input()
                
                if user_input is None:
                    continue
                
                # Process input
                self._process_input(user_input)
                
            except EOFError:
                # Ctrl+D
                self.exit_gracefully()
                break
            except KeyboardInterrupt:
                # Ctrl+C (backup handler)
                self.exit_gracefully()
                break
            except Exception as e:
                self.ui.show_error(f"Something went wrong: {str(e)[:50]}")
    
    # ============================================
    # INPUT HANDLING
    # ============================================
    
    def _get_input(self) -> str:
        """Get user input with styled prompt"""
        theme = self.style_manager.theme
        stats = self.memory.get_session_summary()
        ach_display = self.achievements.get_progress()
        
        # Show subtle status
        self.console.print()
        status = f"  💬 {stats['messages']} | 🏆 {ach_display} | 🎨 {self.memory.current_theme}"
        self.console.print(Text(status, style=theme.muted))
        
        # Input prompt
        try:
            prompt = f"  {theme.emoji} You > "
            user_input = input(prompt)
            return sanitize_input(user_input)
        except (EOFError, KeyboardInterrupt):
            raise
    
    def _process_input(self, user_input: str):
        """Process user input (command or message)"""
        # Handle empty input
        if not user_input.strip():
            self.ui.show_system_message("Say something! I'm listening... 👂")
            return
        
        # Track time for achievements
        self._last_message_time = time.time()
        
        # Check if it's a command
        if self.commands.is_command(user_input):
            cmd, args = self.commands.parse(user_input)
            self._handle_command(cmd, args)
            return
        
        # Check for easter eggs first
        egg = self.eggs.check(user_input)
        if egg:
            self.memory.record_easter_egg(egg.id)
            self._handle_easter_egg(egg)
            return
        
        # Regular conversation
        self._handle_conversation(user_input)
    
    # ============================================
    # COMMAND HANDLING
    # ============================================
    
    def _handle_command(self, cmd: str, args: list):
        """Handle slash commands"""
        self.memory.record_command()
        
        # Check achievements
        self._check_achievements({"command": cmd})
        
        if cmd in ["exit", "quit"]:
            self.exit_gracefully()
            self.running = False
            return
        
        elif cmd == "help":
            help_text = self.commands.get_help_text()
            self.ui.show_help(help_text)
        
        elif cmd == "clear":
            # CRITICAL FIX: Use theme-safe clear that preserves background
            self.theme_engine.clear_screen_safe()
            self.ui.show_welcome(animate=False)
            # Re-apply theme background after welcome screen
            self._apply_current_theme_bg()
            # Ensure background is active for subsequent output
            self.theme_engine.ensure_background()
        
        elif cmd == "reset":
            self.memory.clear()
            self.ui.show_success("Conversation reset! Fresh start. 🌟")
        
        elif cmd == "theme":
            if args:
                target = args[0].lower()
                theme_names = self.style_manager.get_theme_names()
                selected_name = None
                
                # Handle numeric selection
                if target.isdigit():
                    idx = int(target) - 1
                    if 0 <= idx < len(theme_names):
                        selected_name = theme_names[idx]
                elif target in theme_names:
                    selected_name = target
                    
                if selected_name and self.style_manager.switch_theme(selected_name):
                    self.memory.set_theme(selected_name)
                    
                    # ============================================
                    # CRITICAL FIX: DO NOT recreate Console/UI/Animator
                    # Console recreation causes complete state loss and
                    # triggers rendering bugs including token leaks.
                    # 
                    # Instead, we ONLY apply the new theme background.
                    # The style_manager already updated, so Rich will
                    # use new colors on subsequent prints.
                    # ============================================
                    
                    # Apply theme background - this clears screen and applies new colors
                    self._apply_current_theme_bg()
                    
                    # Re-apply background after any potential reset
                    self.theme_engine.ensure_background()
                    
                    # Show success message AFTER theme is applied
                    self.ui.show_success(f"Theme changed to {selected_name} {self.style_manager.theme.emoji}")

                    # Display the new theme's logo
                    from core.logos import get_logo, get_compact_logo
                    import shutil

                    term_width = shutil.get_terminal_size().columns
                    if term_width >= 75:
                        logo = get_logo(selected_name)
                    else:
                        logo = get_compact_logo(selected_name)
                    
                    from rich.align import Align
                    self.console.print(Align.center(Text(logo, style=self.style_manager.theme.primary)))
                    self.console.print()
                    self._check_achievements({"current_theme": selected_name, "themes_used": self.memory.stats.themes_used})
                else:
                    self.ui.show_error(f"Unknown theme. Use /theme to list available options.")
            else:
                self.console.print("\n🎨 Available Themes:", style="bold")
                self.console.print("Type /theme <name> or /theme <number> to switch.\n")
                
                # Show preview list with real colors
                from rich.style import Style as RichStyle
                
                for idx, name in enumerate(self.style_manager.get_theme_names(), 1):
                    t = THEMES[name]
                    # Create a preview block with the theme's background color
                    # We use the RGB values to create a rich style
                    r, g, b = t.bg_rgb
                    preview_style = RichStyle(bgcolor=f"rgb({r},{g},{b})", color=t.user_text)
                    
                    self.console.print(f"  {idx}. ", end="")
                    self.console.print(f" {t.emoji} {t.name:<20} ", style=preview_style)
                self.console.print()
        
        elif cmd == "mode":
            if args:
                mode_name = args[0].lower()
                if self.ai.set_mode(mode_name):
                    self.memory.set_mode(mode_name)
                    self.ui.show_success(f"Mode set to {mode_name} ✨")
                else:
                    self.ui.show_error(f"Unknown mode. Try: {', '.join(self.ai.get_available_modes())}")
            else:
                self.console.print("Available modes:")
                self.console.print(self.commands.get_mode_list())
        
        elif cmd == "stats":
            stats = self.memory.get_session_summary()
            self.ui.show_stats(stats)
        
        elif cmd in ["achievements", "ach"]:
            unlocked = self.achievements.get_unlocked()
            locked = self.achievements.get_locked()
            progress = self.achievements.get_progress()
            self.ui.show_achievements(unlocked, locked, progress)
        
        elif cmd == "sound":
            if args and args[0].lower() in ["on", "off"]:
                enabled = args[0].lower() == "on"
                self.animator.set_sound(enabled)
                
                # Also update global sound engine
                from core.sounds import get_sound_simulator
                sim = get_sound_simulator()
                sim.set_enabled(enabled)
                
                if enabled:
                    sim.play_notification_sound()
                
                self.ui.show_success(f"Sound effects {'enabled' if enabled else 'disabled'}")
            else:
                self.ui.show_system_message("Usage: /sound on|off")
        
        elif cmd == "focus":
            if args and args[0].lower() in ["on", "off"]:
                enabled = args[0].lower() == "on"
                self.focus_mode = enabled
                self.animator.set_focus_mode(enabled)
                self.ui.show_success(f"Focus mode {'enabled' if enabled else 'disabled'}")
            else:
                self.ui.show_system_message("Usage: /focus on|off")
        
        elif cmd == "export":
            if args:
                format_type = args[0].lower()
                self._export_chat(format_type)
            else:
                self.ui.show_system_message("Usage: /export txt|md|json")
        
        elif cmd == "play":
            if args:
                game = args[0].lower()
                self._play_game(game)
            else:
                self.console.print("Available games:")
                self.console.print(self.commands.get_game_list())
        
        elif cmd == "name":
            if args:
                name = " ".join(args)
                self.memory.set_user_name(name)
                self.ui.show_success(f"Nice to meet you, {name}! 👋")
            else:
                self.ui.show_system_message("Usage: /name <your_name>")
        
        elif cmd == "bookmark":
            if self.memory.add_bookmark():
                self.ui.show_success("Bookmark saved! 📌")
                self._check_achievements({"bookmark_count": len(self.memory.bookmarks)})
            else:
                self.ui.show_error("Nothing to bookmark yet!")
        
        elif cmd == "bookmarks":
            bookmarks = self.memory.get_bookmarks()
            if bookmarks:
                self.console.print("\n📚 Your Bookmarks:")
                for i, bm in enumerate(bookmarks, 1):
                    self.console.print(f"  {i}. {bm.message_preview}")
            else:
                self.ui.show_system_message("No bookmarks yet. Use /bookmark to save a moment!")
        
        elif cmd == "about":
            self.ui.show_about()
        
        elif cmd == "hint":
            hint = self.eggs.get_random_hint()
            self.ui.show_system_message(f"🔮 Hint: {hint}")
        
        else:
            self.ui.show_error(f"Unknown command: /{cmd}. Try /help")
    
    # ============================================
    # CONVERSATION
    # ============================================
    
    def _handle_conversation(self, user_input: str):
        """Handle regular conversation with AI"""
        # Display user message
        self.ui.show_user_message(user_input, self.memory.user_name)
        
        # Detect mood
        detected_mood = self.mood.analyze(user_input)
        mood_emoji = detected_mood.emoji
        
        # Store user message
        self.memory.add_message("user", user_input, detected_mood.name)
        self.mood.record_mood(time.time())
        
        # Check for questions (for achievements)
        is_q = is_question(user_input)
        
        # Thinking animation
        self.console.print()
        frames = self.style_manager.get_spinner_frames("dots")
        theme = self.style_manager.theme
        
        # Show thinking
        if not self.focus_mode:
            for i in range(8):
                frame = frames[i % len(frames)]
                self.console.print(f"  {frame} Thinking...", style=theme.system_text, end="\r")
                time.sleep(0.15)
            self.console.print(" " * 30, end="\r")
        
        # Get AI response
        context = self.memory.get_context_for_ai()
        mood_hint = self.mood.suggest_response_tone()
        
        response = self.ai.generate_response(user_input, context, mood_hint)
        
        # CRITICAL: Sanitize response before ANY rendering
        # This strips model tokens like <|im_start|> that must NEVER be displayed
        # CRITICAL: Sanitize response before ANY rendering
        # This strips model tokens like <|im_start|> and system leakage that must NEVER be displayed
        from core.sanitizer import sanitize_output
        sanitized_response = sanitize_output(response)
        
        # Display AI response with typing animation
        self._render_response_safely(sanitized_response, mood_emoji)
        
        # Store AI response
        self.memory.add_message("assistant", response)
        
        # Voice waveform (quick animation)
        if not self.focus_mode:
            self.animator.animate_waveform(0.5)
        
        # Check achievements
        stats = self.memory.get_session_summary()
        self._check_achievements({
            "message_count": stats["messages"],
            "total_words": stats["words"],
            "session_minutes": stats["duration_minutes"],
            "is_question": is_q,
            "mood": detected_mood.name,
            "current_theme": self.memory.current_theme,
            "themes_used": self.memory.stats.themes_used,
        })
    
    def _render_response_safely(self, response: str, mood_emoji: str):
        """Render response with safety checks to prevent duplication"""
        if hasattr(self, 'response_rendered') and self.response_rendered:
            return
        
        if not self.focus_mode:
            self._type_response(response, mood_emoji)
        else:
            self.ui.show_ai_message(response, mood_emoji)
            
        self.response_rendered = True
    
    def _type_response(self, response: str, mood_emoji: str):
        """Display AI response with typing animation - BOX-AWARE RENDERING
        
        FIXED IMPLEMENTATION:
        1. Parse markdown bold -> ANSI bold (no more raw asterisks)
        2. Word-wrap text to fit box inner width (no more overflow)
        3. Render line-by-line with proper padding (no more cutting)
        
        Each character is printed EXACTLY ONCE with proper box boundaries.
        """
        from core.sounds import get_sound_simulator
        from core.text_renderer import prepare_response_for_box, visible_width
        import shutil
        
        theme = self.style_manager.theme
        current_mood = self.mood.get_current_mood()
        speed_mod = current_mood.speed_modifier
        sound = get_sound_simulator()
        
        # ============================================
        # STEP 1: Calculate box dimensions
        # ============================================
        terminal_width = shutil.get_terminal_size().columns
        box_width = min(70, terminal_width - 4)
        
        # ============================================
        # STEP 2: Pre-process and word-wrap response
        # This converts **bold** to ANSI and wraps at word boundaries
        # ============================================
        wrapped_lines, inner_width = prepare_response_for_box(
            response, 
            box_width=box_width,
            terminal_width=terminal_width
        )
        
        # ============================================
        # STEP 3: Render box header (printed ONCE)
        # Get background ANSI code to ensure consistent theme
        # ============================================
        bg_code = self.theme_engine.get_bg_ansi_code()
        
        # Calculate header dynamic width
        # Prefix: "  ╭─ {mood_emoji} NovaMind "
        # We need to measure strictly the VISIBLE width of this prefix
        header_prefix_text = f"  ╭─ {mood_emoji} NovaMind "
        prefix_width = visible_width(header_prefix_text)
        
        # Suffix: "╮" (width 1)
        suffix_width = 1
        
        # Dashes needed: box_width - prefix - suffix
        dashes_needed = box_width - prefix_width - suffix_width
        dashes_needed = max(0, dashes_needed)
        
        print(f"{bg_code}{header_prefix_text}{'─' * dashes_needed}╮", flush=True)
        # Top Empty Line: "  │" + spaces + "│"
        # Width: 3 ("  │") + (box_width - 3 - 2) + 2 (" │") ...
        # Standardize content row: "  │  " (5) + content + " │" (2)
        # top empty line should act like a content line but valid
        # inner_width is box_width - 7
        # So printing 5 chars prefix + inner_width spaces + 2 chars suffix = box_width
        print(f"{bg_code}  │  {' ' * inner_width} │", flush=True)
        
        # ============================================
        # STEP 4: Render each wrapped line with typing animation
        # ============================================
        for line_idx, line in enumerate(wrapped_lines):
            # Print line prefix with background code "  │  "
            print(f"{bg_code}  │  ", end="", flush=True)
            
            # Animate each character in this line
            for char in line:
                print(char, end="", flush=True)
                
                # Skip delay and sound for ANSI escape codes
                if char == '\x1b':
                    continue
                
                # Play typing sound for visible characters
                if char.isalnum() and sound.enabled:
                    sound.play_keystroke_sound()
                
                # Variable delay based on character type
                if char in ".!?":
                    time.sleep(0.08 * speed_mod)
                elif char in ",;:":
                    time.sleep(0.04 * speed_mod)
                elif char == " ":
                    time.sleep(0.01 * speed_mod)
                else:
                    time.sleep(0.02 * speed_mod)
            
            # Pad the rest of the line to align right border
            visible = visible_width(line)
            padding_len = max(0, inner_width - visible)
            padding = ' ' * padding_len
            print(f"{padding} │", flush=True)
        
        # ============================================
        # STEP 5: Render box footer with background code
        #Footer: "  ╰" + dashes + "╯"
        # ============================================
        # Bottom Empty Line
        print(f"{bg_code}  │  {' ' * inner_width} │", flush=True)
        
        # Border
        # Prefix "  ╰" (width 3)
        # Suffix "╯" (width 1)
        # Dashes = box_width - 4
        dashes_len = max(0, box_width - 4)
        print(f"{bg_code}  ╰{'─' * dashes_len}╯", flush=True)
    
    # ============================================
    # EASTER EGGS
    # ============================================
    
    def _handle_easter_egg(self, egg):
        """Handle easter egg trigger"""
        self.ui.show_ai_message(egg.response, "🔮")
        
        # Play special animation if defined
        if egg.animation == "matrix":
            time.sleep(0.5)
            self.animator.matrix_rain(2.0)
        elif egg.animation == "celebration":
            self.animator.celebration_animation()
        
        # Check achievements
        self._check_achievements({
            "found_easter_egg": True,
            "easter_egg_id": egg.id
        })
    
    # ============================================
    # MINI-GAMES
    # ============================================
    
    def _play_game(self, game: str):
        """Play a mini-game"""
        if game == "trivia":
            self._play_trivia()
        elif game == "fortune":
            fortune = get_random_fortune()
            self.ui.show_ai_message(f"🥠 Your fortune:\n\n{fortune}", "🥠")
        elif game == "8ball":
            self.ui.show_system_message("Ask your question, then press Enter...")
            try:
                question = input("  🎱 > ")
                answer = get_8ball_response()
                self.ui.show_ai_message(f"🎱 The Magic 8-Ball says:\n\n{answer}", "🎱")
            except:
                pass
        elif game == "joke":
            setup, punchline = get_random_joke()
            self.ui.show_ai_message(f"😄 {setup}\n\n...{punchline}", "😄")
        else:
            self.ui.show_error(f"Unknown game. Try: trivia, fortune, 8ball, joke")
    
    def _play_trivia(self):
        """Play trivia game"""
        self.ui.show_system_message("Generating trivia question...")
        
        result = self.ai.generate_trivia_question()
        if "content" in result:
            self.ui.show_ai_message(result["content"], "🎯")
    
    # ============================================
    # ACHIEVEMENTS
    # ============================================
    
    def _check_achievements(self, context: dict):
        """Check and award achievements"""
        newly_unlocked = self.achievements.check_and_award(context)
        
        for ach in newly_unlocked:
            self.memory.record_achievement(ach.id)
            self.ui.show_achievement_unlock(ach)
    
    # ============================================
    # EXPORT
    # ============================================
    
    def _export_chat(self, format_type: str):
        """Export chat history"""
        from core.utils import save_to_file, save_json, get_exports_directory
        
        exports_dir = get_exports_directory()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format_type == "txt":
            content = self.memory.export_txt()
            filename = f"novamind_chat_{timestamp}.txt"
            if save_to_file(content, filename, exports_dir):
                self.ui.show_success(f"Exported to {exports_dir}/{filename}")
            else:
                self.ui.show_error("Export failed!")
        
        elif format_type == "md":
            content = self.memory.export_markdown()
            filename = f"novamind_chat_{timestamp}.md"
            if save_to_file(content, filename, exports_dir):
                self.ui.show_success(f"Exported to {exports_dir}/{filename}")
            else:
                self.ui.show_error("Export failed!")
        
        elif format_type == "json":
            data = self.memory.export_json()
            filename = f"novamind_chat_{timestamp}.json"
            if save_json(data, filename, exports_dir):
                self.ui.show_success(f"Exported to {exports_dir}/{filename}")
            else:
                self.ui.show_error("Export failed!")
        
        else:
            self.ui.show_error("Unknown format. Try: txt, md, json")
    
    def _apply_current_theme_bg(self):
        """
        Apply current theme's background color to the ENTIRE terminal viewport.
        
        This method is the CRITICAL entry point for full-screen background painting.
        It MUST be called:
        1. On application startup (before welcome screen)
        2. After ANY theme change via /theme command
        3. After ANY /clear command
        
        The theme_engine.apply_full_background() method fills EVERY cell in the
        terminal with the background color by printing spaces, ensuring the
        entire viewport is colored (not just printed areas).
        """
        if hasattr(self.style_manager.theme, 'bg_rgb'):
            r, g, b = self.style_manager.theme.bg_rgb
            # apply_full_background fills the ENTIRE terminal viewport
            self.theme_engine.apply_full_background(r, g, b)

    # ============================================
    # EXIT
    # ============================================
    
    def exit_gracefully(self):
        """Show exit summary and cleanup"""
        stats = self.memory.get_session_summary()
        mood_journey = self.mood.get_mood_journey()
        
        # Reset background on exit
        if hasattr(self, 'theme_engine'):
            self.theme_engine.reset_background()
        
        self.console.print()
        self.ui.show_exit_summary(stats, mood_journey)


# ============================================
# MAIN ENTRY POINT
# ============================================

def main():
    """Main entry point"""
    try:
        app = NovaMind()
        app.start()
    except KeyboardInterrupt:
        print("\n\n  👋 Goodbye! See you next time!\n")
    except Exception as e:
        print(f"\n  ❌ Fatal error: {e}")
        print("  Please check your setup and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()
