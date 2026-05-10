"""
config.py — All bot configuration in one place.

Credentials are loaded from environment variables (set these on Render).
Never hardcode API_ID, API_HASH, or BOT_TOKEN in this file.
"""

import os

# Set these 3 variables in Render → your service → Environment tab.
API_ID    = int(os.environ["API_ID"])
API_HASH  = os.environ["API_HASH"]
BOT_TOKEN = os.environ["BOT_TOKEN"]

# ── XP Settings ──────────────────────────────────────────────────────────────
XP_PER_MESSAGE   = 5
XP_COOLDOWN_SECS = 60

# ── Level Thresholds ─────────────────────────────────────────────────────────
LEVELS = [
    (0,    "Newbie"),
    (100,  "Space Walker"),
    (500,  "Cosmic Elite"),
    (1500, "Adda Legend"),
]

# ── Anti-Link Keywords ────────────────────────────────────────────────────────
BLOCKED_LINK_PATTERNS = ["http", "https", "t.me", "telegram.me"]