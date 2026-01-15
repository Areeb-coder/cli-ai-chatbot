
candidate_3 = r"""
.__   __.   ______   ____    ____  ___      .___  ___.  __  .__   __.  _______ 
|  \ |  |  /  __  \  \   \  /   / /   \     |   \/   | |  | |  \ |  | |       \
|   \|  | |  |  |  |  \   \/   / /  ^  \    |  \  /  | |  | |   \|  | |  .--.  |
|  . `  | |  |  |  |   \      / /  /_\  \   |  |\/|  | |  | |  . `  | |  |  |  |
|  |\   | |  `--'  |    \    / /  _____  \  |  |  |  | |  | |  |\   | |  '--'  |
|__| \__|  \______/      \__/ /__/     \__\ |__|  |__| |__| |__| \__| |_______/
"""

lines = [l for l in candidate_3.split('\n') if l.strip()]
if lines:
    width = max(len(l) for l in lines)
    print(f"Candidate 3 width: {width}")

candidate_small = r"""
 _   _  _____  _   _   ___   __  __  _____  _   _  ____  
| \ | ||  _  || | | | / _ \ |  \/  ||_   _|| \ | ||  _ \ 
|  \| || | | || | | |/ /_\ \| |\/| |  | |  |  \| || | | |
| . ` || | | || | | ||  _  || |  | |  | |  | . ` || |_| |
| |\  |\ \_/ /\ \_/ /| | | || |  | | _| |_ | |\  || | | |
|_| \_| \___/  \___/ |_| |_||_|  |_||_____||_| \_||_| |_|
"""
lines_small = [l for l in candidate_small.split('\n') if l.strip()]
if lines_small:
    width_small = max(len(l) for l in lines_small.splitlines())
    print(f"Candidate Small width: {width_small}")

