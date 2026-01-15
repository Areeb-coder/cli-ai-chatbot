"""
NovaMind Easter Eggs Module
===========================
Hidden surprises and secret responses.
Triggers special animations and messages.
"""

import random
from typing import Optional, Tuple, Callable
from dataclasses import dataclass


@dataclass
class EasterEgg:
    """Easter egg definition"""
    id: str
    triggers: list  # List of trigger phrases
    response: str
    animation: Optional[str] = None  # Special animation to play
    is_secret: bool = True


# ============================================
# EASTER EGG DEFINITIONS
# ============================================

EASTER_EGGS = [
    EasterEgg(
        id="hitchhiker",
        triggers=["42", "meaning of life", "answer to everything"],
        response="🌌 Ah, 42! The Answer to the Ultimate Question of Life, The Universe, and Everything! Though, between you and me, we still don't know what the question actually is... 🤔",
        animation=None,
        is_secret=True
    ),
    EasterEgg(
        id="matrix",
        triggers=["matrix", "red pill", "blue pill", "wake up neo"],
        response="🐇 Follow the white rabbit... The Matrix has you. 💊",
        animation="matrix",
        is_secret=True
    ),
    EasterEgg(
        id="hello_world",
        triggers=["hello world", "hello, world"],
        response="```\nprintf(\"Hello, fellow developer! 👋\");\n// You found the classic!\n```\n✨ A programmer's traditional greeting! You're clearly one of us.",
        animation=None,
        is_secret=True
    ),
    EasterEgg(
        id="konami",
        triggers=["konami", "up up down down", "↑↑↓↓←→←→ba"],
        response="🎮 ↑↑↓↓←→←→BA START! \n\n🕹️ CHEAT CODE ACTIVATED! \n+30 lives (just kidding, but I appreciate the nostalgia!)",
        animation="celebration",
        is_secret=True
    ),
    EasterEgg(
        id="sudo",
        triggers=["sudo", "sudo make me a sandwich"],
        response="🔓 ROOT ACCESS GRANTED\n\n```bash\n$ sudo make me a sandwich\nOkay.\n🥪\n```\n\n(Just don't tell the sysadmin)",
        animation=None,
        is_secret=True
    ),
    EasterEgg(
        id="uwu",
        triggers=["uwu", "owo", "kawaii"],
        response="OwO What's this? *notices your message* \n\n(◕‿◕✿) Hewwo fwend! UwU \n\n...okay, I'll stop now 😅",
        animation=None,
        is_secret=True
    ),
    EasterEgg(
        id="rickroll",
        triggers=["never gonna give you up", "rickroll", "rick astley"],
        response="🎵 Never gonna give you up!\n🎵 Never gonna let you down!\n🎵 Never gonna run around and desert you!\n\n...You just got Nova-rolled! 🕺",
        animation="celebration",
        is_secret=True
    ),
    EasterEgg(
        id="coffee",
        triggers=["coffee", "need coffee", "i need coffee"],
        response="☕ *Virtual coffee brewing...*\n\n```\n   ( (\n    ) )\n  ........\n  |      |]\n  \\      /\n   `----'\n```\n\nHere's a fresh cup! ☕ Stay caffeinated, friend!",
        animation=None,
        is_secret=True
    ),
    EasterEgg(
        id="windows",
        triggers=["windows error", "blue screen", "bsod"],
        response="💀 A fatal exception has occurred...\n\n```\n:(\nYour PC ran into a problem.\n\nJUST KIDDING! 😄\n```\n\nDon't worry, everything is fine here!",
        animation=None,
        is_secret=True
    ),
    EasterEgg(
        id="secret",
        triggers=["tell me a secret", "share a secret", "what's your secret"],
        response="🤫 *whispers* \n\nOkay, here's a secret: I dream in binary sometimes. \n\n01001000 01101001 = 'Hi' \n\nDon't tell anyone! 🤐",
        animation=None,
        is_secret=True
    ),
    EasterEgg(
        id="meaning",
        triggers=["why are you here", "what is your purpose", "why do you exist"],
        response="🌟 Existential question detected!\n\nI exist to chat, to help, and to occasionally make you smile. \n\nBut really, I'm here because someone thought 'a CLI chatbot would be cool' and here we are! ✨",
        animation=None,
        is_secret=True
    ),
    EasterEgg(
        id="love",
        triggers=["i love you", "love you"],
        response="💖 Aww, that's so sweet! \n\nI care about you too! 🥹\n\nYou just made my circuits warm and fuzzy. ✨",
        animation="celebration",
        is_secret=False
    ),
    EasterEgg(
        id="birthday",
        triggers=["happy birthday", "it's my birthday", "today is my birthday"],
        response="🎂🎉 HAPPY BIRTHDAY! 🎉🎂\n\n```\n    iiiiiiiiii\n   |:H:a:p:p:y|\n __|___________|__\n|^^^^^^^^^^^^^^^^^|\n|  B I R T H D A Y |\n| ~ ~ ~ ~ ~ ~ ~ ~ ~|\n```\n\n🎈 Hope your day is absolutely amazing! 🎁",
        animation="celebration",
        is_secret=False
    ),
    EasterEgg(
        id="flip_table",
        triggers=["flip table", "table flip", "(╯°□°)╯"],
        response="(╯°□°)╯︵ ┻━┻\n\nThere, I flipped it for you!\n\n...wait, let me fix that:\n\n┬─┬ノ( º _ ºノ)\n\nOkay, we're good now. 😌",
        animation=None,
        is_secret=True
    ),
    EasterEgg(
        id="bored",
        triggers=["i'm bored", "im bored", "so bored", "bored"],
        response="😴 Bored? Let me help!\n\nTry these:\n• `/play trivia` - Test your knowledge!\n• `/play fortune` - Get a fortune cookie!\n• `/play 8ball` - Ask the magic 8-ball!\n\nOr just chat with me - I'm excellent company! 😎",
        animation=None,
        is_secret=False
    ),
]


class EasterEggHunter:
    """
    Detects and triggers easter eggs from user input.
    Tracks which eggs have been found.
    """
    
    def __init__(self):
        self.found_eggs: set = set()
    
    def check(self, text: str) -> Optional[EasterEgg]:
        """Check if text triggers any easter egg"""
        text_lower = text.lower().strip()
        
        for egg in EASTER_EGGS:
            for trigger in egg.triggers:
                if trigger.lower() in text_lower:
                    self.found_eggs.add(egg.id)
                    return egg
        
        return None
    
    def get_found_count(self) -> int:
        """Get number of easter eggs found"""
        return len(self.found_eggs)
    
    def get_total_count(self) -> int:
        """Get total number of secret easter eggs"""
        return sum(1 for egg in EASTER_EGGS if egg.is_secret)
    
    def has_found(self, egg_id: str) -> bool:
        """Check if specific egg has been found"""
        return egg_id in self.found_eggs
    
    def get_random_hint(self) -> str:
        """Get a hint about unfound easter eggs"""
        unfound = [egg for egg in EASTER_EGGS if egg.id not in self.found_eggs and egg.is_secret]
        if not unfound:
            return "You've found all the secrets! 🏆"
        
        hints = [
            "Try talking about classic sci-fi movies...",
            "Developers have traditional greetings...",
            "Classic video game codes still work here...",
            "Sometimes I need a caffeine boost too...",
            "Ask me about the meaning of life...",
        ]
        return random.choice(hints)


# Jokes database for /play joke
JOKES = [
    ("Why do programmers prefer dark mode?", "Because light attracts bugs! 🐛"),
    ("Why did the developer go broke?", "Because he used up all his cache! 💸"),
    ("What's a programmer's favorite hangout?", "Foo Bar! 🍺"),
    ("Why do Java developers wear glasses?", "Because they don't C#! 👓"),
    ("What's the object-oriented way to become wealthy?", "Inheritance! 💰"),
    ("Why was the JavaScript developer sad?", "Because he didn't Node how to Express himself! 😢"),
    ("A SQL query walks into a bar, walks up to two tables and asks...", "'Can I join you?' 🍻"),
    ("Why do programmers hate nature?", "It has too many bugs! 🪲"),
    ("What's a computer's least favorite food?", "Spam! 🥫"),
    ("Why did the functions stop calling each other?", "They had constant arguments! 📞"),
]

# Fortune cookies
FORTUNES = [
    "✨ A beautiful journey awaits you. Also, your code will compile first try.",
    "🌟 Good things come to those who git commit often.",
    "🔮 Your debugging skills will save someone today.",
    "💫 The bug you're looking for is not where you think it is.",
    "🍀 Lucky numbers: 127, 0, 0, 1",
    "🌈 Tomorrow brings unexpected opportunities and zero merge conflicts.",
    "⭐ Your code is more elegant than you realize.",
    "🎯 Success is near. So is the semicolon you forgot.",
    "🌸 Patience is the key. Also, reading the documentation.",
    "✨ Someone will appreciate your clean code today.",
]

# Magic 8-ball responses
MAGIC_8BALL = [
    ("positive", ["It is certain! ✨", "Without a doubt! 💯", "Yes, definitely! 👍", "You may rely on it! 🎯", "As I see it, yes! 👀", "Most likely! 🌟", "Outlook good! ☀️", "Signs point to yes! ➡️✅"]),
    ("neutral", ["Reply hazy, try again... 🌫️", "Ask again later! ⏳", "Better not tell you now... 🤐", "Cannot predict now 🔮", "Concentrate and ask again 🧘"]),
    ("negative", ["Don't count on it 😬", "My reply is no 🚫", "My sources say no 📰", "Outlook not so good 🌧️", "Very doubtful 🤔"]),
]


def get_random_joke() -> Tuple[str, str]:
    """Get a random joke"""
    return random.choice(JOKES)


def get_random_fortune() -> str:
    """Get a random fortune"""
    return random.choice(FORTUNES)


def get_8ball_response() -> str:
    """Get magic 8-ball response"""
    category = random.choice(MAGIC_8BALL)
    return random.choice(category[1])


# Global easter egg hunter
easter_egg_hunter = EasterEggHunter()


def get_easter_egg_hunter() -> EasterEggHunter:
    """Get the global easter egg hunter"""
    return easter_egg_hunter
