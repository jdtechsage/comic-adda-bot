
Claude is responding
You said: Build a Telegram moderation and leveling bot using Python and Pyrogram.
Build a Telegram moderation and leveling bot using Python and Pyrogram.
Features required:
1. Anti link system
* Delete messages containing:
  http
  https
  t.me
  telegram.me
2. Moderation commands
* /ban
* /kick
* /mute
* /unmute
* Admin only commands
3. XP and leveling system
* Give 5 XP per message
* Add cooldown to prevent spam farming
* Levels:
1. Newbie
2. Space Walker
3. Cosmic Elite
4. Adda Legend
5. Leaderboards

Commands:
* /top_today
* /top_week
* /top_month
* /top_all
5. Rank command
   /rank should show:
* XP
* Level
* Total messages
* Current streak
6. Daily streak system
* Track daily activity
* Reset if user misses a day
7. Use clean modular structure
8. Include setup instructions for:
* API_ID
* API_HASH
* BOT_TOKEN
(other needed?)
9. Make code with comments and less complexity.
then step by step guide what to do? where to host? Free

Show more
5:52 PM
Claude responded: Now let me build all the bot files and the visual guide.

Check frontend design skill
Check frontend design skill
Now let me build all the bot files and the visual guide.


Created 14 files, ran a command
Created 14 files, ran a command

Create project structure

Script

Main bot entry point
bot.py

Config file
config.py

Database helper using SQLite
database.py

Helper utilities
helpers.py

Utils __init__
__init__.py

Handlers __init__
__init__.py

Anti-link handler
antilink.py

Moderation commands handler
moderation.py

XP and leveling handler
leveling.py

Rank command handler
rank.py

Leaderboard commands handler
leaderboard.py

Requirements file
requirements.txt

Procfile for Railway/Render deployment
Procfile

README with full setup guide
README.md
Done
Now let's zip everything and build the visual guide:


Zip the bot project
Zip the bot project

Zip the bot project
bash

cd /home/claude && zip -r tgbot.zip tgbot/ && echo "done"
Output

  adding: tgbot/ (stored 0%)
  adding: tgbot/Procfile (stored 0%)
  adding: tgbot/requirements.txt (stored 0%)
  adding: tgbot/config.py (deflated 62%)
  adding: tgbot/handlers/ (stored 0%)
  adding: tgbot/handlers/leaderboard.py (deflated 73%)
  adding: tgbot/handlers/leveling.py (deflated 67%)
  adding: tgbot/handlers/__init__.py (stored 0%)
  adding: tgbot/handlers/moderation.py (deflated 81%)
  adding: tgbot/handlers/rank.py (deflated 58%)
  adding: tgbot/handlers/antilink.py (deflated 52%)
  adding: tgbot/README.md (deflated 53%)
  adding: tgbot/{handlers,utils,data}/ (stored 0%)
  adding: tgbot/utils/ (stored 0%)
  adding: tgbot/utils/__init__.py (stored 0%)
  adding: tgbot/utils/helpers.py (deflated 55%)
  adding: tgbot/utils/database.py (deflated 64%)
  adding: tgbot/bot.py (deflated 44%)
done
Done
Now building the visual guide:


Ran a command, read a file
Ran a command, read a file


Here's your complete bot — click the steps above to walk through setup. Here's a quick summary of what's included:

What's in the zip (8 files, clean modular structure):

bot.py — entry point, registers all handlers
config.py — all your settings in one place (API keys, XP values, levels, blocked patterns)
handlers/antilink.py — auto-deletes any message with http, https, t.me, telegram.me (admins exempt)
handlers/moderation.py — /ban, /kick, /mute, /unmute with admin-only checks; reply to any message to target that user
handlers/leveling.py — 5 XP per message, 60-second cooldown, level-up announcements, daily streak tracking
handlers/rank.py — /rank shows XP bar, level name, message count, streak with fire emoji for 3+ day streaks
handlers/leaderboard.py — all four /top_* commands
utils/database.py — SQLite (no external DB needed, zero cost)
Key design decisions to know:

Leaderboards filter by last_msg_date — users who haven't spoken in the period drop off naturally
Streak resets if a user skips a day (tracked per YYYY-MM-DD)
Muting uses Pyrogram's restrict_chat_member — unmuting restores full default permissions
The .db file lives in data/bot.db and is auto-created on first run
For Railway hosting, just swap the 3 hardcoded values in config.py with os.environ["..."] calls as shown in Step 7, push to GitHub, and connect the repo — it picks up the Procfile automatically.


Tgbot
ZIP 
You said: want to use render.
want to use render... what to do to config file? without credential.... 

then step by step of render

6:00 PM

Working
Working

Check current config.py

Update config.py to read credentials from environmen



Claude is AI and can make mistakes. Please double-check responses.
Config · PY
Copy

"""
config.py — All bot configuration in one place.
Fill in your credentials here before running the bot.
"""
 
# ─── Telegram Credentials ─────────────────────────────────────────────────────
# Get these from https://my.telegram.org → "API development tools"
API_ID   = 123456          # Replace with your api_id (integer)
API_HASH = "your_api_hash" # Replace with your api_hash (string)
 
# Get this from @BotFather on Telegram
BOT_TOKEN = "your_bot_token"
 
# ─── XP Settings ──────────────────────────────────────────────────────────────
XP_PER_MESSAGE   = 5    # XP awarded per valid message
XP_COOLDOWN_SECS = 60   # Seconds before a user can earn XP again
 
# ─── Level Thresholds (XP required to reach each level) ───────────────────────
LEVELS = [
    (0,    "Newbie"),
    (100,  "Space Walker"),
    (500,  "Cosmic Elite"),
    (1500, "Adda Legend"),
]
 
# ─── Anti-Link Keywords ────────────────────────────────────────────────────────
BLOCKED_LINK_PATTERNS = ["http", "https", "t.me", "telegram.me"]
 
