# 🤖 Adda Bot — Telegram Moderation + Leveling Bot

Built with Python & Pyrogram. Features anti-link, moderation commands, XP leveling, streaks, and leaderboards.

---

## 📁 Project Structure

```
tgbot/
├── bot.py               # Entry point — run this
├── config.py            # Your credentials & settings
├── requirements.txt
├── Procfile             # For Railway/Render hosting
├── data/
│   └── bot.db           # Auto-created SQLite database
├── handlers/
│   ├── antilink.py      # Deletes link messages
│   ├── moderation.py    # /ban /kick /mute /unmute
│   ├── leveling.py      # XP per message + streak
│   ├── rank.py          # /rank command
│   └── leaderboard.py   # /top_today /top_week /top_month /top_all
└── utils/
    ├── database.py      # SQLite helpers
    └── helpers.py       # Shared utility functions
```

---

## ⚙️ Setup (Local)

### Step 1 — Get your Telegram credentials

1. Go to https://my.telegram.org
2. Log in → click **"API development tools"**
3. Create an app → copy `api_id` and `api_hash`
4. Open Telegram → search `@BotFather` → `/newbot`
5. Follow prompts → copy the `bot_token`

### Step 2 — Fill in config.py

Open `config.py` and replace the placeholders:

```python
API_ID   = 123456          # your integer api_id
API_HASH = "abc123..."     # your api_hash string
BOT_TOKEN = "110201543..." # from BotFather
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Run the bot

```bash
python bot.py
```

You should see: `✅ Bot is running...`

### Step 5 — Add bot to your group

1. Open your Telegram group
2. Add the bot as a member
3. Promote it to **Admin** (needs ban/restrict/delete permissions)

---

## 🌐 Free Hosting Options

### Option A — Railway (Recommended, easiest)

1. Push your code to GitHub
2. Go to https://railway.app → sign up (free)
3. Click **New Project → Deploy from GitHub**
4. Select your repo
5. Go to **Variables** tab → add:
   - `API_ID` = your value
   - `API_HASH` = your value
   - `BOT_TOKEN` = your value
6. Update `config.py` to read from env vars:
   ```python
   import os
   API_ID   = int(os.environ["API_ID"])
   API_HASH = os.environ["API_HASH"]
   BOT_TOKEN = os.environ["BOT_TOKEN"]
   ```
7. Railway auto-detects `Procfile` and runs `python bot.py`
8. Free tier gives 500 hours/month (enough for one bot)

### Option B — Render

1. Push to GitHub
2. Go to https://render.com → sign up
3. New → **Background Worker** → connect GitHub repo
4. Build command: `pip install -r requirements.txt`
5. Start command: `python bot.py`
6. Add environment variables (same as Railway above)
7. Free tier spins down after inactivity — use Railway instead

### Option C — Always-Free VPS (Oracle Cloud)

1. Sign up at https://cloud.oracle.com (free forever tier)
2. Create an **ARM VM** (4 CPU, 24GB RAM — free!)
3. SSH in, install Python, clone your repo
4. Run with: `nohup python bot.py &`
5. Or set up a systemd service for auto-restart

---

## 📋 Commands Reference

| Command | Who | Description |
|---|---|---|
| `/rank` | Everyone | Show your XP, level, streak |
| `/top_today` | Everyone | Today's top chatters |
| `/top_week` | Everyone | This week's top chatters |
| `/top_month` | Everyone | This month's top chatters |
| `/top_all` | Everyone | All-time leaderboard |
| `/ban` | Admins | Ban a replied-to user |
| `/kick` | Admins | Kick a replied-to user |
| `/mute` | Admins | Mute a replied-to user |
| `/unmute` | Admins | Unmute a replied-to user |

---

## ⭐ Level Thresholds

| XP | Level |
|---|---|
| 0 | Newbie |
| 100 | Space Walker |
| 500 | Cosmic Elite |
| 1500 | Adda Legend |

Adjust these in `config.py` → `LEVELS` list.
