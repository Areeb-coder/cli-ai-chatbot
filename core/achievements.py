"""
NovaMind Achievements Module
============================
Gamification system with unlockable badges.
Tracks user progress and milestones.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Callable
from datetime import datetime
import time


@dataclass
class Achievement:
    """Achievement definition"""
    id: str
    name: str
    description: str
    emoji: str
    secret: bool = False  # Secret achievements are hidden until unlocked


# ============================================
# ACHIEVEMENT DEFINITIONS
# ============================================

ACHIEVEMENTS: Dict[str, Achievement] = {
    "first_contact": Achievement(
        id="first_contact",
        name="First Contact",
        description="Start your first conversation",
        emoji="🌟"
    ),
    "chatterbox": Achievement(
        id="chatterbox",
        name="Chatterbox",
        description="Send 50 messages in a session",
        emoji="💬"
    ),
    "curious_mind": Achievement(
        id="curious_mind",
        name="Curious Mind",
        description="Ask 10 questions",
        emoji="🤔"
    ),
    "theme_explorer": Achievement(
        id="theme_explorer",
        name="Theme Explorer",
        description="Try all available themes",
        emoji="🎨"
    ),
    "secret_finder": Achievement(
        id="secret_finder",
        name="Secret Finder",
        description="Discover an easter egg",
        emoji="🔮"
    ),
    "night_owl": Achievement(
        id="night_owl",
        name="Night Owl",
        description="Chat after midnight",
        emoji="🦉"
    ),
    "early_bird": Achievement(
        id="early_bird",
        name="Early Bird",
        description="Chat before 6 AM",
        emoji="🐦"
    ),
    "speed_demon": Achievement(
        id="speed_demon",
        name="Speed Demon",
        description="Reply within 2 seconds",
        emoji="⚡"
    ),
    "marathon": Achievement(
        id="marathon",
        name="Marathon Chatter",
        description="Chat for over 30 minutes",
        emoji="🏃"
    ),
    "wordsmith": Achievement(
        id="wordsmith",
        name="Wordsmith",
        description="Write over 1000 words total",
        emoji="✍️"
    ),
    "bookworm": Achievement(
        id="bookworm",
        name="Bookworm",
        description="Create 5 bookmarks",
        emoji="📚"
    ),
    "commander": Achievement(
        id="commander",
        name="Commander",
        description="Use 10 different commands",
        emoji="⌨️"
    ),
    "mood_master": Achievement(
        id="mood_master",
        name="Mood Master",
        description="Experience 5 different moods",
        emoji="🎭"
    ),
    "zen_master": Achievement(
        id="zen_master",
        name="Zen Master",
        description="Use the zen theme for 10 minutes",
        emoji="🧘"
    ),
    "hacker": Achievement(
        id="hacker",
        name="Elite Hacker",
        description="Find the sudo easter egg",
        emoji="💻",
        secret=True
    ),
    "nostalgia": Achievement(
        id="nostalgia",
        name="Nostalgia Trip",
        description="Use the retro theme",
        emoji="📺"
    ),
    "birthday": Achievement(
        id="birthday",
        name="Party Time!",
        description="Celebrate a birthday",
        emoji="🎂",
        secret=True
    ),
    "completionist": Achievement(
        id="completionist",
        name="Completionist",
        description="Unlock 10 achievements",
        emoji="🏆"
    ),
}


class AchievementTracker:
    """
    Tracks and awards achievements.
    Checks conditions and unlocks badges.
    """
    
    def __init__(self):
        self.unlocked: Dict[str, float] = {}  # id -> timestamp
        self.commands_used: set = set()
        self.moods_experienced: set = set()
        self.questions_asked: int = 0
        self.zen_start_time: Optional[float] = None
    
    def unlock(self, achievement_id: str) -> Optional[Achievement]:
        """
        Unlock an achievement if not already unlocked.
        Returns the achievement if newly unlocked, None otherwise.
        """
        if achievement_id in self.unlocked:
            return None
        
        if achievement_id in ACHIEVEMENTS:
            self.unlocked[achievement_id] = time.time()
            
            # Check for completionist
            if len(self.unlocked) >= 10 and "completionist" not in self.unlocked:
                self.unlock("completionist")
            
            return ACHIEVEMENTS[achievement_id]
        
        return None
    
    def check_and_award(self, context: dict) -> List[Achievement]:
        """
        Check conditions and award any earned achievements.
        Returns list of newly unlocked achievements.
        """
        newly_unlocked = []
        
        # First Contact - first message
        if context.get("message_count", 0) >= 1:
            ach = self.unlock("first_contact")
            if ach:
                newly_unlocked.append(ach)
        
        # Chatterbox - 50 messages
        if context.get("message_count", 0) >= 50:
            ach = self.unlock("chatterbox")
            if ach:
                newly_unlocked.append(ach)
        
        # Curious Mind - 10 questions
        if context.get("is_question", False):
            self.questions_asked += 1
        if self.questions_asked >= 10:
            ach = self.unlock("curious_mind")
            if ach:
                newly_unlocked.append(ach)
        
        # Theme Explorer - all themes
        if len(context.get("themes_used", [])) >= 6:
            ach = self.unlock("theme_explorer")
            if ach:
                newly_unlocked.append(ach)
        
        # Secret Finder - easter egg
        if context.get("found_easter_egg", False):
            ach = self.unlock("secret_finder")
            if ach:
                newly_unlocked.append(ach)
        
        # Night Owl - after midnight
        current_hour = datetime.now().hour
        if current_hour >= 0 and current_hour < 5:
            ach = self.unlock("night_owl")
            if ach:
                newly_unlocked.append(ach)
        
        # Early Bird - before 6 AM
        if current_hour >= 4 and current_hour < 6:
            ach = self.unlock("early_bird")
            if ach:
                newly_unlocked.append(ach)
        
        # Speed Demon - fast reply
        if context.get("reply_time", float('inf')) < 2.0:
            ach = self.unlock("speed_demon")
            if ach:
                newly_unlocked.append(ach)
        
        # Marathon - 30+ minutes
        if context.get("session_minutes", 0) >= 30:
            ach = self.unlock("marathon")
            if ach:
                newly_unlocked.append(ach)
        
        # Wordsmith - 1000+ words
        if context.get("total_words", 0) >= 1000:
            ach = self.unlock("wordsmith")
            if ach:
                newly_unlocked.append(ach)
        
        # Bookworm - 5 bookmarks
        if context.get("bookmark_count", 0) >= 5:
            ach = self.unlock("bookworm")
            if ach:
                newly_unlocked.append(ach)
        
        # Commander - 10 commands
        if context.get("command"):
            self.commands_used.add(context["command"])
        if len(self.commands_used) >= 10:
            ach = self.unlock("commander")
            if ach:
                newly_unlocked.append(ach)
        
        # Mood Master - 5 moods
        if context.get("mood"):
            self.moods_experienced.add(context["mood"])
        if len(self.moods_experienced) >= 5:
            ach = self.unlock("mood_master")
            if ach:
                newly_unlocked.append(ach)
        
        # Nostalgia - retro theme
        if context.get("current_theme") == "retro":
            ach = self.unlock("nostalgia")
            if ach:
                newly_unlocked.append(ach)
        
        # Zen Master - zen theme for 10 minutes
        if context.get("current_theme") == "zen":
            if self.zen_start_time is None:
                self.zen_start_time = time.time()
            elif time.time() - self.zen_start_time >= 600:
                ach = self.unlock("zen_master")
                if ach:
                    newly_unlocked.append(ach)
        else:
            self.zen_start_time = None
        
        # Hacker - sudo easter egg
        if context.get("easter_egg_id") == "sudo":
            ach = self.unlock("hacker")
            if ach:
                newly_unlocked.append(ach)
        
        # Birthday
        if context.get("easter_egg_id") == "birthday":
            ach = self.unlock("birthday")
            if ach:
                newly_unlocked.append(ach)
        
        return newly_unlocked
    
    def get_unlocked(self) -> List[Achievement]:
        """Get list of unlocked achievements"""
        return [ACHIEVEMENTS[id] for id in self.unlocked if id in ACHIEVEMENTS]
    
    def get_locked(self) -> List[Achievement]:
        """Get list of locked (non-secret) achievements"""
        return [
            ach for id, ach in ACHIEVEMENTS.items() 
            if id not in self.unlocked and not ach.secret
        ]
    
    def get_progress(self) -> str:
        """Get progress string"""
        total = len([a for a in ACHIEVEMENTS.values() if not a.secret])
        unlocked = len([id for id in self.unlocked if not ACHIEVEMENTS.get(id, Achievement("", "", "", "", True)).secret])
        return f"{unlocked}/{total}"
    
    def get_display_string(self) -> str:
        """Get emoji string of unlocked achievements"""
        if not self.unlocked:
            return "No achievements yet"
        
        emojis = [ACHIEVEMENTS[id].emoji for id in self.unlocked if id in ACHIEVEMENTS]
        return " ".join(emojis[:10])  # Show max 10


# Global achievement tracker
achievement_tracker = AchievementTracker()


def get_achievement_tracker() -> AchievementTracker:
    """Get the global achievement tracker"""
    return achievement_tracker
