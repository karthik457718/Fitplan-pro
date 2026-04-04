# -*- coding: utf-8 -*-
"""
daily_reminder.py — FitPlan Pro Daily Workout Reminder
======================================================
Sends a motivational "Don't forget your workout today!" email via Brevo.

USAGE (call from scheduler or HuggingFace Spaces startup):

    from daily_reminder import send_daily_reminder, should_send_reminder

    # Check if it's time to send (call every ~15 min from a background loop):
    if should_send_reminder(username, user_data, session_state):
        ok, msg = send_daily_reminder(username, user_data, session_state)

HOW TO INTEGRATE IN app.py / Dashboard:
    Add the settings UI from the snippet below to your Settings/Profile page.
    The scheduler block runs in your dashboard or a separate process.

SETTINGS STORED (via utils.db.save_user_setting):
    reminder_enabled   : "1" or "0"
    reminder_time      : "HH:MM"  (24-hour, user's local timezone label)
    reminder_tz_label  : display label e.g. "IST (UTC+5:30)"
    reminder_last_sent : ISO date "YYYY-MM-DD" — prevents duplicate sends
"""

import os, json, time, urllib.request, urllib.error
from datetime import date, datetime

BREVO_API_KEY    = os.getenv("BREVO_API_KEY", "")
EMAIL_SENDER     = os.getenv("BREVO_SENDER_EMAIL", "noreply@fitplanpro.ai")
SENDER_NAME      = "FitPlan Pro"

# ── Motivational messages rotated daily ──────────────────────────────────────
_MESSAGES = [
    ("🔥 Time to CRUSH It!", "Your muscles are rested. Your plan is ready. Today is the day."),
    ("💪 Your Workout Is Waiting", "Champions aren't made on rest days. Let's build something today."),
    ("⚡ Don't Break the Streak!", "You've been consistent. Don't let today be the day you stopped."),
    ("🏋️ One Workout Away", "You're one session away from feeling incredible. Let's go!"),
    ("🎯 Stay on Track", "Consistency beats intensity. Show up today — even for 20 minutes."),
    ("🚀 Push Your Limits", "Every rep is a vote for the athlete you're becoming. Cast yours today."),
    ("💎 Discipline = Freedom", "Do it now, feel great later. Your future self will thank you."),
]

def _get_message_of_day():
    idx = date.today().toordinal() % len(_MESSAGES)
    return _MESSAGES[idx]


def _build_email_html(username: str, workout_info: dict, reminder_time: str) -> str:
    subject_title, body_message = _get_message_of_day()
    day_num   = workout_info.get("day", "?")
    muscle    = workout_info.get("muscle_group", "Workout")
    ex_count  = workout_info.get("exercises", 0)
    is_rest   = workout_info.get("is_rest", False)

    if is_rest:
        session_info = "🌿 Today is your <strong>rest day</strong> — stretch, walk, and recover!"
        cta_text     = "View Rest Day Activities"
    else:
        session_info = (
            f"💪 Day <strong>{day_num}</strong> — <strong>{muscle}</strong>"
            + (f" &nbsp;·&nbsp; {ex_count} exercises" if ex_count else "")
        )
        cta_text = "Open My Workout Plan"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>FitPlan Pro Reminder</title>
</head>
<body style="margin:0;padding:0;background:#0a0200;font-family:'Helvetica Neue',Arial,sans-serif">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#0a0200">
<tr><td align="center" style="padding:32px 16px">
<table width="520" cellpadding="0" cellspacing="0"
       style="background:linear-gradient(135deg,#140202,#0d0408);
              border-radius:20px;overflow:hidden;
              border:1px solid rgba(229,9,20,0.35);
              box-shadow:0 20px 60px rgba(0,0,0,0.80)">

  <!-- Top accent line -->
  <tr><td style="height:3px;background:linear-gradient(90deg,#E50914,rgba(229,9,20,0.30))"></td></tr>

  <!-- Header -->
  <tr><td style="padding:32px 36px 20px;text-align:center">
    <div style="font-size:2.6rem;margin-bottom:8px">⚡</div>
    <div style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:1.6rem;
                font-weight:900;color:#E50914;letter-spacing:5px;text-transform:uppercase;
                margin-bottom:4px">FITPLAN PRO</div>
    <div style="font-size:0.78rem;color:rgba(255,255,255,0.35);letter-spacing:3px;text-transform:uppercase">
      Daily Workout Reminder</div>
  </td></tr>

  <!-- Divider -->
  <tr><td style="padding:0 36px">
    <div style="height:1px;background:linear-gradient(90deg,transparent,rgba(229,9,20,0.40),transparent)"></div>
  </td></tr>

  <!-- Main message -->
  <tr><td style="padding:28px 36px">
    <div style="font-size:1.5rem;font-weight:700;color:#fff;margin-bottom:12px">
      {subject_title}
    </div>
    <div style="font-size:1rem;color:rgba(255,255,255,0.70);line-height:1.65;margin-bottom:20px">
      Hey <strong style="color:#fff">{username}</strong>,<br><br>
      {body_message}
    </div>

    <!-- Today's session card -->
    <div style="background:rgba(229,9,20,0.10);border:1px solid rgba(229,9,20,0.30);
                border-radius:14px;padding:18px 22px;margin-bottom:24px">
      <div style="font-size:0.70rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;
                  color:rgba(229,9,20,0.75);margin-bottom:8px">TODAY'S SESSION</div>
      <div style="font-size:1.05rem;color:#fff">{session_info}</div>
    </div>

    <!-- CTA Button -->
    <div style="text-align:center;margin-bottom:8px">
      <a href="https://huggingface.co/spaces"
         style="display:inline-block;background:linear-gradient(135deg,#E50914,#c0000c);
                color:#fff;font-weight:700;font-size:1rem;padding:14px 36px;
                border-radius:12px;text-decoration:none;letter-spacing:0.5px;
                box-shadow:0 4px 20px rgba(229,9,20,0.50)">
        🏋️ {cta_text}
      </a>
    </div>
  </td></tr>

  <!-- Motivation quote -->
  <tr><td style="padding:0 36px 20px">
    <div style="background:rgba(255,255,255,0.03);border-radius:10px;padding:14px 18px;
                border-left:3px solid rgba(229,9,20,0.60)">
      <div style="font-size:0.85rem;font-style:italic;color:rgba(255,255,255,0.55)">
        "The only bad workout is the one that didn't happen."
      </div>
    </div>
  </td></tr>

  <!-- Footer -->
  <tr><td style="padding:20px 36px;text-align:center;border-top:1px solid rgba(255,255,255,0.06)">
    <div style="font-size:0.72rem;color:rgba(255,255,255,0.28);line-height:1.7">
      You're receiving this because you set a daily reminder at {reminder_time}.<br>
      To stop reminders, update your settings in FitPlan Pro.
    </div>
  </td></tr>

</table>
</td></tr>
</table>
</body>
</html>"""


def send_daily_reminder(username: str, user_data: dict,
                         session_state: dict) -> tuple[bool, str]:
    """
    Send a daily workout reminder email to the user.

    Args:
        username:      The user's display name
        user_data:     Dict with user profile (email, etc.)
        session_state: Streamlit session_state or a plain dict mirroring it

    Returns:
        (success: bool, message: str)
    """
    if not BREVO_API_KEY or not EMAIL_SENDER:
        return False, "Brevo not configured (set BREVO_API_KEY + BREVO_SENDER_EMAIL secrets)."

    to_email = user_data.get("email", "")
    if not to_email:
        return False, "No email address found for user."

    # Build today's workout info from session_state
    sdays     = session_state.get("structured_days", [])
    plan_start = session_state.get("plan_start", date.today().isoformat())
    reminder_time = "8:00 AM"
    try:
        from utils.db import get_user_setting
        _rt = get_user_setting(username, "reminder_time")
        if _rt:
            reminder_time = _rt
    except Exception:
        pass

    workout_info = {}
    if sdays:
        try:
            _ps  = date.fromisoformat(plan_start)
            _idx = (date.today() - _ps).days
            _idx = max(0, min(_idx, len(sdays) - 1))
            _day = sdays[_idx]
            workout_info = {
                "day":          _day.get("day", _idx + 1),
                "muscle_group": _day.get("muscle_group", "Workout"),
                "exercises":    len(_day.get("workout", [])),
                "is_rest":      _day.get("is_rest_day", False),
            }
        except Exception:
            pass

    subject_title, _ = _get_message_of_day()
    html_body = _build_email_html(username, workout_info, reminder_time)

    payload = json.dumps({
        "sender":      {"name": SENDER_NAME, "email": EMAIL_SENDER},
        "to":          [{"email": to_email, "name": username}],
        "subject":     f"FitPlan Pro · {subject_title}",
        "htmlContent": html_body,
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.brevo.com/v3/smtp/email",
        data=payload,
        headers={
            "accept":       "application/json",
            "api-key":      BREVO_API_KEY,
            "content-type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=12) as r:
            ok = r.status in (200, 201, 202)
            if ok:
                # Mark as sent today
                try:
                    from utils.db import save_user_setting
                    save_user_setting(username, "reminder_last_sent", date.today().isoformat())
                except Exception:
                    pass
            return ok, "Reminder sent!" if ok else f"Brevo error {r.status}"
    except urllib.error.HTTPError as e:
        return False, f"Brevo HTTP error {e.code}: {e.read().decode()[:200]}"
    except Exception as e:
        return False, str(e)


def should_send_reminder(username: str, user_data: dict,
                          session_state: dict) -> bool:
    """
    Returns True if the reminder should be sent right now.
    Logic: enabled=1, time matches current hour:minute, not yet sent today.
    Call this every ~15 minutes from a background scheduler.
    """
    try:
        from utils.db import get_user_setting
        enabled = get_user_setting(username, "reminder_enabled")
        if enabled != "1":
            return False

        reminder_time = get_user_setting(username, "reminder_time") or "08:00"
        last_sent     = get_user_setting(username, "reminder_last_sent") or ""

        # Don't send twice on the same day
        if last_sent == date.today().isoformat():
            return False

        # Check if current time matches reminder time (within 15 min window)
        now    = datetime.now()
        target = datetime.strptime(f"{date.today().isoformat()} {reminder_time}", "%Y-%m-%d %H:%M")
        diff   = abs((now - target).total_seconds())
        return diff <= 900  # within 15 minutes

    except Exception:
        return False


# ── SETTINGS UI SNIPPET ───────────────────────────────────────────────────────
# Paste this block inside your 1_Profile.py / Settings section:
"""
COPY THIS INTO pages/1_Profile.py (inside the settings expander or tab):

─────────────────────────────────────────────────────────────────────
# ── DAILY REMINDER SETTINGS ──────────────────────────────────────────────────
import streamlit as st
from utils.db import get_user_setting, save_user_setting

st.markdown(
    "<div style='font-size:0.75rem;font-weight:700;letter-spacing:3px;"
    "text-transform:uppercase;color:rgba(229,9,20,0.75);margin:18px 0 10px;"
    "display:flex;align-items:center;gap:8px'>"
    "<span style='width:14px;height:1.5px;background:#E50914;display:block'></span>"
    "⏰ Daily Reminder Email</div>",
    unsafe_allow_html=True
)

_rem_enabled_raw = get_user_setting(uname, "reminder_enabled") or "0"
_rem_time_raw    = get_user_setting(uname, "reminder_time") or "08:00"

rc1, rc2, rc3 = st.columns([2, 3, 2])
with rc1:
    rem_on = st.toggle("Enable Reminder", value=(_rem_enabled_raw == "1"), key="rem_toggle")
with rc2:
    rem_time = st.time_input("Reminder Time", value=datetime.strptime(_rem_time_raw, "%H:%M").time(),
                              key="rem_time_inp", help="When to send your daily workout reminder")
with rc3:
    if st.button("💾 Save Reminder", key="save_reminder", use_container_width=True):
        save_user_setting(uname, "reminder_enabled", "1" if rem_on else "0")
        save_user_setting(uname, "reminder_time", rem_time.strftime("%H:%M"))
        st.success("✅ Reminder saved!")
        st.rerun()

if _rem_enabled_raw == "1":
    _last = get_user_setting(uname, "reminder_last_sent") or "Never"
    st.markdown(
        f"<div style='font-size:0.78rem;color:rgba(255,255,255,0.40);margin-top:6px'>"
        f"📧 Reminder active at <b>{_rem_time_raw}</b> daily &nbsp;·&nbsp; Last sent: {_last}</div>",
        unsafe_allow_html=True
    )

# Manual send button (for testing)
if st.button("📧 Send Test Reminder Now", key="test_reminder"):
    from daily_reminder import send_daily_reminder
    _ok, _msg = send_daily_reminder(uname, data, st.session_state)
    if _ok:
        st.success("✅ Test reminder sent!")
    else:
        st.error("Failed: " + _msg)
─────────────────────────────────────────────────────────────────────
"""