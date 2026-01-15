"""
NovaMind Output Sanitization Pipeline
=====================================
Strict cleaning stage to prevent internal model content from reaching the user.
"""

import re
from typing import List

# Forbidden phrases that indicate internal reasoning or system text
FORBIDDEN_PHRASES = [
    "The user is asking",
    "System:",
    "Developer:",
    "Instruction:",
    "You are ChatGPT",
    "You are an AI",
    "<|im_start|>",
    "<|im_end|>",
    "----",
    "[SUGGESTION]",
    "[THOUGHT]",
    "[DEBUG]"
]

# Patterns for chain of thought or internal reasoning key phrases
REASONING_PATTERNS = [
    r"(?i)^reasoning:",
    r"(?i)^analysis:",
    r"(?i)^thought:",
    r"(?i)^step-by-step:",
    r"(?i)^explanation:",
    r"(?i)^scratchpad:"
]

def sanitize_output(text: str) -> str:
    """
    Main sanitization pipeline function.
    
    Pipeline:
    1. Strip known special tokens
    2. Filter out internal reasoning/system lines
    3. Extract final answer if chain-of-thought is detected
    4. Clean formatting
    """
    if not text:
        return ""
        
    cleaned = text
    
    # 1. SPECIAL TOKEN REMOVAL (Regex based for better coverage)
    # Remove <|im_start|>role and <|im_end|>
    cleaned = re.sub(r"<\|im_start\|>\s*\w+\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"<\|im_end\|>", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"<\|im_sep\|>", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"<s>|</s>", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\[/?INST\]", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"<\/?s>", "", cleaned, flags=re.IGNORECASE)
        
    # 2. LINE-BASED FILTERING
    lines = cleaned.split('\n')
    filtered_lines = []
    
    inside_code_block = False
    
    for line in lines:
        stripped_line = line.strip()
        
        # Track code blocks - we generally preserve content inside code blocks
        if stripped_line.startswith("```"):
            inside_code_block = not inside_code_block
            filtered_lines.append(line)
            continue
            
        if inside_code_block:
            filtered_lines.append(line)
            continue
            
        # Skip empty lines (we'll handle spacing later)
        if not stripped_line:
            filtered_lines.append(line)
            continue
            
        # CHECK FOR FORBIDDEN PHRASES
        is_forbidden = False
        for phrase in FORBIDDEN_PHRASES:
            # Check if line *starts with* or *strongly contains* scaffolding
            if phrase.lower() in stripped_line.lower():
                # Context check: "Assistant:" at start of line is bad. 
                # Strict start check for roles or forbidden phrases
                if stripped_line.lower().startswith(phrase.lower()) or \
                   phrase in ["<|im_start|>", "<|im_end|>", "[DEBUG]", "[THOUGHT]"]:
                    is_forbidden = True
                    break
        
        if is_forbidden:
            continue
            
        # CHECK FOR ROLE PREFIXES (e.g. "NovaMind: Hello")
        # Handles "Assistant: ", "Assistant", "AI: "
        role_match = re.match(r"^(System|Assistant|User|NovaMind|AI|Model)(:\s*|\s*$)", stripped_line, re.IGNORECASE)
        if role_match:
            # Remove the prefix but keep the content
            content = line[role_match.end():]
            if content.strip():
                filtered_lines.append(content)
            # If content is empty/whitespace (e.g. just "Assistant"), we drop the line 
            # (which effectively happens by not appending if content.strip() is empty)
            continue
            
        filtered_lines.append(line)
        
    cleaned = '\n'.join(filtered_lines)
    
    # 3. CHAIN OF THOUGHT EXTRACTION
    # If we see "Final Answer:" or similar, we might want to discard everything before it
    # IF and ONLY IF we detect substantial reasoning text before it.
    
    # Simple heuristic: If "Final Answer:" exists, take everything after it.
    final_answer_match = re.search(r"(?i)^final answer:\s*", cleaned, re.MULTILINE)
    if final_answer_match:
        cleaned = cleaned[final_answer_match.end():]
        
    return cleaned.strip()

def unit_test_sanitizer():
    """Run verification tests on the sanitizer"""
    test_cases = [
        (
            "System: You are a helpful assistant.\nUser: Hi\nAssistant: Hello there!", 
            "Hi\nHello there!"
        ),
        (
            "The user is asking for python code.\nHere it is:\n```python\nprint('hi')\n```", 
            "Here it is:\n```python\nprint('hi')\n```"
        ),
        (
            "<|im_start|>assistant\nI can help with that.", 
            "I can help with that."
        ),
        (
            "Reasoning: The user wants X.\nFinal Answer: The answer is X.", 
            "The answer is X."
        )
    ]
    
    print("Running Sanitizer Unit Tests...")
    failures = 0
    for input_text, expected in test_cases:
        result = sanitize_output(input_text)
        if result.strip() != expected.strip():
            print(f"[FAIL] Input: {input_text[:20]}...\nExpected: {expected}\nGot: {result}")
            failures += 1
            
    if failures == 0:
        print("All Tests Passed!")
    else:
        print(f"{failures} Tests Failed.")

if __name__ == "__main__":
    unit_test_sanitizer()
