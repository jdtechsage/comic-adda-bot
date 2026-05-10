"""
utils/database.py — SQLite database for XP, levels, streaks, and messages.
Uses a single .db file — no external database needed.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "bot.db")


def get_connection():
    """Return a connection to the SQLite database."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # lets us access columns by name
    return conn


def init_db():
    """Create tables if they don't exist yet. Called once on startup."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id      INTEGER NOT NULL,
                chat_id      INTEGER NOT NULL,
                username     TEXT,
                xp           INTEGER DEFAULT 0,
                total_msgs   INTEGER DEFAULT 0,
                streak       INTEGER DEFAULT 0,
                last_msg_date TEXT,          -- date string YYYY-MM-DD
                last_xp_time  REAL DEFAULT 0, -- unix timestamp for cooldown
                PRIMARY KEY (user_id, chat_id)
            )
        """)
        conn.commit()


def get_user(user_id: int, chat_id: int) -> sqlite3.Row | None:
    """Fetch a user row, or None if not found."""
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM users WHERE user_id=? AND chat_id=?",
            (user_id, chat_id),
        ).fetchone()


def upsert_user(user_id: int, chat_id: int, username: str):
    """Create user row if missing, or update username."""
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO users (user_id, chat_id, username)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id, chat_id) DO UPDATE SET username=excluded.username
        """, (user_id, chat_id, username))
        conn.commit()


def update_xp(user_id: int, chat_id: int, xp_gain: int,
              new_msgs: int, streak: int, last_date: str, last_xp_time: float):
    """Update XP, message count, streak, and timestamps."""
    with get_connection() as conn:
        conn.execute("""
            UPDATE users
            SET xp=xp+?, total_msgs=total_msgs+?, streak=?, 
                last_msg_date=?, last_xp_time=?
            WHERE user_id=? AND chat_id=?
        """, (xp_gain, new_msgs, streak, last_date, last_xp_time,
              user_id, chat_id))
        conn.commit()


def get_leaderboard(chat_id: int, period: str, limit: int = 10):
    """
    Returns top users for a given period.
    period: 'today' | 'week' | 'month' | 'all'
    We use date filtering on last_msg_date for approximations.
    For a full period leaderboard you'd track daily XP separately;
    here we rank by total XP for simplicity (common bot pattern).
    """
    with get_connection() as conn:
        if period == "today":
            date_filter = "AND last_msg_date = date('now')"
        elif period == "week":
            date_filter = "AND last_msg_date >= date('now', '-7 days')"
        elif period == "month":
            date_filter = "AND last_msg_date >= date('now', '-30 days')"
        else:  # all
            date_filter = ""

        rows = conn.execute(f"""
            SELECT username, xp, total_msgs, streak
            FROM users
            WHERE chat_id=? {date_filter}
            ORDER BY xp DESC
            LIMIT ?
        """, (chat_id, limit)).fetchall()
    return rows
