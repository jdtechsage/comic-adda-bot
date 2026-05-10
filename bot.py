import os
import asyncio
from aiohttp import web
from pyrogram import Client, idle

print("Starting bot...", flush=True)

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
BOT_TOKEN = os.environ["BOT_TOKEN"]

app = Client(
    "comic_adda_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# IMPORT HANDLERS
from handlers.antilink import *
from handlers.moderation import *
from handlers.leveling import *
from handlers.rank import *
from handlers.leaderboard import *

print("Handlers loaded!", flush=True)


async def health(request):
    return web.Response(text="Bot is running!")


async def start_health_server():
    port = int(os.environ.get("PORT", 10000))

    web_app = web.Application()
    web_app.router.add_get("/", health)

    runner = web.AppRunner(web_app)
    await runner.setup()

    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    print(f"Health server running on port {port}", flush=True)


async def main():
    await start_health_server()

    print("Connecting bot...", flush=True)

    await app.start()

    me = await app.get_me()

    print(f"✅ Bot online: @{me.username}", flush=True)

    try:
        await app.send_message(
            "deepdarji",
            f"✅ Bot online!\n🤖 @{me.username}"
        )
    except Exception as e:
        print(f"Startup message failed: {e}", flush=True)

    print("Bot fully started!", flush=True)

    await idle()

    await app.stop()


asyncio.run(main())