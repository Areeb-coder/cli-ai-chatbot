"""
NovaMind Utilities Module
=========================
Helper functions and shared utilities.
"""

import os
import sys
import shutil
import json
from datetime import datetime
from typing import Optional


def get_terminal_size() -> tuple:
    """Get terminal width and height"""
    size = shutil.get_terminal_size()
    return size.columns, size.lines


def is_emoji_supported() -> bool:
    """Check if terminal likely supports emoji"""
    # Windows Terminal and modern terminals support emoji
    if os.name == 'nt':
        # Check for Windows Terminal
        return 'WT_SESSION' in os.environ or 'TERM_PROGRAM' in os.environ
    return True


def safe_print(text: str, fallback: str = "") -> str:
    """Safely print text with emoji fallback"""
    try:
        print(text)
        return text
    except UnicodeEncodeError:
        print(fallback or text.encode('ascii', 'ignore').decode())
        return fallback


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate text to max length with suffix"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def wrap_text(text: str, width: int) -> list:
    """Wrap text to specified width"""
    words = text.split()
    lines = []
    current_line = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + 1 <= width:
            current_line.append(word)
            current_length += len(word) + 1
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
            current_length = len(word)
    
    if current_line:
        lines.append(" ".join(current_line))
    
    return lines


def format_timestamp(timestamp: float) -> str:
    """Format timestamp to readable string"""
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime("%H:%M")


def format_date(timestamp: float) -> str:
    """Format timestamp to date string"""
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime("%Y-%m-%d %H:%M")


def save_to_file(content: str, filename: str, directory: str = ".") -> bool:
    """Save content to file"""
    try:
        filepath = os.path.join(directory, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception:
        return False


def save_json(data: dict, filename: str, directory: str = ".") -> bool:
    """Save data as JSON file"""
    try:
        filepath = os.path.join(directory, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False


def load_env_file(filepath: str = ".env") -> dict:
    """Load environment variables from .env file"""
    env_vars = {}
    
    if not os.path.exists(filepath):
        return env_vars
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
                    os.environ[key.strip()] = value.strip()
    except Exception:
        pass
    
    return env_vars


def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def is_question(text: str) -> bool:
    """Check if text is a question"""
    question_words = ['what', 'why', 'how', 'when', 'where', 'who', 'which', 'whose', 'whom']
    text_lower = text.lower().strip()
    
    if text_lower.endswith('?'):
        return True
    
    for word in question_words:
        if text_lower.startswith(word + ' '):
            return True
    
    return False


def sanitize_input(text: str) -> str:
    """Sanitize user input"""
    # Remove control characters but keep newlines
    cleaned = ''.join(
        char for char in text 
        if char == '\n' or (ord(char) >= 32 and ord(char) < 127) or ord(char) > 127
    )
    return cleaned.strip()


class Colors:
    """ANSI color codes for fallback when Rich isn't available"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'


def get_exports_directory() -> str:
    """Get or create exports directory"""
    exports_dir = os.path.join(os.getcwd(), "exports")
    if not os.path.exists(exports_dir):
        os.makedirs(exports_dir)
    return exports_dir
