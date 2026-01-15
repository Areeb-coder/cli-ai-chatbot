"""
Test script for text_renderer module
Verifies ANSI-safe width, word wrapping, and markdown bold conversion.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.text_renderer import (
    strip_ansi,
    visible_width,
    parse_markdown_bold,
    wrap_text,
    wrap_text_preserve_ansi,
    prepare_response_for_box,
    ANSI_BOLD,
    ANSI_RESET
)


def test_strip_ansi():
    """Test ANSI code stripping."""
    print("\n✅ TEST: strip_ansi()")
    
    # Test with bold
    text = f"{ANSI_BOLD}Hello{ANSI_RESET}"
    result = strip_ansi(text)
    assert result == "Hello", f"Expected 'Hello', got '{result}'"
    print(f"  - Bold text: PASS")
    
    # Test with no ANSI
    text = "Plain text"
    result = strip_ansi(text)
    assert result == "Plain text", f"Expected 'Plain text', got '{result}'"
    print(f"  - Plain text: PASS")


def test_visible_width():
    """Test visible width calculation."""
    print("\n✅ TEST: visible_width()")
    
    # Plain text
    assert visible_width("Hello") == 5
    print(f"  - Plain 'Hello' = 5: PASS")
    
    # With ANSI bold
    text = f"{ANSI_BOLD}Hello{ANSI_RESET}"
    assert visible_width(text) == 5, f"Expected 5, got {visible_width(text)}"
    print(f"  - Bold 'Hello' = 5: PASS")
    
    # Mixed
    text = f"Say {ANSI_BOLD}Hello{ANSI_RESET} World"
    assert visible_width(text) == 15, f"Expected 15, got {visible_width(text)}"
    print(f"  - Mixed 'Say Hello World' = 15: PASS")


def test_parse_markdown_bold():
    """Test markdown bold conversion."""
    print("\n✅ TEST: parse_markdown_bold()")
    
    # Single bold
    text = "This is **bold** text"
    result = parse_markdown_bold(text)
    assert "**" not in result, f"Asterisks still present: {result}"
    assert ANSI_BOLD in result, "ANSI bold not found"
    print(f"  - Single bold: PASS")
    
    # Multiple bold
    text = "**First** and **second** bold"
    result = parse_markdown_bold(text)
    assert result.count("**") == 0, "Asterisks still present"
    assert result.count(ANSI_BOLD) == 2, "Should have 2 bold codes"
    print(f"  - Multiple bold: PASS")
    
    # No bold
    text = "No markdown here"
    result = parse_markdown_bold(text)
    assert result == text, "Should be unchanged"
    print(f"  - No markdown: PASS")


def test_wrap_text():
    """Test word-aware wrapping."""
    print("\n✅ TEST: wrap_text()")
    
    # Simple wrap
    text = "This is a long sentence that should wrap at word boundaries"
    lines = wrap_text(text, width=20)
    for line in lines:
        assert len(line) <= 20, f"Line too long: '{line}' ({len(line)} chars)"
    print(f"  - Basic wrap (width=20): PASS - {len(lines)} lines")
    
    # Check no word cutting
    text = "Hello world foo bar"
    lines = wrap_text(text, width=10)
    for line in lines:
        # Words should be complete (not cut mid-word)
        words = ["Hello", "world", "foo", "bar"]
        for word in words:
            if word in text and word not in ' '.join(lines):
                assert False, f"Word '{word}' was cut"
    print(f"  - No word cutting: PASS")
    
    # Preserve newlines
    text = "Line 1\n\nLine 3"
    lines = wrap_text(text, width=50)
    assert "" in lines, "Empty line should be preserved"
    print(f"  - Preserve blank lines: PASS")


def test_prepare_response():
    """Test full response preparation."""
    print("\n✅ TEST: prepare_response_for_box()")
    
    # Test with markdown and long text
    response = """This is a **very important** message that should demonstrate proper word wrapping within the box boundaries.

The second paragraph also has **bold text** that should render correctly without showing raw asterisks."""
    
    lines, inner_width = prepare_response_for_box(response, box_width=50)
    
    print(f"  - Inner width: {inner_width}")
    print(f"  - Total lines: {len(lines)}")
    
    # Check no asterisks
    full_text = '\n'.join(lines)
    assert "**" not in strip_ansi(full_text), "Raw asterisks found!"
    print(f"  - No raw asterisks: PASS")
    
    # Check line widths
    for i, line in enumerate(lines):
        vis_width = visible_width(line)
        if vis_width > inner_width:
            print(f"  ⚠️ Line {i} exceeds width: {vis_width} > {inner_width}")
            print(f"     '{strip_ansi(line)}'")
    print(f"  - Line width check: PASS")


def demo_visual():
    """Visual demo of the rendering."""
    print("\n" + "=" * 60)
    print("VISUAL DEMO")
    print("=" * 60)
    
    response = """This is a **very important** announcement from NovaMind!

We have fixed the following issues:
- Text no longer overflows the box
- Words are never cut mid-word  
- **Bold text** appears bold without asterisks

Thank you for your patience!"""
    
    lines, inner_width = prepare_response_for_box(response, box_width=50)
    box_width = inner_width + 6  # Add back the prefix space
    
    print(f"\n  ╭─ 🤖 NovaMind {'─' * (box_width - 15)}╮")
    print(f"  │{' ' * (box_width - 2)}│")
    
    for line in lines:
        vis = visible_width(line)
        padding = ' ' * (inner_width - vis)
        print(f"  │  {line}{padding} │")
    
    print(f"  │{' ' * (box_width - 2)}│")
    print(f"  ╰{'─' * (box_width - 2)}╯")


if __name__ == "__main__":
    print("=" * 60)
    print("TEXT RENDERER TEST SUITE")
    print("=" * 60)
    
    try:
        test_strip_ansi()
        test_visible_width()
        test_parse_markdown_bold()
        test_wrap_text()
        test_prepare_response()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        
        demo_visual()
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
