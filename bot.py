"""
bot.py — Entry point for the Telegram moderation + leveling bot.

pyrotgfork is a maintained pyrogram fork that works on Python 3.14.
We also manually set an event loop before importing pyrogram,
because Python 3.14 no longer auto-creates one on the main thread.
"""

import asyncio
import os

# ── MUST be before any pyrogram import ───────────────────────────────────────
# Python 3.14 removed the implicit event loop. Set one before pyrogram loads.
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

from aiohttp import web
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
from handlers import moderation, antilink, leveling, leaderboard, rank


# ── Tiny async health server (required so Render doesn't kill the process) ────
async def run_health_server():
    port = int(os.environ.get("PORT", 8080))
    app = web.Application()
    app.router.add_get("/", lambda r: web.Response(text="Bot is running!"))
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, "0.0.0.0", port).start()
    print(f"✅ Health server on port {port}")
    await asyncio.Event().wait()


# ── Pyrogram async bot ────────────────────────────────────────────────────────
async def run_bot():
    bot = Client(
        "adda_bot",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
    )

    moderation.register(bot)
    antilink.register(bot)
    leveling.register(bot)
    leaderboard.register(bot)
    rank.register(bot)

    await bot.start()
    print("✅ Bot is running...")
    await asyncio.Event().wait()
    await bot.stop()


async def main():
    await asyncio.gather(
        run_health_server(),
        run_bot(),
    )

if __name__ == "__main__":
    loop.run_until_complete(main())