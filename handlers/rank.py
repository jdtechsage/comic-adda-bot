import os
import asyncio
from aiohttp import web
from pyrogram import Client, idle

print("🚀 Starting bot...", flush=True)

# ENV VARIABLES
API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
BOT_TOKEN = os.environ["BOT_TOKEN"]

# CREATE BOT CLIENT
app = Client(
    "comic_adda_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

print("✅ Client created", flush=True)

# IMPORT REGISTER FUNCTIONS
from handlers.rank import register as register_rank
from handlers.leveling import register as register_leveling
from handlers.leaderboard import register as register_leaderboard
from handlers.moderation import register as register_moderation
from handlers.antilink import register as register_antilink

# REGISTER HANDLERS
register_rank(app)
register_leveling(app)
register_leaderboard(app)
register_moderation(app)
register_antilink(app)

print("✅ All handlers registered!", flush=True)


# HEALTH CHECK ROUTE
async def health(request):
    return web.Response(text="Bot is running!")


# START HEALTH SERVER
async def start_health_server():
    port = int(os.environ.get("PORT", 10000))

    web_app = web.Application()
    web_app.router.add_get("/", health)

    runner = web.AppRunner(web_app)
    await runner.setup()

    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    print(f"✅ Health server running on port {port}", flush=True)


# MAIN FUNCTION
async def main():
    try:
        await start_health_server()

        print("⏳ Connecting to Telegram...", flush=True)

        await app.start()

        me = await app.get_me()

        print(f"✅ Bot online: @{me.username}", flush=True)

        # OPTIONAL STARTUP MESSAGE
        try:
            await app.send_message(
                "deepdarji",
                f"✅ Bot is online!\n🤖 @{me.username}"
            )
            print("✅ Startup message sent", flush=True)

        except Exception as e:
            print(f"⚠️ Could not send startup message: {e}", flush=True)

        print("🎉 Bot fully started!", flush=True)

        await idle()

    except Exception as e:
        print(f"❌ MAIN ERROR: {e}", flush=True)

    finally:
        await app.stop()


# RUN BOT
asyncio.run(main())