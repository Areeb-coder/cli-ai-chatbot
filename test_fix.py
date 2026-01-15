
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
import re

def test_fix():
    # The problem string (2 repetitions)
    text = "Did you know that a day on Venus is longer than a year on Venus? 🌍🪐 A single rotation takes about 243 Earth days, while its orbit around the Sun takes only about 225 Earth days Did you know that a day on Venus is longer than a year on Venus? 🌍🪐 A single rotation takes about 243 Earth days, while its orbit around the Sun takes only about 225 Earth days"
    
    # Try to find repeated patterns of significant length (e.g., > 20 chars)
    # We use non-greedy matching for the content, but greedy for the repetition
    match = re.search(r'(.{20,}?)\1+', text, re.DOTALL)
    
    # Proposed "Halves" logic
    words = text.split()
    if len(words) > 10:
        half = len(words) // 2
        # part1 covers first half of words
        part1_words = words[:half]
        # part2 covers second half of words
        part2_words = words[half:] 
        
        # If odd number of words, lengths differ by 1.
        # Let's align them.
        min_len = min(len(part1_words), len(part2_words))
        
        s1 = ' '.join(part1_words[:min_len]).lower()
        s2 = ' '.join(part2_words[:min_len]).lower()
        
        print(f"S1 ({len(s1)}): {s1[:30]}...")
        print(f"S2 ({len(s2)}): {s2[:30]}...")
        
        # Use a tolerance or prefix match
        if len(s1) > 20 and s1 == s2:
             print("SUCCESS: Exact match detected in halves!")
        elif len(s1) > 20 and s1[:min(len(s1), 100)] == s2[:min(len(s2), 100)]:
             print("SUCCESS: Prefix match detected in halves!")
        else:
             print("FAILURE: No match in halves.")
             # Debug why
             # find first diff
             for i in range(min(len(s1), len(s2))):
                 if s1[i] != s2[i]:
                     print(f"Diff at {i}: '{s1[i]}' vs '{s2[i]}'")
                     print(f"Context: {s1[i-10:i+10]}")
                     break

if __name__ == "__main__":
    test_fix()
