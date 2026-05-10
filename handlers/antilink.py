"""
handlers/antilink.py — Deletes messages containing links.
Admins are exempt from this check.
"""

from pyrogram import Client, filters
from pyrogram.types import Message
from config import BLOCKED_LINK_PATTERNS
from utils.helpers import is_admin


def register(app: Client):

    @app.on_message(filters.group & filters.text)
    async def check_for_links(client: Client, message: Message):
        # Admins can post links freely
        if await is_admin(client, message.chat.id, message.from_user.id):
            return

        text = message.text.lower()

        # Check if any blocked pattern is in the message
        for pattern in BLOCKED_LINK_PATTERNS:
            if pattern in text:
                await message.delete()
                warning = await message.reply(
                    f"⚠️ {message.from_user.mention}, links are not allowed here!"
                )
                # Auto-delete the warning after 5 seconds
                await warning.delete(5)
                return  # Stop after first match
