"""
weekly_email.py — Weekly progress summary email sender via Brevo.
Call send_weekly_summary(username, user_data, session_state) every Sunday
or trigger manually from Dashboard.
"""
import os, json, requests
from datetime import date, timedelta

BREVO_API_KEY   = os.getenv("BREVO_API_KEY", "").strip()
BREVO_SENDER    = os.getenv("BREVO_SENDER_EMAIL", "noreply@fitplanpro.com").strip()
BREVO_SENDER_NAME = "FitPlan Pro"


def _build_email_html(uname, stats, plan_info, week_str):
    """Build a beautiful HTML email for weekly summary."""
    done    = stats.get("done", 0)
    total   = stats.get("total", 0)
    missed  = stats.get("missed", 0)
    streak  = stats.get("streak", 0)
    water   = stats.get("avg_water", 0)
    pct     = int(done / max(total, 1) * 100)
    diet_t  = plan_info.get("dietary_type", "veg")
    goal    = plan_info.get("goal", "Fitness")

    if pct >= 80:
        grade, grade_color, grade_msg = "A", "#22c55e", "Outstanding week! You're crushing it! 🔥"
    elif pct >= 60:
        grade, grade_color, grade_msg = "B", "#60a5fa", "Good effort! Keep pushing! 💪"
    elif pct >= 40:
        grade, grade_color, grade_msg = "C", "#fbbf24", "Room to improve. You've got this! 🌟"
    else:
        grade, grade_color, grade_msg = "D", "#ef4444", "Tough week. Tomorrow is a fresh start! 🌅"

    return f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>FitPlan Pro — Weekly Summary</title>
</head>
<body style="margin:0;padding:0;background:#0a0604;font-family:'DM Sans',Arial,sans-serif;color:#fff;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#0a0604;padding:24px 0">
<tr><td align="center">
<table width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%">

  <!-- HEADER -->
  <tr><td style="background:linear-gradient(135deg,#1a0608,#0d0408);border:1px solid rgba(229,9,20,0.30);border-radius:16px 16px 0 0;padding:32px 36px;text-align:center">
    <div style="font-size:2rem;margin-bottom:8px">⚡</div>
    <div style="font-size:1.4rem;font-weight:900;letter-spacing:4px;color:#E50914;text-transform:uppercase">FitPlan Pro</div>
    <div style="font-size:0.85rem;color:rgba(255,255,255,0.50);margin-top:4px">Weekly Progress Summary</div>
    <div style="font-size:0.80rem;color:rgba(255,255,255,0.35);margin-top:2px">{week_str}</div>
  </td></tr>

  <!-- GRADE -->
  <tr><td style="background:#0f0608;border-left:1px solid rgba(229,9,20,0.20);border-right:1px solid rgba(229,9,20,0.20);padding:28px 36px;text-align:center">
    <div style="font-size:0.75rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:rgba(229,9,20,0.65);margin-bottom:8px">THIS WEEK'S GRADE</div>
    <div style="font-size:5rem;font-weight:900;color:{grade_color};line-height:1">{grade}</div>
    <div style="font-size:1rem;color:rgba(255,255,255,0.70);margin-top:8px">Hey {uname}, {grade_msg}</div>
  </td></tr>

  <!-- STATS -->
  <tr><td style="background:#0f0608;border-left:1px solid rgba(229,9,20,0.20);border-right:1px solid rgba(229,9,20,0.20);padding:0 36px 24px">
    <table width="100%" cellpadding="0" cellspacing="0">
    <tr>
      <td width="25%" style="text-align:center;padding:12px 8px;background:rgba(229,9,20,0.08);border:1px solid rgba(229,9,20,0.18);border-radius:12px;margin:4px">
        <div style="font-size:2rem;font-weight:900;color:#22c55e">{done}</div>
        <div style="font-size:0.65rem;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.45);margin-top:3px">Workouts Done</div>
      </td>
      <td width="4%"></td>
      <td width="25%" style="text-align:center;padding:12px 8px;background:rgba(229,9,20,0.08);border:1px solid rgba(229,9,20,0.18);border-radius:12px">
        <div style="font-size:2rem;font-weight:900;color:#ef4444">{missed}</div>
        <div style="font-size:0.65rem;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.45);margin-top:3px">Missed</div>
      </td>
      <td width="4%"></td>
      <td width="25%" style="text-align:center;padding:12px 8px;background:rgba(229,9,20,0.08);border:1px solid rgba(229,9,20,0.18);border-radius:12px">
        <div style="font-size:2rem;font-weight:900;color:#fbbf24">{pct}%</div>
        <div style="font-size:0.65rem;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.45);margin-top:3px">Consistency</div>
      </td>
      <td width="4%"></td>
      <td width="25%" style="text-align:center;padding:12px 8px;background:rgba(229,9,20,0.08);border:1px solid rgba(229,9,20,0.18);border-radius:12px">
        <div style="font-size:2rem;font-weight:900;color:#60a5fa">{streak}</div>
        <div style="font-size:0.65rem;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.45);margin-top:3px">Day Streak</div>
      </td>
    </tr>
    </table>
  </td></tr>

  <!-- PROGRESS BAR -->
  <tr><td style="background:#0f0608;border-left:1px solid rgba(229,9,20,0.20);border-right:1px solid rgba(229,9,20,0.20);padding:0 36px 28px">
    <div style="font-size:0.72rem;color:rgba(255,255,255,0.40);margin-bottom:6px">Weekly completion: {done}/{total} workouts</div>
    <div style="height:10px;background:rgba(255,255,255,0.08);border-radius:5px;overflow:hidden">
      <div style="height:100%;width:{pct}%;background:linear-gradient(90deg,#E50914,{'#22c55e' if pct>=80 else '#fbbf24'});border-radius:5px"></div>
    </div>
    <div style="margin-top:10px;font-size:0.78rem;color:rgba(255,255,255,0.45)">
      💧 Avg water intake: {water}/8 glasses &nbsp;·&nbsp; 🎯 Goal: {goal}
    </div>
  </td></tr>

  <!-- MOTIVATION -->
  <tr><td style="background:linear-gradient(135deg,rgba(229,9,20,0.12),rgba(10,6,2,0.95));border-left:1px solid rgba(229,9,20,0.20);border-right:1px solid rgba(229,9,20,0.20);padding:20px 36px;text-align:center">
    <div style="font-size:1.1rem;color:rgba(255,255,255,0.80);line-height:1.6;font-style:italic">
      "The only bad workout is the one that didn't happen."
    </div>
    <div style="font-size:0.75rem;color:rgba(229,9,20,0.60);margin-top:6px">— FitPlan Pro</div>
  </td></tr>

  <!-- CTA -->
  <tr><td style="background:#0f0608;border-left:1px solid rgba(229,9,20,0.20);border-right:1px solid rgba(229,9,20,0.20);padding:24px 36px;text-align:center">
    <a href="https://huggingface.co/spaces/LakshmiNandaS/FitPlanAI_PLAN_dulpicate"
       style="display:inline-block;background:linear-gradient(135deg,#E50914,#c0000c);color:#fff;
       font-weight:700;font-size:1rem;padding:12px 32px;border-radius:10px;text-decoration:none;
       letter-spacing:1px">View My Dashboard →</a>
  </td></tr>

  <!-- FOOTER -->
  <tr><td style="background:#080404;border:1px solid rgba(229,9,20,0.15);border-radius:0 0 16px 16px;padding:18px 36px;text-align:center">
    <div style="font-size:0.72rem;color:rgba(255,255,255,0.25);line-height:1.6">
      FitPlan Pro · AI-Powered Fitness<br>
      This email was sent because you have a FitPlan Pro account.<br>
      Week of {week_str}
    </div>
  </td></tr>

</table>
</td></tr>
</table>
</body>
</html>
"""


def send_weekly_summary(username, user_data, session_state, to_email=None):
    """
    Send weekly workout summary email via Brevo.
    Returns (success: bool, message: str)
    """
    if not BREVO_API_KEY:
        return False, "BREVO_API_KEY not set in environment secrets."

    # ── Gather stats ──────────────────────────────────────────────────────────
    from datetime import date as _date, timedelta as _td
    today       = _date.today()
    week_start  = today - _td(days=today.weekday())   # Monday
    week_end    = week_start + _td(days=6)
    week_str    = f"{week_start.strftime('%b %d')} – {week_end.strftime('%b %d, %Y')}"

    tracking    = session_state.get("tracking", {})
    sdays       = session_state.get("structured_days", [])
    plan_start_str = session_state.get("plan_start", str(today))
    try:
        plan_start = _date.fromisoformat(plan_start_str)
    except Exception:
        plan_start = today

    done = missed = total = 0
    for i, sd in enumerate(sdays):
        work_date = plan_start + _td(days=i)
        if week_start <= work_date <= week_end and not sd.get("is_rest_day"):
            total += 1
            status = tracking.get(work_date.isoformat(), {}).get("status", "")
            if status == "done":
                done += 1
            elif work_date < today:
                missed += 1

    # Streak
    streak = 0
    try:
        from utils.db import get_streak
        _s = get_streak(username)
        streak = _s.get("current_streak", 0)
    except Exception:
        pass

    # Avg water this week
    avg_water = 0
    try:
        from utils.db import get_water
        waters = []
        for d in range(7):
            _d = (week_start + _td(days=d)).isoformat()
            w  = get_water(username, _d)
            if w > 0: waters.append(w)
        avg_water = round(sum(waters)/len(waters), 1) if waters else 0
    except Exception:
        pass

    stats = {
        "done": done, "total": total, "missed": missed,
        "streak": streak, "avg_water": avg_water
    }
    plan_info = {
        "dietary_type": session_state.get("dietary_type", "veg"),
        "goal":         user_data.get("goal", "Fitness"),
    }

    # ── Recipient email ───────────────────────────────────────────────────────
    if not to_email:
        # Try to get from DB
        try:
            from utils.db import get_user_setting
            to_email = get_user_setting(username, "email")
        except Exception:
            pass
    if not to_email:
        return False, "No email address found. Please set your email in Settings."

    # ── Build & send ──────────────────────────────────────────────────────────
    html_body = _build_email_html(username, stats, plan_info, week_str)

    payload = {
        "sender":     {"name": BREVO_SENDER_NAME, "email": BREVO_SENDER},
        "to":         [{"email": to_email, "name": username}],
        "subject":    f"⚡ {username}'s Weekly FitPlan Summary — {week_str}",
        "htmlContent": html_body,
    }

    try:
        r = requests.post(
            "https://api.brevo.com/v3/smtp/email",
            headers={
                "api-key":      BREVO_API_KEY,
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=12
        )
        if r.ok:
            return True, f"✅ Weekly summary sent to {to_email}!"
        else:
            return False, f"Brevo error {r.status_code}: {r.text[:200]}"
    except Exception as e:
        return False, f"Send failed: {str(e)}"