"""
utils/helpers.py — Shared utility functions used across handlers.
"""

from config import LEVELS


def get_level(xp: int) -> str:
    """Return the level name for a given XP amount."""
    level_name = LEVELS[0][1]  # default: lowest level
    for threshold, name in LEVELS:
        if xp >= threshold:
            level_name = name
    return level_name


def get_level_progress(xp: int) -> tuple[str, int, int | None]:
    """
    Returns (current_level_name, xp_into_level, xp_needed_for_next).
    xp_needed_for_next is None if user is at max level.
    """
    current_name = LEVELS[0][1]
    current_threshold = 0
    next_threshold = None

    for i, (threshold, name) in enumerate(LEVELS):
        if xp >= threshold:
            current_name = name
            current_threshold = threshold
            # Check if there's a next level
            if i + 1 < len(LEVELS):
                next_threshold = LEVELS[i + 1][0]

    xp_into_level = xp - current_threshold
    xp_to_next = (next_threshold - xp) if next_threshold else None
    return current_name, xp_into_level, xp_to_next


def format_leaderboard(rows, title: str) -> str:
    """Format leaderboard rows into a readable message string."""
    if not rows:
        return f"📊 *{title}*\n\nNo data yet. Start chatting!"

    medals = ["🥇", "🥈", "🥉"]
    lines = [f"📊 *{title}*\n"]

    for i, row in enumerate(rows):
        icon = medals[i] if i < 3 else f"`{i+1}.`"
        name = row["username"] or "Unknown"
        lines.append(f"{icon} *{name}* — {row['xp']} XP | {row['total_msgs']} msgs")

    return "\n".join(lines)


async def is_admin(client, chat_id: int, user_id: int) -> bool:
    """Check if a user is an admin or creator in the chat."""
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status.name in ("ADMINISTRATOR", "OWNER")
    except Exception:
        return False
