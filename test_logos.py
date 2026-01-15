
def print_logo(name, logo):
    print(f"\n[{name.upper()}]")
    print("-" * 60)
    lines = logo.split('\n')
    max_w = 0
    for line in lines:
        if line.strip():
            print(line)
            max_w = max(max_w, len(line))
    print("-" * 60)
    print(f"Max Width: {max_w}")

# ---------------------------------------------------------
# NEW HACKER LOGO
# Goal: "NOVAMIND" full visibility, blocky cyber, green matrix style.
# ---------------------------------------------------------

# Using a standard "ANSI Shadow" or comparable block font that fits 80 chars
# NOVAMIND in ANSI Shadow is usually approx 80-90 chars wide, might be tight.
# Let's try a smaller "Slant" or custom blocky design.

HACKER_LOGO_FINAL = r"""
    ΓòöΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòù
    Γòæ   _   _   ___   _   _   _     __  __   ___   _   _   ____      Γòæ
    Γòæ  | \ | | / _ \ | | | | / \   |  \/  | |_ _| | \ | ||  _ \      Γòæ
    Γòæ  |  \| || | | || | | |/ _ \  | |\/| |  | |  |  \| || | | |     Γòæ
    Γòæ  | |\  || |_| | \ V // ___ \ | |  | |  | |  | |\  || |_| |     Γòæ
    Γòæ  |_| \_| \___/   \_//_/   \_\|_|  |_| |___| |_| \_||____/      Γòæ
    Γòæ                                                                  Γòæ
    Γòæ               > SYSTEM_ROOT_ACCESS: GRANTED                      Γòæ
    ΓòÜΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓò¥
"""
# Note: I used explicit Unicode box characters ΓòöΓòÉ etc exactly as in the original file to match style.
# The text is "NOVAMIND" using standard small-caps or similar.

# ---------------------------------------------------------
# NEW OCEAN LOGO
# Goal: Text-based, bold, tech-inspired, sharp wave-like edges.
# ---------------------------------------------------------

OCEAN_LOGO_FINAL = r"""
        /\      /\     N  O  V  A  M  I  N  D     /\      /\
       /  \    /  \    ____________________    /  \    /  \
      / /\ \  / /\ \  |_   _|  ____  |  __ \  / /\ \  / /\ \
     / /  \ \/ /  \ \   | | | |____| | |  | |/ /  \ \/ /  \ \
    / /    \  /    \ \  | | |  ____  | |  | / /    \  /    \ \
   / /      \/      \ \_| |_| |    | | |__|/ /      \/      \ \
  / /                \____/ |_|    |_|____/ /                \ \
  \/                 f l u i d   s y s t e m                  \/
"""
# This uses "ITA" style letters roughly? No, just placeholder ASCII text.
# The user wants "BOLD TYPOGRAPHY".
# Let's try to construct a custom bold font for "NOVAMIND".

OCEAN_LOGO_BOLD = r"""
     /\                                                  /\
    /  \   |\   |  ___  \  /   /\   |\  /|  |  |\  |  |  \   /  \
   / /\ \  | \  | |   |  \/   /__\  | \/ |  |  | \ |  |   \ / /\ \
   \ \/ /  |  \ | |   |  /\  /    \ |    |  |  |  \|  |   / \ \/ /
    \  /   |   \| |___| /  \ |    | |    |  |  |   |  |__/   \  /
     \/                                                       \/
            >  D E E P   O C E A N   S Y S T E M S  <
"""
# That's a bit scattered.

if __name__ == "__main__":
    print_logo("hacker_final", HACKER_LOGO_FINAL)
    print_logo("ocean_final", OCEAN_LOGO_FINAL)
    print_logo("ocean_bold", OCEAN_LOGO_BOLD)
