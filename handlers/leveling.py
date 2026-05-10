"""
handlers/leveling.py — Awards XP per message with cooldown and streak tracking.
"""

import time
from datetime import date, timedelta
from pyrogram import Client, filters
from pyrogram.types import Message
from config import XP_PER_MESSAGE, XP_COOLDOWN_SECS
from utils.database import get_user, upsert_user, update_xp
from utils.helpers import get_level


def register(app: Client):

    @app.on_message(filters.group & filters.text)
    async def award_xp(client: Client, message: Message):
        user = message.from_user
        if user is None or user.is_bot:
            return  # Skip bots

        chat_id = message.chat.id
        user_id = user.id
        username = user.username or user.first_name or "User"
        now = time.time()
        today = str(date.today())  # "YYYY-MM-DD"

        # Ensure user exists in DB
        upsert_user(user_id, chat_id, username)
        row = get_user(user_id, chat_id)

        # ── Cooldown check ────────────────────────────────────────────────────
        last_xp_time = row["last_xp_time"] if row else 0
        if now - last_xp_time < XP_COOLDOWN_SECS:
            # Still on cooldown — count the message but don't give XP
            update_xp(user_id, chat_id, 0, 1, 
                      row["streak"], row["last_msg_date"] or today, last_xp_time)
            return

        # ── Streak calculation ─────────────────────────────────────────────────
        last_date_str = row["last_msg_date"] if row else None
        current_streak = row["streak"] if row else 0

        if last_date_str is None:
            # First ever message
            new_streak = 1
        else:
            last_date = date.fromisoformat(last_date_str)
            diff = (date.today() - last_date).days

            if diff == 0:
                new_streak = current_streak  # Same day, keep streak
            elif diff == 1:
                new_streak = current_streak + 1  # Consecutive day!
            else:
                new_streak = 1  # Missed a day — reset

        # ── Award XP ──────────────────────────────────────────────────────────
        old_level = get_level(row["xp"] if row else 0)
        update_xp(user_id, chat_id, XP_PER_MESSAGE, 1, new_streak, today, now)

        # Check for level-up
        new_row = get_user(user_id, chat_id)
        new_level = get_level(new_row["xp"])

        if new_level != old_level:
            await message.reply(
                f"🎉 {message.from_user.mention} leveled up to **{new_level}**! "
                f"Keep going 🚀"
            )
