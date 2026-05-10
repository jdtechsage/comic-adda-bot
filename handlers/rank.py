"""
handlers/rank.py — /rank command shows a user's XP, level, messages, and streak.
"""

from pyrogram import Client, filters
from pyrogram.types import Message
from utils.database import get_user, upsert_user
from utils.helpers import get_level, get_level_progress


def register(app: Client):

    @app.on_message(filters.command("rank") & filters.group)
    async def show_rank(client: Client, message: Message):
        user = message.from_user
        upsert_user(user.id, message.chat.id, user.username or user.first_name)
        row = get_user(user.id, message.chat.id)

        if not row or row["total_msgs"] == 0:
            return await message.reply("You haven't sent any messages yet. Start chatting!")

        xp = row["xp"]
        level_name, xp_into_level, xp_to_next = get_level_progress(xp)

        # Build the XP bar (10 blocks)
        if xp_to_next:
            filled = int((xp_into_level / (xp_into_level + xp_to_next)) * 10)
            bar = "█" * filled + "░" * (10 - filled)
            progress_text = f"`[{bar}]` {xp_into_level}/{xp_into_level + xp_to_next} XP to next level"
        else:
            bar = "█" * 10
            progress_text = f"`[{bar}]` Max level reached! 🏆"

        streak_emoji = "🔥" if row["streak"] >= 3 else "📅"

        text = (
            f"👤 **{user.mention}'s Rank**\n"
            f"━━━━━━━━━━━━━━━\n"
            f"⭐ Level: **{level_name}**\n"
            f"💫 Total XP: **{xp}**\n"
            f"💬 Messages: **{row['total_msgs']}**\n"
            f"{streak_emoji} Daily Streak: **{row['streak']} day(s)**\n"
            f"━━━━━━━━━━━━━━━\n"
            f"{progress_text}"
        )

        await message.reply(text)
