"""
bot.py — Entry point for the Telegram moderation + leveling bot.

Render's free tier only supports Web Services (not Background Workers).
Web Services must bind to an HTTP port or Render kills them.
So we run a tiny Flask health-check server in a background thread,
and the Pyrogram bot runs on the main thread as normal.
"""

import threading
from flask import Flask
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
from handlers import moderation, antilink, leveling, leaderboard, rank

# ── Tiny health-check web server (required by Render free tier) ───────────────
health_app = Flask(__name__)

@health_app.route("/")
def health():
    return "Bot is running!", 200

def run_health_server():
    # Render sets the PORT env variable; default to 8080 locally
    import os
    port = int(os.environ.get("PORT", 8080))
    health_app.run(host="0.0.0.0", port=port)

# ── Pyrogram bot client ───────────────────────────────────────────────────────
app = Client(
    "adda_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

# Register all handler modules
moderation.register(app)
antilink.register(app)
leveling.register(app)
leaderboard.register(app)
rank.register(app)

if __name__ == "__main__":
    # Start Flask in a background thread (daemon=True so it exits with the bot)
    thread = threading.Thread(target=run_health_server, daemon=True)
    thread.start()
    print("✅ Health server started")

    # Run the bot on the main thread
    print("✅ Bot is running...")
    app.run()