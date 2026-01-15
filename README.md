# 🤖 NovaMind - Creative CLI AI Chatbot

<p align="center">
  <b>A terminal experience that feels alive</b>
</p>

```
███╗   ██╗ ██████╗ ██╗   ██╗ █████╗ ███╗   ███╗██╗███╗   ██╗██████╗ 
████╗  ██║██╔═══██╗██║   ██║██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗
██╔██╗ ██║██║   ██║██║   ██║███████║██╔████╔██║██║██╔██╗ ██║██║  ██║
██║╚██╗██║██║   ██║╚██╗ ██╔╝██╔══██║██║╚██╔╝██║██║██║╚██╗██║██║  ██║
██║ ╚████║╚██████╔╝ ╚████╔╝ ██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██████╔╝
╚═╝  ╚═══╝ ╚═════╝   ╚═══╝  ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═════╝ 
```

---

## 📋 Table of Contents

1. [Features](#-features)
2. [Installation](#-installation)
3. [Usage Examples](#-usage-examples)
4. [Themes](#-themes)
5. [Commands](#-all-commands)
6. [Achievements](#-achievements)
7. [Easter Eggs](#-easter-eggs)
8. [Mini-Games](#-mini-games)
9. [Project Structure](#-project-structure)

---

## ✨ Features

### 🎨 Dynamic Theme System
Switch between 11 beautiful visual themes on-the-fly, each with a unique ASCII logo.

### 💬 Mood-Reactive Interface  
The UI adapts colors and typing speed based on your emotional tone.

### 🏆 Achievement System
Unlock 18 badges as you chat, explore, and discover secrets.

### 🔮 Easter Eggs
15 hidden surprises waiting to be discovered.

### 🎮 Mini-Games
Play trivia, get fortunes, ask the magic 8-ball, or hear jokes.

### 📊 Session Statistics
Track messages, words, duration, and mood journey.

### 💾 Chat Export
Save conversations as TXT, Markdown, or JSON.

### ⌨️ Typing Animation
Character-by-character output with human-like variable speed.

### 🎯 Focus Mode
Minimal animations for distraction-free work.

### 📌 Bookmarks
Save and revisit important moments in your conversation.

### ⏰ Smart Greetings
Time-aware greetings that change throughout the day.

### 🤖 Multiple AI Personalities
Switch between creative, serious, friendly, or sarcastic modes.

---

## 🚀 Installation

### Step 1: Clone/Navigate to Project

```powershell
cd "c:\Users\admin\Documents\CLI Basesd AI chatbot"
```

### Step 2: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 3: Configure API Key

Create a `.env` file with your Google Gemini API key:

```
GEMINI_API_KEY=your_api_key_here
```

### Step 4: Run NovaMind

```powershell
python main.py
```

---

## 📸 Usage Examples

### Example 1: Starting the Chatbot

**Input:**
```
python main.py
```

**Output:**
```
███╗   ██╗ ██████╗ ██╗   ██╗ █████╗ ███╗   ███╗██╗███╗   ██╗██████╗ 
████╗  ██║██╔═══██╗██║   ██║██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗
██╔██╗ ██║██║   ██║██║   ██║███████║██╔████╔██║██║██╔██╗ ██║██║  ██║
██║╚██╗██║██║   ██║╚██╗ ██╔╝██╔══██║██║╚██╔╝██║██║██║╚██╗██║██║  ██║
██║ ╚████║╚██████╔╝ ╚████╔╝ ██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██████╔╝
╚═╝  ╚═══╝ ╚═════╝   ╚═══╝  ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═════╝ 

                Your AI companion in the terminal ✨

              🌤️ Good afternoon! Hope your day is going well!

╭─ 💡 Tip ────────────────────────────────────────────────╮
│ 🎮 Type /play trivia to test your knowledge            │
╰─────────────────────────────────────────────────────────╯

  ✅ AI engine ready!

  💬 0 | 🏆 0/15 | 🎨 neon
  🌆 You > 
```

---

### Example 2: Basic Conversation

**Input:**
```
🌆 You > Hello! How are you today?
```

**Output:**
```
╭─ 👤 You ─────────────────────────────────────────────────────╮
│ Hello! How are you today?                                     │
╰───────────────────────────────────────────────────────────────╯

  ⠋ Thinking...

  ╭─ 😊 NovaMind ──────────────────────────────────────────────
  │
  │  Hey there! 👋 I'm doing great, thanks for asking! 
  │  I'm always excited to chat with someone new. How about you?
  │  What's on your mind today? ✨
  │
  ╰───────────────────────────────────────────────────────────

    ▁▃▅▇▅▃▁▃▅▇▅▃▁
```

---

### Example 3: Changing Theme

**Input:**
```
🌆 You > /theme hacker
```

**Output:**
```
  ✅ Theme changed to hacker 🖥️

  💬 2 | 🏆 1/15 | 🎨 hacker
  🖥️ You > 
```

All text now appears in Matrix-style green!

---

### Example 4: Changing AI Mode

**Input:**
```
🖥️ You > /mode sarcastic
```

**Output:**
```
  ✅ Mode set to sarcastic ✨
```

**Then asking a question:**
```
🖥️ You > What's the best programming language?
```

**Output:**
```
╭─ 🤖 NovaMind ─────────────────────────────────────────────────╮
│ Oh, you're asking *that* question? Bold move. 😏              │
│                                                                │
│ The best programming language is obviously the one you        │
│ actually know how to use without Googling every 5 minutes.    │
│                                                                │
│ But if you want a real answer - Python for readability,       │
│ JavaScript for job security (because everything breaks),      │
│ and Rust if you enjoy the compiler telling you you're wrong.  │
╰────────────────────────────────────────────────────────────────╯
```

---

### Example 5: Playing Trivia

**Input:**
```
🖥️ You > /play trivia
```

**Output:**
```
  ℹ️  Generating trivia question...

╭─ 🎯 NovaMind ─────────────────────────────────────────────────╮
│ QUESTION: What is the largest planet in our solar system?    │
│                                                                │
│ A) Saturn                                                      │
│ B) Jupiter                                                     │
│ C) Neptune                                                     │
│ D) Uranus                                                      │
│                                                                │
│ ANSWER: B) Jupiter                                             │
╰────────────────────────────────────────────────────────────────╯
```

---

### Example 6: Fortune Cookie

**Input:**
```
🌆 You > /play fortune
```

**Output:**
```
╭─ 🥠 NovaMind ─────────────────────────────────────────────────╮
│ 🥠 Your fortune:                                               │
│                                                                │
│ ✨ A beautiful journey awaits you. Also, your code will       │
│ compile first try.                                             │
╰────────────────────────────────────────────────────────────────╯
```

---

### Example 7: Magic 8-Ball

**Input:**
```
🌆 You > /play 8ball
```

**Output:**
```
  ℹ️  Ask your question, then press Enter...
  🎱 > Will I get the job?

╭─ 🎱 NovaMind ─────────────────────────────────────────────────╮
│ 🎱 The Magic 8-Ball says:                                      │
│                                                                │
│ Signs point to yes! ➡️✅                                       │
╰────────────────────────────────────────────────────────────────╯
```

---

### Example 8: Viewing Session Stats

**Input:**
```
🌆 You > /stats
```

**Output:**
```
╔═══════════════════════════════════════════════════════════════╗
║                     📊 Session Stats                          ║
╠═══════════════════════════════════════════════════════════════╣
║  💬 Messages      │ 12                                        ║
║  📝 Words         │ 347                                       ║
║  ⏱️  Duration     │ 8 minutes                                 ║
║  🏆 Achievements  │ 3                                         ║
║  🎨 Themes Used   │ 2                                         ║
║  🔮 Easter Eggs   │ 1                                         ║
╚═══════════════════════════════════════════════════════════════╝
```

---

### Example 9: Viewing Achievements

**Input:**
```
🌆 You > /achievements
```

**Output:**
```
╔═══════════════════════════════════════════════════════════════╗
║                     🏆 Achievements                           ║
╠═══════════════════════════════════════════════════════════════╣
║  Progress: 3/15                                               ║
║                                                                ║
║  🏆 Unlocked:                                                  ║
║    🌟 First Contact - Start your first conversation           ║
║    🎨 Theme Explorer - Try all available themes               ║
║    🔮 Secret Finder - Discover an easter egg                  ║
║                                                                ║
║  🔒 Locked:                                                    ║
║    ❓ Chatterbox - Send 50 messages in a session              ║
║    ❓ Night Owl - Chat after midnight                         ║
║    ❓ Wordsmith - Write over 1000 words total                 ║
║    ... and 9 more to discover!                                ║
╚═══════════════════════════════════════════════════════════════╝
```

---

### Example 10: Easter Egg - "42"

**Input:**
```
🌆 You > 42
```

**Output:**
```
╭─ 🔮 NovaMind ─────────────────────────────────────────────────╮
│ 🌌 Ah, 42! The Answer to the Ultimate Question of Life,       │
│ The Universe, and Everything! Though, between you and me,     │
│ we still don't know what the question actually is... 🤔       │
╰────────────────────────────────────────────────────────────────╯

          🎉 Achievement Unlocked!
        ╔═══════════════════════════╗
        ║  🔮 Secret Finder         ║
        ║  Discover an easter egg   ║
        ╚═══════════════════════════╝
```

---

### Example 11: Easter Egg - "Matrix"

**Input:**
```
🌆 You > matrix
```

**Output:**
```
╭─ 🔮 NovaMind ─────────────────────────────────────────────────╮
│ 🐇 Follow the white rabbit... The Matrix has you. 💊          │
╰────────────────────────────────────────────────────────────────╯

ｱ ｲ ｳ   ｴ         ｵ     ｶ ｷ         ｸ
  ｹ   ｺ     ｻ ｼ ｽ   ｾ ｿ               
ﾀ     ﾁ ﾂ         ﾃ     ﾄ ﾅ ﾆ   ﾇ     
  ﾈ ﾉ     0 1 2     3         4   5   
    6     7   8 9                      
(Matrix rain animation plays for 2 seconds)
```

---

### Example 12: Exporting Chat

**Input:**
```
🌆 You > /export md
```

**Output:**
```
  ✅ Exported to exports/novamind_chat_20260115_151030.md
```

Exported file content:
```markdown
# NovaMind Chat Export

**Date:** 2026-01-15 15:10
**Duration:** 12 minutes
**Messages:** 15

---

### **You** `14:58`

Hello! How are you today?

### **🤖 NovaMind** `14:58`

Hey there! 👋 I'm doing great, thanks for asking!
...
```

---

### Example 13: Setting Your Name

**Input:**
```
🌆 You > /name Alex
```

**Output:**
```
  ✅ Nice to meet you, Alex! 👋
```

Now messages show:
```
╭─ 👤 Alex ────────────────────────────────────────────────────╮
│ This is so cool!                                              │
╰───────────────────────────────────────────────────────────────╯
```

---

### Example 14: Bookmarking

**Input:**
```
🌆 You > /bookmark
```

**Output:**
```
  ✅ Bookmark saved! 📌
```

**Viewing bookmarks:**
```
🌆 You > /bookmarks

📚 Your Bookmarks:
  1. Hey there! 👋 I'm doing great, thanks for asking...
  2. The best programming language is obviously the one...
```

---

### Example 15: Exiting with Summary

**Input:**
```
🌆 You > /exit
```

**Output:**
```
╔══════════════════════════════════════════════════════╗
║              ✨ SESSION COMPLETE ✨                  ║
╠══════════════════════════════════════════════════════╣
║  📊 Messages Exchanged: 15                           ║
║  ⏱️  Session Duration: 12 minutes                    ║
║  💬 Words Spoken: 523                                ║
║  🏆 Achievements Unlocked: 4                         ║
╠══════════════════════════════════════════════════════╣
║  💫 Mood Journey: 😊 → 🤔 → 😄 → 🤔 → 😊             ║
╠══════════════════════════════════════════════════════╣
║  🌟 Memorable Moment:                                ║
║  "This is the coolest chatbot I've ever used!"      ║
╚══════════════════════════════════════════════════════╝

        Thanks for chatting! See you soon! 👋
```

---

## 🎨 Themes

## 🎨 Themes

| Command | Theme | Description |
|---------|-------|-------------|
| `/theme dark` | 🌑 Dark | Professional dark gray & white (Default) |
| `/theme light` | ☀️ Light | Clean, minimal white mode |
| `/theme neon` | 🌆 Neon | Cyberpunk magenta & cyan glow |
| `/theme hacker` | 🖥️ Hacker | Matrix-style green on black |
| `/theme zen` | 🧘 Zen | Calm, balanced cyan & white |
| `/theme retro` | 📺 Retro | Amber CRT nostalgia |
| `/theme ocean` | 🌊 Ocean | Deep blue waves |
| `/theme sunset` | 🌅 Sunset | Warm orange gradients |
| `/theme midnight` | 🌙 Midnight | Deep blue starry night |
| `/theme calm` | ☁️ Calm | Soft slate & cloudy gray |
| `/theme warning` | ⚠️ Warning | High contrast red alert |

---

## 📋 All Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/help` | Show all commands | `/help` |
| `/clear` | Clear terminal | `/clear` |
| `/exit` | Exit with summary | `/exit` |
| `/reset` | Reset conversation | `/reset` |
| `/theme <name>` | Change theme | `/theme hacker` |
| `/mode <type>` | Change AI mode | `/mode creative` |
| `/stats` | View session stats | `/stats` |
| `/achievements` | View badges | `/achievements` |
| `/play <game>` | Play mini-game | `/play trivia` |
| `/sound on\|off` | Toggle sounds | `/sound on` |
| `/focus on\|off` | Toggle focus mode | `/focus on` |
| `/export <format>` | Export chat | `/export md` |
| `/name <name>` | Set nickname | `/name Alex` |
| `/bookmark` | Save moment | `/bookmark` |
| `/bookmarks` | List bookmarks | `/bookmarks` |
| `/about` | About NovaMind | `/about` |
| `/hint` | Easter egg hint | `/hint` |

### AI Modes

| Mode | Description |
|------|-------------|
| `creative` | Imaginative and playful |
| `serious` | Professional and focused |
| `friendly` | Warm and casual (default) |
| `sarcastic` | Witty with sass |

---

## 🏆 Achievements

| Badge | Name | How to Unlock |
|-------|------|---------------|
| 🌟 | First Contact | Start your first conversation |
| 💬 | Chatterbox | Send 50 messages in a session |
| 🤔 | Curious Mind | Ask 10 questions |
| 🎨 | Theme Explorer | Try all 6 themes |
| 🔮 | Secret Finder | Discover an easter egg |
| 🦉 | Night Owl | Chat after midnight |
| 🐦 | Early Bird | Chat before 6 AM |
| ⚡ | Speed Demon | Reply within 2 seconds |
| 🏃 | Marathon Chatter | Chat for 30+ minutes |
| ✍️ | Wordsmith | Write 1000+ words |
| 📚 | Bookworm | Create 5 bookmarks |
| ⌨️ | Commander | Use 10 different commands |
| 🎭 | Mood Master | Experience 5 moods |
| 🧘 | Zen Master | Use zen theme for 10 min |
| 💻 | Elite Hacker | Find the sudo easter egg |
| 📺 | Nostalgia Trip | Use the retro theme |
| 🎂 | Party Time! | Celebrate a birthday |
| 🏆 | Completionist | Unlock 10 achievements |

---

## 🔮 Easter Eggs

Try typing these secret phrases!

| Trigger | Hint |
|---------|------|
| `42` | The answer to everything |
| `matrix` | Follow the white rabbit |
| `hello world` | Developer greeting |
| `konami` | Classic game code |
| `sudo` | Root access |
| `uwu` | Cute mode |
| `rickroll` | Never gonna... |
| `coffee` | Caffeine boost |
| `tell me a secret` | Hidden wisdom |
| `i love you` | Warm response |
| `happy birthday` | Celebration! |
| `flip table` | Express frustration |
| `i'm bored` | Game suggestions |

---

## 🎮 Mini-Games

| Game | Command | Description |
|------|---------|-------------|
| 🎯 Trivia | `/play trivia` | Random trivia question with answers |
| 🥠 Fortune | `/play fortune` | Get a fortune cookie message |
| 🎱 8-Ball | `/play 8ball` | Ask the magic 8-ball |
| 😄 Jokes | `/play joke` | Hear a programmer joke |

---

## 📁 Project Structure

```
CLI Basesd AI chatbot/
├── main.py              # Entry point (500+ lines)
├── requirements.txt     # Dependencies
├── .env                 # API key (create this)
├── README.md            # This file
└── core/
    ├── __init__.py      # Package init
    ├── ai_engine.py     # Gemini AI integration
    ├── animator.py      # Typing & effects
    ├── ui.py            # Terminal UI panels
    ├── logos.py         # ASCII art logos
    ├── styles.py        # 11 theme system
    ├── memory.py        # Session management
    ├── commands.py      # 18 commands
    ├── mood.py          # Sentiment detection
    ├── achievements.py  # 18 badges
    ├── easter_eggs.py   # 15 secrets
    ├── sounds.py        # Sound simulation
    └── utils.py         # Helpers
```

---

## 🔧 Requirements

- Python 3.8+
- Google Gemini API key
- Works on Windows, Linux, macOS

### Dependencies

```
rich>=13.0.0
python-dotenv>=1.0.0
google-generativeai>=0.3.0
textblob>=0.17.1
emoji>=2.0.0
pyfiglet>=0.8.post1
```

---

## 🎯 Quick Start Summary

```powershell
# 1. Navigate to project
cd "c:\Users\admin\Documents\CLI Basesd AI chatbot"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up API key
echo GEMINI_API_KEY=your_key_here > .env

# 4. Run NovaMind
python main.py

# 5. Try these commands:
#    /help          - See all commands
#    /theme hacker  - Matrix theme
#    /play trivia   - Play trivia
#    42             - Easter egg!
#    /exit          - Exit with summary
```

---

<p align="center">
  Made with ❤️ for terminal lovers<br>
  <b>NovaMind v1.0</b>
</p>
