"""
NovaMind Memory Module
======================
Manages conversation context and session statistics.
Tracks achievements and provides session summaries.
"""

import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field


@dataclass
class Message:
    """Single conversation message"""
    role: str  # "user" or "assistant"
    content: str
    timestamp: float
    mood: str = "neutral"
    
    def to_dict(self) -> dict:
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp,
            "mood": self.mood
        }


@dataclass
class SessionStats:
    """Statistics for current session"""
    start_time: float = field(default_factory=time.time)
    message_count: int = 0
    user_message_count: int = 0
    ai_message_count: int = 0
    word_count: int = 0
    mood_changes: int = 0
    commands_used: int = 0
    achievements_unlocked: List[str] = field(default_factory=list)
    themes_used: List[str] = field(default_factory=list)
    easter_eggs_found: List[str] = field(default_factory=list)
    fastest_reply: float = float('inf')
    
    def get_duration_minutes(self) -> float:
        """Get session duration in minutes"""
        return (time.time() - self.start_time) / 60
    
    def get_duration_formatted(self) -> str:
        """Get formatted duration string"""
        minutes = int(self.get_duration_minutes())
        if minutes < 1:
            return "< 1 minute"
        elif minutes == 1:
            return "1 minute"
        elif minutes < 60:
            return f"{minutes} minutes"
        else:
            hours = minutes // 60
            mins = minutes % 60
            return f"{hours}h {mins}m"


@dataclass
class Bookmark:
    """Saved conversation moment"""
    index: int
    message_preview: str
    timestamp: float
    mood: str


class ConversationMemory:
    """
    Manages conversation history and session state.
    Provides context for AI and tracks user interactions.
    """
    
    def __init__(self, max_history: int = 50):
        self.messages: List[Message] = []
        self.max_history = max_history
        self.stats = SessionStats()
        self.bookmarks: List[Bookmark] = []
        self.user_name: str = "User"
        self.current_mode: str = "friendly"
        self.current_theme: str = "neon"
        self._last_user_message_time: float = 0
    
    def add_message(self, role: str, content: str, mood: str = "neutral"):
        """Add a message to conversation history"""
        timestamp = time.time()
        message = Message(role, content, timestamp, mood)
        self.messages.append(message)
        
        # Update stats
        self.stats.message_count += 1
        self.stats.word_count += len(content.split())
        
        if role == "user":
            self.stats.user_message_count += 1
            self._last_user_message_time = timestamp
        else:
            self.stats.ai_message_count += 1
            # Check for fast reply
            if self._last_user_message_time > 0:
                reply_time = timestamp - self._last_user_message_time
                if reply_time < self.stats.fastest_reply:
                    self.stats.fastest_reply = reply_time
        
        # Trim history if too long
        if len(self.messages) > self.max_history:
            self.messages = self.messages[-self.max_history:]
    
    def get_context(self, last_n: int = 10) -> List[dict]:
        """Get recent conversation context for AI"""
        recent = self.messages[-last_n:] if len(self.messages) > last_n else self.messages
        return [msg.to_dict() for msg in recent]
    
    def get_context_for_ai(self, last_n: int = 10) -> List[dict]:
        """Get context formatted for AI API calls"""
        context = []
        recent = self.messages[-last_n:] if len(self.messages) > last_n else self.messages
        
        for msg in recent:
            context.append({
                "role": "user" if msg.role == "user" else "model",
                "parts": [{"text": msg.content}]
            })
        
        return context
    
    def clear(self):
        """Clear conversation history"""
        self.messages = []
        # Keep stats but reset message count
        old_stats = self.stats
        self.stats = SessionStats()
        self.stats.themes_used = old_stats.themes_used
        self.stats.achievements_unlocked = old_stats.achievements_unlocked
    
    def add_bookmark(self, preview_length: int = 50) -> bool:
        """Bookmark current position in conversation"""
        if not self.messages:
            return False
        
        last_msg = self.messages[-1]
        preview = last_msg.content[:preview_length]
        if len(last_msg.content) > preview_length:
            preview += "..."
        
        bookmark = Bookmark(
            index=len(self.messages) - 1,
            message_preview=preview,
            timestamp=last_msg.timestamp,
            mood=last_msg.mood
        )
        self.bookmarks.append(bookmark)
        return True
    
    def get_bookmarks(self) -> List[Bookmark]:
        """Get all bookmarks"""
        return self.bookmarks
    
    def record_achievement(self, achievement_id: str):
        """Record an unlocked achievement"""
        if achievement_id not in self.stats.achievements_unlocked:
            self.stats.achievements_unlocked.append(achievement_id)
    
    def record_theme_used(self, theme_name: str):
        """Record a theme being used"""
        if theme_name not in self.stats.themes_used:
            self.stats.themes_used.append(theme_name)
    
    def record_easter_egg(self, egg_id: str):
        """Record an easter egg being found"""
        if egg_id not in self.stats.easter_eggs_found:
            self.stats.easter_eggs_found.append(egg_id)
    
    def record_command(self):
        """Record a command being used"""
        self.stats.commands_used += 1
    
    def set_user_name(self, name: str):
        """Set user's nickname"""
        self.user_name = name
    
    def set_mode(self, mode: str):
        """Set conversation mode"""
        self.current_mode = mode
    
    def set_theme(self, theme: str):
        """Set current theme"""
        self.current_theme = theme
        self.record_theme_used(theme)
    
    def get_memorable_moment(self) -> Optional[str]:
        """Get a random memorable message from the session"""
        if len(self.messages) < 3:
            return None
        
        # Find longer, meaningful messages
        good_messages = [
            msg for msg in self.messages 
            if msg.role == "user" and len(msg.content) > 30
        ]
        
        if good_messages:
            import random
            return random.choice(good_messages).content[:80]
        
        return None
    
    def get_session_summary(self) -> dict:
        """Get comprehensive session summary"""
        return {
            "messages": self.stats.message_count,
            "user_messages": self.stats.user_message_count,
            "ai_messages": self.stats.ai_message_count,
            "words": self.stats.word_count,
            "duration": self.stats.get_duration_formatted(),
            "duration_minutes": int(self.stats.get_duration_minutes()),
            "achievements": len(self.stats.achievements_unlocked),
            "themes_used": len(self.stats.themes_used),
            "commands_used": self.stats.commands_used,
            "easter_eggs": len(self.stats.easter_eggs_found),
            "memorable_moment": self.get_memorable_moment(),
        }
    
    def export_txt(self) -> str:
        """Export conversation as plain text"""
        lines = [
            f"NovaMind Chat Export",
            f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            f"Duration: {self.stats.get_duration_formatted()}",
            "=" * 50,
            ""
        ]
        
        for msg in self.messages:
            role = "You" if msg.role == "user" else "NovaMind"
            time_str = datetime.fromtimestamp(msg.timestamp).strftime("%H:%M")
            lines.append(f"[{time_str}] {role}:")
            lines.append(msg.content)
            lines.append("")
        
        return "\n".join(lines)
    
    def export_markdown(self) -> str:
        """Export conversation as Markdown"""
        lines = [
            "# NovaMind Chat Export",
            "",
            f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            f"**Duration:** {self.stats.get_duration_formatted()}",
            f"**Messages:** {self.stats.message_count}",
            "",
            "---",
            ""
        ]
        
        for msg in self.messages:
            role = "**You**" if msg.role == "user" else "**🤖 NovaMind**"
            time_str = datetime.fromtimestamp(msg.timestamp).strftime("%H:%M")
            lines.append(f"### {role} `{time_str}`")
            lines.append("")
            lines.append(msg.content)
            lines.append("")
        
        return "\n".join(lines)
    
    def export_json(self) -> dict:
        """Export conversation as JSON-serializable dict"""
        return {
            "metadata": {
                "export_date": datetime.now().isoformat(),
                "duration": self.stats.get_duration_formatted(),
                "user_name": self.user_name,
                "theme": self.current_theme,
                "mode": self.current_mode,
            },
            "stats": self.get_session_summary(),
            "messages": [msg.to_dict() for msg in self.messages],
            "bookmarks": [
                {
                    "index": b.index,
                    "preview": b.message_preview,
                    "timestamp": b.timestamp,
                    "mood": b.mood
                }
                for b in self.bookmarks
            ]
        }


# Global memory instance
conversation_memory = ConversationMemory()


def get_memory() -> ConversationMemory:
    """Get the global conversation memory"""
    return conversation_memory
