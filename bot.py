import asyncio
import os

# Must happen before pyrogram import
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

from aiohttp import web
from pyrogram import Client, idle
from config import API_ID, API_HASH, BOT_TOKEN
from handlers import moderation, antilink, leveling, leaderboard, rank

OWNER_USERNAME = "deepdarji"

async def start_health_server():
    port = int(os.environ.get("PORT", 8080))
    app = web.Application()
    app.router.add_get("/", lambda r: web.Response(text="Bot is running!"))
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, "0.0.0.0", port).start()
    print(f"✅ Health server on port {port}", flush=True)

async def main():
    await start_health_server()

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

    try:
        print("⏳ Connecting to Telegram...", flush=True)
        await bot.start()
        me = await bot.get_me()
        print(f"✅ Bot online: @{me.username}", flush=True)

        try:
            await bot.send_message(
                OWNER_USERNAME,
                f"✅ Bot is online!\n🤖 @{me.username} running on Render."
            )
        except Exception as e:
            print(f"⚠️ Notify failed: {e}", flush=True)

        await idle()

    except Exception as e:
        print(f"❌ Bot error: {type(e).__name__}: {e}", flush=True)
        raise
    finally:
        try:
            await bot.stop()
        except Exception:
            pass

if __name__ == "__main__":
    loop.run_until_complete(main())
