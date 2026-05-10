import os
import asyncio
from aiohttp import web
from pyrogram import Client, idle

print("STEP 1: bot.py started", flush=True)

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
BOT_TOKEN = os.environ["BOT_TOKEN"]

print("STEP 2: env loaded", flush=True)

app = Client(
    "comic_adda_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

print("STEP 3: client created", flush=True)


async def health(request):
    return web.Response(text="Bot running!")


async def start_health_server():
    print("STEP 4: starting health server", flush=True)

    port = int(os.environ.get("PORT", 10000))

    web_app = web.Application()
    web_app.router.add_get("/", health)

    runner = web.AppRunner(web_app)
    await runner.setup()

    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    print(f"✅ Health server running on port {port}", flush=True)


async def main():
    try:
        await start_health_server()

        print("STEP 5: connecting bot", flush=True)

        await app.start()

        me = await app.get_me()

        print(f"✅ Bot online: @{me.username}", flush=True)

        await app.send_message(
            "deepdarji",
            f"✅ Bot started successfully!\n🤖 @{me.username}"
        )

        print("STEP 6: sent startup message", flush=True)

        await idle()

    except Exception as e:
        print("❌ ERROR:", repr(e), flush=True)
        raise


asyncio.run(main())