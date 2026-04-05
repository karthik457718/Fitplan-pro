"""
utils/streak_manager.py — Streak calculation and update logic for FitPlan Pro.

Streak increases when user completes all exercises for a day.
Streak resets if a day is missed.
Works with both Supabase and SQLite via utils/db.py.
"""

from datetime import date, timedelta


# ── CORE UPDATE ───────────────────────────────────────────────────────────────

def update_streak(username: str, day_completed: bool) -> int:
    """
    Call this every time a user completes or uncompletes a workout day.

    day_completed=True  → mark today done, extend or start streak
    day_completed=False → unmark today, decrement streak if it was counted

    Returns: updated current_streak (int)
    """
    from utils.db import get_streak, save_streak

    today     = str(date.today())
    yesterday = str(date.today() - timedelta(days=1))

    streak  = get_streak(username)
    # Ensure username is always present (needed by save_streak)
    streak.setdefault("username", username)
    history = streak.get("streak_history", []) or []
    last    = streak.get("last_completed_date")

    if day_completed:
        # Add today to history if not already recorded
        if today not in history:
            history.append(today)
            history.sort()

        if last == yesterday:
            # Consecutive day — extend streak
            streak["current_streak"] = streak.get("current_streak", 0) + 1
        elif last == today:
            # Already counted today — nothing changes
            pass
        else:
            # Gap of 1+ days — restart from 1
            streak["current_streak"] = 1

        streak["last_completed_date"] = today
        streak["longest_streak"] = max(
            streak.get("longest_streak", 0),
            streak["current_streak"]
        )

    else:
        # User unchecked — today is no longer fully complete
        if last == today and today in history:
            history.remove(today)
            streak["current_streak"] = max(0, streak.get("current_streak", 1) - 1)
            streak["last_completed_date"] = history[-1] if history else None

    streak["streak_history"] = history
    save_streak(streak)

    return streak["current_streak"]


# ── DISPLAY DATA ──────────────────────────────────────────────────────────────

def get_streak_display(username: str) -> dict:
    """
    Get full streak info formatted for the UI.
    Auto-resets streak in DB if it was broken (missed days detected).

    Returns dict with:
      current_streak  — int
      longest_streak  — int
      last_completed  — str (ISO date) or None
      status          — "active" | "at_risk" | "broken" | "inactive"
      completed_days  — int (total history count)
      emoji           — str
    """
    from utils.db import get_streak, save_streak

    streak  = get_streak(username)
    streak.setdefault("username", username)

    current = streak.get("current_streak", 0)
    longest = streak.get("longest_streak", 0)
    last    = streak.get("last_completed_date")
    history = streak.get("streak_history", []) or []

    today     = str(date.today())
    yesterday = str(date.today() - timedelta(days=1))

    # Determine status
    if current > 0 and last not in (today, yesterday):
        # Streak was broken — reset display and DB
        status  = "broken"
        current = 0
        streak["current_streak"] = 0
        save_streak(streak)
    elif last == today:
        status = "active"
    elif last == yesterday:
        status = "at_risk"    # must complete today to keep alive
    else:
        status = "inactive"

    return {
        "current_streak": current,
        "longest_streak": longest,
        "last_completed":  last,
        "status":          status,
        "completed_days":  len(history),
        "history":         history,
        "emoji":           _streak_emoji(current),
    }


# ── MILESTONES ────────────────────────────────────────────────────────────────

def check_streak_milestone(streak_count: int) -> str | None:
    """
    Return a milestone celebration message when the user hits a notable streak.
    Returns None if no milestone at this count.
    """
    milestones = {
        1:   "First workout done! Your journey begins! 🌱",
        3:   "3-day streak! You're building a habit! 💪",
        7:   "One full week! Incredible consistency! 🏅",
        14:  "Two weeks strong! You're unstoppable! ⚡",
        21:  "21 days — habits are officially formed! 🧠",
        30:  "30-day streak! Elite level dedication! 🏆",
        50:  "50 days! You're a fitness legend! 🌟",
        75:  "75 days! Absolute machine! 🦾",
        100: "100 DAYS! You are a true champion! 👑",
        180: "180 days! Half a year of fire! 🔥👑",
        365: "ONE FULL YEAR! You are legendary! 🏆👑🔥",
    }
    return milestones.get(streak_count)


# ── HELPERS ───────────────────────────────────────────────────────────────────

def _streak_emoji(streak_count: int) -> str:
    """Return flame emoji(s) scaled to streak length."""
    if streak_count == 0:   return "💤"
    elif streak_count < 3:  return "🔥"
    elif streak_count < 7:  return "🔥🔥"
    elif streak_count < 14: return "🔥🔥🔥"
    elif streak_count < 30: return "⚡🔥"
    elif streak_count < 100:return "🏆🔥"
    else:                   return "👑🔥"


def get_streak_stats(username: str) -> dict:
    """
    Get quick stats for dashboard cards — lightweight call.
    Returns: current_streak, longest_streak, status, emoji
    """
    from utils.db import get_streak

    streak  = get_streak(username)
    current = streak.get("current_streak", 0)
    longest = streak.get("longest_streak", 0)
    last    = streak.get("last_completed_date")

    today     = str(date.today())
    yesterday = str(date.today() - timedelta(days=1))

    if current > 0 and last not in (today, yesterday):
        status  = "broken"
        current = 0
    elif last == today:
        status = "active"
    elif last == yesterday:
        status = "at_risk"
    else:
        status = "inactive"

    return {
        "current_streak": current,
        "longest_streak": longest,
        "status":          status,
        "emoji":           _streak_emoji(current),
    }