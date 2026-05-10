"""
bot.py — Entry point for the Telegram moderation + leveling bot.

Python 3.14 removed asyncio.get_event_loop() compatibility that pyrogram's
sync wrapper relied on. Fix: run everything natively async in one event loop.
- Pyrogram runs as a proper async client (app.start() / app.stop())
- aiohttp replaces Flask for the health server (no threading needed)
- Both run together via asyncio.gather()
"""

import asyncio
import os
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
    await asyncio.Event().wait()  # keep alive forever


# ── Pyrogram async bot ────────────────────────────────────────────────────────
async def run_bot():
    bot = Client(
        "adda_bot",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
    )

    # Register all handler modules
    moderation.register(bot)
    antilink.register(bot)
    leveling.register(bot)
    leaderboard.register(bot)
    rank.register(bot)

    await bot.start()
    print("✅ Bot is running...")
    await asyncio.Event().wait()  # keep alive until process is killed
    await bot.stop()


# ── Start both together in one event loop ────────────────────────────────────
async def main():
    await asyncio.gather(
        run_health_server(),
        run_bot(),
    )

if __name__ == "__main__":
    asyncio.run(main())