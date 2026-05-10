"""
handlers/leaderboard.py — Top user commands.
Commands: /top_today, /top_week, /top_month, /top_all
"""

from pyrogram import Client, filters
from pyrogram.types import Message
from utils.database import get_leaderboard
from utils.helpers import format_leaderboard


def register(app: Client):

    @app.on_message(filters.command("top_today") & filters.group)
    async def top_today(client: Client, message: Message):
        rows = get_leaderboard(message.chat.id, "today")
        await message.reply(format_leaderboard(rows, "Top Today"), parse_mode="markdown")

    @app.on_message(filters.command("top_week") & filters.group)
    async def top_week(client: Client, message: Message):
        rows = get_leaderboard(message.chat.id, "week")
        await message.reply(format_leaderboard(rows, "Top This Week"), parse_mode="markdown")

    @app.on_message(filters.command("top_month") & filters.group)
    async def top_month(client: Client, message: Message):
        rows = get_leaderboard(message.chat.id, "month")
        await message.reply(format_leaderboard(rows, "Top This Month"), parse_mode="markdown")

    @app.on_message(filters.command("top_all") & filters.group)
    async def top_all(client: Client, message: Message):
        rows = get_leaderboard(message.chat.id, "all")
        await message.reply(format_leaderboard(rows, "All-Time Legends"), parse_mode="markdown")
