"""
bot.py — Entry point for the Telegram moderation + leveling bot.
Run this file to start the bot.
"""

from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
from handlers import moderation, antilink, leveling, leaderboard, rank

# Create the Pyrogram client (your bot)
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
    print("✅ Bot is running...")
    app.run()
