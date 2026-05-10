"""
handlers/moderation.py — Admin-only moderation commands.
Commands: /ban, /kick, /mute, /unmute
Usage: Reply to a user's message and run the command.
"""

from datetime import timedelta
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus
from utils.helpers import is_admin


def register(app: Client):

    # ── /ban ──────────────────────────────────────────────────────────────────
    @app.on_message(filters.command("ban") & filters.group)
    async def ban_user(client: Client, message: Message):
        if not await is_admin(client, message.chat.id, message.from_user.id):
            return await message.reply("❌ Only admins can use this command.")

        target = await _get_target(message)
        if not target:
            return await message.reply("↩️ Reply to a user's message to ban them.")

        await client.ban_chat_member(message.chat.id, target.id)
        await message.reply(f"🔨 {target.mention} has been **banned**.")

    # ── /kick ─────────────────────────────────────────────────────────────────
    @app.on_message(filters.command("kick") & filters.group)
    async def kick_user(client: Client, message: Message):
        if not await is_admin(client, message.chat.id, message.from_user.id):
            return await message.reply("❌ Only admins can use this command.")

        target = await _get_target(message)
        if not target:
            return await message.reply("↩️ Reply to a user's message to kick them.")

        # Ban then immediately unban = kick (they can rejoin)
        await client.ban_chat_member(message.chat.id, target.id)
        await client.unban_chat_member(message.chat.id, target.id)
        await message.reply(f"👢 {target.mention} has been **kicked**.")

    # ── /mute ─────────────────────────────────────────────────────────────────
    @app.on_message(filters.command("mute") & filters.group)
    async def mute_user(client: Client, message: Message):
        if not await is_admin(client, message.chat.id, message.from_user.id):
            return await message.reply("❌ Only admins can use this command.")

        target = await _get_target(message)
        if not target:
            return await message.reply("↩️ Reply to a user's message to mute them.")

        # Restrict: revoke permission to send messages
        await client.restrict_chat_member(
            message.chat.id,
            target.id,
            permissions=_no_send_permissions(),
        )
        await message.reply(f"🔇 {target.mention} has been **muted**.")

    # ── /unmute ───────────────────────────────────────────────────────────────
    @app.on_message(filters.command("unmute") & filters.group)
    async def unmute_user(client: Client, message: Message):
        if not await is_admin(client, message.chat.id, message.from_user.id):
            return await message.reply("❌ Only admins can use this command.")

        target = await _get_target(message)
        if not target:
            return await message.reply("↩️ Reply to a user's message to unmute them.")

        # Restore default permissions (all allowed)
        await client.restrict_chat_member(
            message.chat.id,
            target.id,
            permissions=_default_permissions(),
        )
        await message.reply(f"🔊 {target.mention} has been **unmuted**.")


# ── Internal helpers ──────────────────────────────────────────────────────────

async def _get_target(message: Message):
    """Return the user that was replied to, or None."""
    if message.reply_to_message and message.reply_to_message.from_user:
        return message.reply_to_message.from_user
    return None


def _no_send_permissions():
    """ChatPermissions object that blocks all sending."""
    from pyrogram.types import ChatPermissions
    return ChatPermissions(
        can_send_messages=False,
        can_send_media_messages=False,
        can_send_other_messages=False,
        can_add_web_page_previews=False,
    )


def _default_permissions():
    """ChatPermissions object that restores normal member rights."""
    from pyrogram.types import ChatPermissions
    return ChatPermissions(
        can_send_messages=True,
        can_send_media_messages=True,
        can_send_other_messages=True,
        can_add_web_page_previews=True,
    )
