"""
NovaMind Commands Module
========================
Command parser and handlers for slash commands.
"""

from typing import Optional, Tuple, Callable, Dict, Any
from dataclasses import dataclass
import os


@dataclass
class Command:
    """Command definition"""
    name: str
    description: str
    usage: str
    handler: Optional[str] = None  # Handler function name


# ============================================
# COMMAND DEFINITIONS
# ============================================

COMMANDS: Dict[str, Command] = {
    "help": Command(
        name="help",
        description="Show available commands",
        usage="/help"
    ),
    "clear": Command(
        name="clear",
        description="Clear the terminal screen",
        usage="/clear"
    ),
    "exit": Command(
        name="exit",
        description="Exit with session summary",
        usage="/exit or /quit"
    ),
    "quit": Command(
        name="quit",
        description="Exit with session summary",
        usage="/quit or /exit"
    ),
    "reset": Command(
        name="reset",
        description="Reset conversation history",
        usage="/reset"
    ),
    "theme": Command(
        name="theme",
        description="Change visual theme",
        usage="/theme <name> (neon, hacker, zen, retro, ocean, sunset)"
    ),
    "mode": Command(
        name="mode",
        description="Change AI personality mode",
        usage="/mode <type> (creative, serious, friendly, sarcastic)"
    ),
    "stats": Command(
        name="stats",
        description="Show session statistics",
        usage="/stats"
    ),
    "achievements": Command(
        name="achievements",
        description="View unlocked achievements",
        usage="/achievements or /ach"
    ),
    "ach": Command(
        name="ach",
        description="View unlocked achievements (shortcut)",
        usage="/ach"
    ),
    "sound": Command(
        name="sound",
        description="Toggle typing sound effects",
        usage="/sound on|off"
    ),
    "focus": Command(
        name="focus",
        description="Toggle focus mode (minimal animations)",
        usage="/focus on|off"
    ),
    "export": Command(
        name="export",
        description="Export chat history",
        usage="/export <format> (txt, md, json)"
    ),
    "play": Command(
        name="play",
        description="Play a mini-game",
        usage="/play <game> (trivia, fortune, 8ball, joke)"
    ),
    "name": Command(
        name="name",
        description="Set your nickname",
        usage="/name <your_name>"
    ),
    "bookmark": Command(
        name="bookmark",
        description="Bookmark current conversation point",
        usage="/bookmark"
    ),
    "bookmarks": Command(
        name="bookmarks",
        description="List saved bookmarks",
        usage="/bookmarks"
    ),
    "about": Command(
        name="about",
        description="About NovaMind",
        usage="/about"
    ),
    "hint": Command(
        name="hint",
        description="Get a hint about hidden secrets",
        usage="/hint"
    ),
}


class CommandParser:
    """
    Parses and handles slash commands.
    """
    
    def __init__(self):
        self.last_command: Optional[str] = None
    
    def is_command(self, text: str) -> bool:
        """Check if text is a command"""
        return text.strip().startswith("/")
    
    def parse(self, text: str) -> Tuple[Optional[str], list]:
        """
        Parse command text.
        Returns (command_name, arguments) or (None, []) if not a command.
        """
        text = text.strip()
        if not text.startswith("/"):
            return None, []
        
        parts = text[1:].split()
        if not parts:
            return None, []
        
        command = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        self.last_command = command
        return command, args
    
    def get_command(self, name: str) -> Optional[Command]:
        """Get command by name"""
        return COMMANDS.get(name.lower())
    
    def get_all_commands(self) -> Dict[str, Command]:
        """Get all commands"""
        return COMMANDS
    
    def get_help_text(self) -> str:
        """Generate help text for all commands"""
        lines = [
            "╭─────────────────────────────────────────────────────╮",
            "│              📚 AVAILABLE COMMANDS                  │",
            "╰─────────────────────────────────────────────────────╯",
            ""
        ]
        
        # Group commands by category
        categories = {
            "General": ["help", "clear", "exit", "about"],
            "Customization": ["theme", "mode", "name", "sound", "focus"],
            "Session": ["stats", "achievements", "reset", "bookmark", "bookmarks"],
            "Fun": ["play", "hint"],
            "Export": ["export"],
        }
        
        for category, cmds in categories.items():
            lines.append(f"  {category}:")
            for cmd_name in cmds:
                if cmd_name in COMMANDS:
                    cmd = COMMANDS[cmd_name]
                    lines.append(f"    {cmd.usage:<30} - {cmd.description}")
            lines.append("")
        
        return "\n".join(lines)
    
    def get_theme_list(self) -> str:
        """Get formatted theme list"""
        themes = [
            ("neon", "🌆 Cyberpunk glow"),
            ("hacker", "🖥️ Matrix green"),
            ("zen", "🧘 Calm pastels"),
            ("retro", "📺 Amber CRT"),
            ("ocean", "🌊 Deep blue"),
            ("sunset", "🌅 Warm gradients"),
        ]
        return "\n".join([f"  {name:<10} {desc}" for name, desc in themes])
    
    def get_mode_list(self) -> str:
        """Get formatted mode list"""
        modes = [
            ("creative", "Imaginative and playful"),
            ("serious", "Professional and focused"),
            ("friendly", "Warm and casual (default)"),
            ("sarcastic", "Witty with sass"),
        ]
        return "\n".join([f"  {name:<12} {desc}" for name, desc in modes])
    
    def get_game_list(self) -> str:
        """Get formatted game list"""
        games = [
            ("trivia", "🎯 Quick trivia question"),
            ("fortune", "🥠 Fortune cookie wisdom"),
            ("8ball", "🎱 Magic 8-ball predictions"),
            ("joke", "😄 Tell a joke"),
        ]
        return "\n".join([f"  {name:<10} {desc}" for name, desc in games])


# Global command parser
command_parser = CommandParser()


def get_command_parser() -> CommandParser:
    """Get the global command parser"""
    return command_parser
