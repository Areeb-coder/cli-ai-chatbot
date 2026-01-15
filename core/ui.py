"""
NovaMind UI Module
==================
Terminal UI components: panels, boxes, welcome screen.
Uses Rich library for beautiful formatting.
"""

import shutil
import random
from datetime import datetime
from typing import Optional, List
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.columns import Columns
from rich.align import Align
from rich.box import ROUNDED, DOUBLE, HEAVY, SIMPLE

from .styles import get_style_manager


# ASCII Art Logo
LOGO = """
███╗   ██╗ ██████╗ ██╗   ██╗ █████╗ ███╗   ███╗██╗███╗   ██╗██████╗ 
████╗  ██║██╔═══██╗██║   ██║██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗
██╔██╗ ██║██║   ██║██║   ██║███████║██╔████╔██║██║██╔██╗ ██║██║  ██║
██║╚██╗██║██║   ██║╚██╗ ██╔╝██╔══██║██║╚██╔╝██║██║██║╚██╗██║██║  ██║
██║ ╚████║╚██████╔╝ ╚████╔╝ ██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██████╔╝
╚═╝  ╚═══╝ ╚═════╝   ╚═══╝  ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═════╝ 
"""

LOGO_SMALL = """
╔╗╔┌─┐┬  ┬┌─┐╔╦╗┬┌┐┌┌┬┐
║║║│ │└┐┌┘├─┤║║║││││ ││
╝╚╝└─┘ └┘ ┴ ┴╩ ╩┴┘└┘─┴┘
"""

# Taglines
TAGLINES = [
    "Your AI companion in the terminal ✨",
    "Where conversations come alive 💫",
    "Intelligence meets creativity 🧠",
    "Chat different. Chat NovaMind. 🚀",
    "A terminal that talks back 💬",
]

# Startup tips
TIPS = [
    "💡 Type /help to see all commands",
    "🎨 Try /theme hacker for Matrix vibes",
    "🎮 Type /play trivia to test your knowledge",
    "🔮 There are hidden easter eggs to discover!",
    "📌 Use /bookmark to save important moments",
]


class UI:
    """
    Terminal UI manager for NovaMind.
    Handles all visual display elements.
    """
    
    def __init__(self, console: Console):
        self.console = console
        self.style_manager = get_style_manager()
        self.term_width = shutil.get_terminal_size().columns
        self.focus_mode = False
    
    def refresh_size(self):
        """Refresh terminal size"""
        self.term_width = shutil.get_terminal_size().columns
    
    # ============================================
    # WELCOME SCREEN
    # ============================================
    
    def show_welcome(self, animate: bool = True):
        """Display animated welcome screen"""
        self.console.clear()
        theme = self.style_manager.theme
        
        # Choose logo based on terminal width
        if self.term_width >= 75:
            logo = LOGO
        else:
            logo = LOGO_SMALL
        
        # Display logo
        logo_text = Text(logo, style=theme.primary)
        self.console.print(Align.center(logo_text))
        
        # Tagline
        tagline = random.choice(TAGLINES)
        self.console.print(Align.center(Text(tagline, style=theme.secondary)))
        self.console.print()
        
        # Time-based greeting
        greeting = self._get_time_greeting()
        self.console.print(Align.center(Text(greeting, style=theme.ai_text)))
        self.console.print()
        
        # Tip
        tip = random.choice(TIPS)
        tip_panel = Panel(
            Text(tip, style=theme.muted),
            border_style=theme.border,
            box=ROUNDED,
            width=min(60, self.term_width - 4),
            title="💡 Tip",
            title_align="left"
        )
        self.console.print(Align.center(tip_panel))
        self.console.print()
        
        # Separator
        self.console.print(
            Align.center(
                Text("─" * min(50, self.term_width - 10), style=theme.muted)
            )
        )
        self.console.print()
    
    def _get_time_greeting(self) -> str:
        """Get greeting based on current time"""
        hour = datetime.now().hour
        
        if 5 <= hour < 12:
            return "☀️ Good morning! Ready to start the day?"
        elif 12 <= hour < 17:
            return "🌤️ Good afternoon! Hope your day is going well!"
        elif 17 <= hour < 21:
            return "🌅 Good evening! What's on your mind?"
        else:
            return "🌙 Burning the midnight oil? I'm here for you!"
    
    # ============================================
    # MESSAGE DISPLAY
    # ============================================
    
    def show_user_message(self, message: str, name: str = "You"):
        """Display user message in styled panel"""
        theme = self.style_manager.theme
        
        panel = Panel(
            Text(message, style=theme.user_text),
            border_style=theme.user_text,
            box=ROUNDED,
            title=f"👤 {name}",
            title_align="left",
            width=min(70, self.term_width - 4),
            padding=(0, 1)
        )
        self.console.print(panel)
    
    def show_ai_message(self, message: str, mood_emoji: str = "🤖"):
        """Display AI message in styled panel"""
        theme = self.style_manager.theme
        
        panel = Panel(
            Text(message, style=theme.ai_text),
            border_style=theme.ai_text,
            box=ROUNDED,
            title=f"{mood_emoji} NovaMind",
            title_align="left",
            width=min(70, self.term_width - 4),
            padding=(0, 1)
        )
        self.console.print(panel)
    
    def show_system_message(self, message: str, title: str = "System"):
        """Display system message"""
        theme = self.style_manager.theme
        
        self.console.print(
            Text(f"  ℹ️  {message}", style=theme.system_text)
        )
    
    def show_error(self, message: str):
        """Display error message"""
        theme = self.style_manager.theme
        
        self.console.print(
            Text(f"  ⚠️  {message}", style=theme.error_text)
        )
    
    def show_success(self, message: str):
        """Display success message"""
        self.console.print(
            Text(f"  ✅ {message}", style="bright_green")
        )
    
    # ============================================
    # PANELS & BOXES
    # ============================================
    
    def show_help(self, help_text: str):
        """Display help panel"""
        theme = self.style_manager.theme
        
        panel = Panel(
            Text(help_text, style=theme.ai_text),
            border_style=theme.border,
            box=DOUBLE,
            title="📚 Help",
            title_align="center",
            padding=(1, 2)
        )
        self.console.print(panel)
    
    def show_stats(self, stats: dict):
        """Display session statistics"""
        theme = self.style_manager.theme
        
        table = Table(
            show_header=False,
            box=ROUNDED,
            border_style=theme.border,
            padding=(0, 1)
        )
        table.add_column("Stat", style=theme.muted)
        table.add_column("Value", style=theme.primary)
        
        table.add_row("💬 Messages", str(stats.get("messages", 0)))
        table.add_row("📝 Words", f"{stats.get('words', 0):,}")
        table.add_row("⏱️  Duration", stats.get("duration", "0 min"))
        table.add_row("🏆 Achievements", str(stats.get("achievements", 0)))
        table.add_row("🎨 Themes Used", str(stats.get("themes_used", 0)))
        table.add_row("🔮 Easter Eggs", str(stats.get("easter_eggs", 0)))
        
        panel = Panel(
            table,
            border_style=theme.border,
            box=DOUBLE,
            title="📊 Session Stats",
            title_align="center"
        )
        self.console.print(panel)
    
    def show_achievements(self, unlocked: List, locked: List, progress: str):
        """Display achievements panel"""
        theme = self.style_manager.theme
        
        lines = [f"Progress: {progress}\n"]
        
        if unlocked:
            lines.append("🏆 Unlocked:")
            for ach in unlocked:
                lines.append(f"  {ach.emoji} {ach.name} - {ach.description}")
            lines.append("")
        
        if locked:
            lines.append("🔒 Locked:")
            for ach in locked[:5]:  # Show only first 5 locked
                lines.append(f"  ❓ {ach.name} - {ach.description}")
            if len(locked) > 5:
                lines.append(f"  ... and {len(locked) - 5} more to discover!")
        
        panel = Panel(
            Text("\n".join(lines), style=theme.ai_text),
            border_style=theme.border,
            box=DOUBLE,
            title="🏆 Achievements",
            title_align="center",
            padding=(1, 2)
        )
        self.console.print(panel)
    
    def show_achievement_unlock(self, achievement):
        """Display achievement unlock notification"""
        theme = self.style_manager.theme
        
        content = f"{achievement.emoji} {achievement.name}\n{achievement.description}"
        
        panel = Panel(
            Align.center(Text(content, style=theme.highlight)),
            border_style="bright_yellow",
            box=HEAVY,
            title="🎉 Achievement Unlocked!",
            title_align="center",
            width=min(50, self.term_width - 4),
            padding=(1, 2)
        )
        self.console.print()
        self.console.print(Align.center(panel))
        self.console.print()
    
    def show_about(self):
        """Display about panel"""
        theme = self.style_manager.theme
        
        about_text = """
🤖 NovaMind v1.0

A creative CLI AI chatbot that feels alive.

Features:
  • 🎨 6 Dynamic themes
  • 🏆 18 Achievements to unlock
  • 🔮 Hidden easter eggs
  • 💬 Mood-reactive interface
  • 📊 Session statistics
  • 🎮 Mini-games

Made with ❤️ for the terminal lovers.
"""
        
        panel = Panel(
            Text(about_text.strip(), style=theme.ai_text),
            border_style=theme.primary,
            box=DOUBLE,
            title="About",
            title_align="center",
            padding=(1, 2)
        )
        self.console.print(panel)
    
    # ============================================
    # SESSION SUMMARY
    # ============================================
    
    def show_exit_summary(self, stats: dict, mood_journey: str = ""):
        """Display beautiful exit summary"""
        theme = self.style_manager.theme
        
        lines = [
            "",
            "╔══════════════════════════════════════════════════════╗",
            "║              ✨ SESSION COMPLETE ✨                  ║",
            "╠══════════════════════════════════════════════════════╣",
        ]
        
        # Stats - using proper string formatting
        msg_count = str(stats.get('messages', 0))
        duration = str(stats.get('duration', 'N/A'))
        words = f"{stats.get('words', 0):,}"
        ach_count = str(stats.get('achievements', 0))
        
        lines.append(f"║  📊 Messages Exchanged: {msg_count:<26}║")
        lines.append(f"║  ⏱️  Session Duration: {duration:<27}║")
        lines.append(f"║  💬 Words Spoken: {words:<33}║")
        lines.append(f"║  🏆 Achievements Unlocked: {ach_count:<24}║")
        
        if mood_journey:
            lines.append("╠══════════════════════════════════════════════════════╣")
            lines.append(f"║  💫 Mood Journey: {mood_journey:<33}║")
        
        memorable = stats.get('memorable_moment')
        if memorable:
            lines.append("╠══════════════════════════════════════════════════════╣")
            lines.append("║  🌟 Memorable Moment:                                ║")
            # Wrap memorable moment to fit
            wrapped = memorable[:45] + "..."
            lines.append(f"║  {wrapped:<50}║")
        
        lines.append("╚══════════════════════════════════════════════════════╝")
        lines.append("")
        lines.append("        Thanks for chatting! See you soon! 👋")
        lines.append("")
        
        for line in lines:
            self.console.print(Text(line, style=theme.primary))
    
    # ============================================
    # INPUT PROMPT
    # ============================================
    
    def get_prompt(self, message_count: int, achievements_display: str = "") -> str:
        """Get styled input prompt"""
        theme = self.style_manager.theme
        
        # Status bar
        status = f"💬 {message_count}"
        if achievements_display:
            status += f" | 🏆 {achievements_display}"
        
        self.console.print(Text(f"  {status}", style=theme.muted))
        self.console.print(Text("  ⌨️  Type a message (/help for commands)", style=theme.muted))
        
        # Actual prompt
        return f"  {theme.emoji} > "
    
    def show_thinking(self) -> str:
        """Show thinking indicator and return the message"""
        theme = self.style_manager.theme
        return f"  🤔 Thinking..."
    
    # ============================================
    # UTILITY
    # ============================================
    
    def clear(self):
        """Clear the terminal"""
        self.console.clear()
    
    def set_focus_mode(self, enabled: bool):
        """Set focus mode"""
        self.focus_mode = enabled
    
    def show_divider(self):
        """Show a subtle divider"""
        theme = self.style_manager.theme
        self.console.print(
            Text("  " + "─" * min(40, self.term_width - 10), style=theme.muted)
        )


def get_ui(console: Console) -> UI:
    """Factory function to create UI"""
    return UI(console)
