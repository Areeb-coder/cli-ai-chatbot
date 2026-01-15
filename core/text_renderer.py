"""
NovaMind Text Renderer Module - FIXED VERSION
"""

import re
import shutil
import textwrap
from typing import List, Tuple
from rich.cells import cell_len

ANSI_ESCAPE_PATTERN = re.compile(r'\x1b\[[0-9;]*m')
ANSI_BOLD = '\x1b[1m'
ANSI_RESET = '\x1b[0m'

# Tokens to strip - ChatML, Llama/Mistral, etc.
# Pipe characters escaped as chr(124), angle brackets as chr(60)/chr(62)
_PIPE = chr(124)
_LT = chr(60)
_GT = chr(62)

TOKENS_TO_STRIP = [
    f'{_LT}{_PIPE}im_start{_PIPE}{_GT}system',
    f'{_LT}{_PIPE}im_start{_PIPE}{_GT}user', 
    f'{_LT}{_PIPE}im_start{_PIPE}{_GT}assistant',
    f'{_LT}{_PIPE}im_start{_PIPE}{_GT}',
    f'{_LT}{_PIPE}im_end{_PIPE}{_GT}',
    f'{_LT}{_PIPE}im_sep{_PIPE}{_GT}',
    '[INST]',
    '[/INST]',
    f'{_LT}{_LT}SYS{_GT}{_GT}',
    f'{_LT}{_LT}/SYS{_GT}{_GT}',
    f'{_LT}s{_GT}',
    f'{_LT}/s{_GT}',
    f'{_LT}{_PIPE}end{_PIPE}{_GT}',
    f'{_LT}{_PIPE}assistant{_PIPE}{_GT}',
]


def sanitize_ai_response(text):
    """
    MANDATORY sanitization - strips all model tokens from response.
    
    THIS FUNCTION MUST BE CALLED:
    1. After AI generation
    2. Before ANY rendering
    3. For ALL output paths (typing animation AND focus mode)
    
    NO CODE PATH MAY BYPASS THIS FUNCTION.
    """
    if not text:
        return text
    
    result = text
    for token in TOKENS_TO_STRIP:
        result = result.replace(token, '')
    
    # Clean up multiple spaces/newlines that may result from removal
    result = re.sub(r'\n{3,}', '\n\n', result)
    result = re.sub(r' {2,}', ' ', result)
    
    return result.strip()


def strip_ansi(text):
    """Remove all ANSI escape codes from text."""
    return ANSI_ESCAPE_PATTERN.sub('', text)


def visible_width(text):
    """
    Calculate visible width of text (excluding ANSI codes).
    Uses rich.cells.cell_len to correctly handle emojis and wide characters.
    """
    return cell_len(strip_ansi(text))


MARKDOWN_BOLD_PATTERN = re.compile(r'\*\*(.+?)\*\*')


def parse_markdown_bold(text):
    """Convert markdown **bold** to terminal ANSI bold."""
    def replace_bold(match):
        content = match.group(1)
        return f'{ANSI_BOLD}{content}{ANSI_RESET}'
    return MARKDOWN_BOLD_PATTERN.sub(replace_bold, text)


def wrap_text(text, width):
    """Word-aware text wrapping."""
    if width <= 0:
        width = 40
    
    lines = []
    paragraphs = text.split('\n')
    
    for paragraph in paragraphs:
        if not paragraph.strip():
            lines.append('')
            continue
        
        wrapped = textwrap.wrap(
            paragraph,
            width=width,
            break_long_words=True,
            break_on_hyphens=True,
            replace_whitespace=False,
            drop_whitespace=True
        )
        
        if wrapped:
            lines.extend(wrapped)
        else:
            lines.append('')
    
    return lines


def wrap_text_preserve_ansi(text, width):
    """Advanced word wrapping that handles ANSI codes and wide characters."""
    if width <= 0:
        width = 40
    
    # We always use our custom logic to be safe with wide chars,
    # even if no ANSI codes are present, because python's textwrap
    # doesn't handle 'visible width' (columns) but just 'characters'.
    
    lines = []
    current_line = ''
    current_visible_width = 0
    
    paragraphs = text.split('\n')
    
    for para_idx, paragraph in enumerate(paragraphs):
        # Handle empty paragraphs (newlines)
        if not paragraph:
            if current_line:
                lines.append(current_line)
                current_line = ''
                current_visible_width = 0
            lines.append('')
            continue

        words = paragraph.split(' ')
        
        for i, word in enumerate(words):
            if not word: continue
            
            word_visible = visible_width(word)
            
            # Add space width if not the first word
            space_needed = 1 if current_visible_width > 0 else 0
            
            if current_visible_width + space_needed + word_visible <= width:
                if current_visible_width > 0:
                    current_line += ' '
                    current_visible_width += 1
                current_line += word
                current_visible_width += word_visible
            else:
                # Word doesn't fit
                if current_line:
                    lines.append(current_line)
                    current_line = ''
                    current_visible_width = 0
                
                # If word itself is longer than width, force split
                if word_visible > width:
                    remaining = word
                    while visible_width(remaining) > width:
                        break_point = _find_break_point(remaining, width)
                        chunk = remaining[:break_point]
                        lines.append(chunk)
                        remaining = remaining[break_point:]
                    current_line = remaining
                    current_visible_width = visible_width(remaining)
                else:
                    current_line = word
                    current_visible_width = word_visible
        
        if current_line:
            lines.append(current_line)
            current_line = ''
            current_visible_width = 0
            
        # Add a newline if this isn't the last paragraph?
        # text.split('\n') consumes the newlines.
        # Logic above handles explicit empty strings as blank lines.
        # But normal paragraphs just get added. 
    
    return lines


def _find_break_point(text, max_width):
    """Find where to break text for wrapping, respecting ANSI and wide chars."""
    visible_count = 0
    i = 0
    length = len(text)
    
    while i < length:
        if text[i] == '\x1b':
            match = ANSI_ESCAPE_PATTERN.match(text, i)
            if match:
                i = match.end()
                continue
        
        # Calculate width of THIS character
        char_width = cell_len(text[i])
        
        # If adding this char exceeds max_width, stop here
        if visible_count + char_width > max_width:
            break
            
        visible_count += char_width
        i += 1
    
    return i


def render_line_in_box(line, inner_width, prefix="  |  "):
    """Render a line within a box with proper padding."""
    visible = visible_width(line)
    padding_needed = max(0, inner_width - visible)
    padding = ' ' * padding_needed
    return f"{prefix}{line}{padding}"


def prepare_response_for_box(response, box_width=70, terminal_width=None):
    """
    Prepare a response for rendering inside a box.
    
    Pipeline:
    1. Parse markdown bold -> ANSI bold
    2. Calculate inner width
    3. Word-wrap text to inner width
    4. Return wrapped lines and inner width
    """
    if terminal_width is None:
        terminal_width = shutil.get_terminal_size().columns
    
    # Ensure box fits in terminal
    actual_box_width = min(box_width, terminal_width - 4)
    
    # Calculate FIXED inner width
    # 2 chars for left border "  │ ", 2 for right " │" (approx)
    # Based on main.py: "  │  " (5 chars) and " │" (2 chars)
    # Total chrome: 7
    inner_width = actual_box_width - 7
    inner_width = max(20, inner_width)
    
    processed = parse_markdown_bold(response)
    wrapped_lines = wrap_text_preserve_ansi(processed, inner_width)
    
    return wrapped_lines, inner_width


def get_default_box_width():
    """Get a reasonable default box width."""
    term_width = shutil.get_terminal_size().columns
    return min(70, term_width - 4)
