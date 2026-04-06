# -*- coding: utf-8 -*-
import streamlit as st
import os, sys, json
from datetime import date, timedelta
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth_token import logout

st.set_page_config(page_title="Streaks | FitPlan Pro", page_icon="🔥",
                   layout="wide", initial_sidebar_state="collapsed")

if not st.session_state.get("logged_in"):  st.switch_page("app.py")
if "user_data" not in st.session_state:   st.switch_page("pages/1_Profile.py")

uname    = st.session_state.get("username", "Athlete")
data     = st.session_state.user_data
_dn      = data.get("display_name","").strip() or data.get("name","").strip() or uname
_display = _dn if "@" not in _dn else uname

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow+Condensed:wght@700;800;900&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700&display=swap');

html,body,.stApp,[data-testid="stAppViewContainer"]{
  background:
    radial-gradient(ellipse at 12% 8%,  rgba(251,146,60,0.22)  0%,transparent 38%),
    radial-gradient(ellipse at 88% 12%, rgba(239,68,68,0.18)   0%,transparent 35%),
    radial-gradient(ellipse at 75% 80%, rgba(251,191,36,0.14)  0%,transparent 40%),
    radial-gradient(ellipse at 15% 78%, rgba(249,115,22,0.12)  0%,transparent 35%),
    linear-gradient(160deg,#1a0a02 0%,#261200 28%,#1e0e00 58%,#160900 100%)
    !important;
  color:#fff!important;font-family:'DM Sans',sans-serif!important;}

#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stDecoration"],
[data-testid="stSidebarNav"],section[data-testid="stSidebar"]{display:none!important;}
[data-testid="stAppViewContainer"]>section>div.block-container{
  max-width:1060px!important;margin:0 auto!important;padding:0 22px 100px!important;position:relative;z-index:2;}

.nav-wrap{background:rgba(12,4,0,0.97);backdrop-filter:blur(40px);
  border-bottom:1px solid rgba(251,146,60,0.20);padding:5px 0;margin-bottom:6px;
  box-shadow:0 4px 30px rgba(0,0,0,0.70);}
.nav-logo{font-family:'Bebas Neue',sans-serif;font-size:1.4rem;letter-spacing:5px;
  color:#fb923c;text-shadow:0 0 20px rgba(251,146,60,0.55);line-height:1;}

div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"]>button{
  background:rgba(20,8,0,0.85)!important;border:1px solid rgba(251,146,60,0.22)!important;
  color:rgba(255,255,255,0.72)!important;border-radius:8px!important;
  font-size:0.78rem!important;font-weight:600!important;height:30px!important;
  min-height:30px!important;white-space:nowrap!important;transition:all 0.15s!important;box-shadow:none!important;}
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"]>button:hover{
  background:rgba(251,146,60,0.20)!important;border-color:rgba(251,146,60,0.60)!important;color:#fff!important;}
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"]:last-child>button{
  background:rgba(239,68,68,0.20)!important;border-color:rgba(239,68,68,0.45)!important;}

.stButton>button{
  background:linear-gradient(135deg,#ea580c,#dc2626)!important;
  border:none!important;color:#fff!important;border-radius:14px!important;
  font-weight:700!important;font-size:0.95rem!important;
  box-shadow:0 6px 24px rgba(234,88,12,0.50)!important;transition:all 0.22s!important;}
.stButton>button:hover{transform:translateY(-3px) scale(1.02)!important;
  box-shadow:0 10px 32px rgba(234,88,12,0.70)!important;}
.stMarkdown p{color:#fff!important;line-height:1.7!important;}
p,div,span,label{color:#fff!important;text-shadow:0 1px 4px rgba(0,0,0,0.80)!important;}
[data-testid="stWidgetLabel"],[data-testid="stWidgetLabel"] p{
  color:#fff!important;font-weight:700!important;}

@keyframes firePulse{0%,100%{text-shadow:0 0 20px rgba(251,146,60,0.80),0 0 40px rgba(239,68,68,0.50)}
  50%{text-shadow:0 0 30px rgba(251,191,36,1),0 0 60px rgba(251,146,60,0.80)}}
@keyframes fadeUp{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:translateY(0)}}
@keyframes badgePop{0%{transform:scale(0.8);opacity:0}70%{transform:scale(1.1)}100%{transform:scale(1);opacity:1}}

/* ── Mobile / Tablet responsive ─────────────────────── */
@media(max-width:900px){
  [data-testid="stAppViewContainer"]>section>div.block-container{padding:0 12px 80px!important;}
}
@media(max-width:700px){
  .stMarkdown p{font-size:0.92rem!important;}
}
</style>
""", unsafe_allow_html=True)

# ── NAV ───────────────────────────────────────────────────────────────────────
try:
    from nav_component import render_nav
    render_nav("streak", uname)
except Exception as _nav_err:
    st.warning(f"Nav error: {_nav_err}")

# ── LOAD DATA ─────────────────────────────────────────────────────────────────
today     = date.today()
today_str = today.isoformat()

@st.cache_data(ttl=300)
def load_streak(uname):
    try:
        from utils.streak_manager import get_streak_display
        return get_streak_display(uname)
    except Exception:
        try:
            from utils.db import get_streak
            return get_streak(uname)
        except Exception:
            return {"current_streak":0,"longest_streak":0,"last_completed_date":None,
                    "streak_history":[],"status":"inactive","completed_days":0,"emoji":"💤"}

@st.cache_data(ttl=300)
def load_history(uname):
    try:
        from utils.db import get_workout_history
        return get_workout_history(uname) or []
    except Exception:
        return []

streak_data  = load_streak(uname)
history      = load_history(uname)
current_st   = streak_data.get("current_streak", 0)
longest_st   = streak_data.get("longest_streak", 0)
last_done    = streak_data.get("last_completed_date")
streak_status= streak_data.get("status", "inactive")   # active / at_risk / broken / inactive
streak_emoji_txt = streak_data.get("emoji", "🔥")

# Build set of completed workout dates from history
workout_dates = set()
for h in history:
    if h.get("status") == "completed" and h.get("date"):
        workout_dates.add(h["date"])

# Calculate actual current streak from history
def calc_streak(dates_set):
    cur = 0
    d   = today
    while d.isoformat() in dates_set:
        cur += 1
        d -= timedelta(days=1)
    return cur

real_current = calc_streak(workout_dates)
total_done   = len(workout_dates)

# ── HERO ──────────────────────────────────────────────────────────────────────
flame_size = ("5rem" if real_current >= 30 else "4.2rem" if real_current >= 7 else "3.5rem")
streak_col = ("#fbbf24" if real_current >= 30 else "#fb923c" if real_current >= 7 else "#ef4444")

# Status banner
_status_banners = {
    "active":   ("✅ Streak active — keep going strong!", "#22c55e", "rgba(34,197,94,0.10)", "rgba(34,197,94,0.25)"),
    "at_risk":  ("⚠️ Streak at risk — complete today's workout to keep it alive!", "#fbbf24", "rgba(251,191,36,0.10)", "rgba(251,191,36,0.30)"),
    "broken":   ("💔 Streak broken — but every legend starts fresh. Begin again today!", "#ef4444", "rgba(239,68,68,0.10)", "rgba(239,68,68,0.25)"),
    "inactive": ("👟 No streak yet — complete your first workout to start your fire!", "#fb923c", "rgba(251,146,60,0.10)", "rgba(251,146,60,0.25)"),
}
_s_txt, _s_col, _s_bg, _s_brd = _status_banners.get(streak_status, _status_banners["inactive"])
st.markdown(f"""
<div style='background:{_s_bg};border:1px solid {_s_brd};border-radius:14px;
  padding:12px 20px;margin-bottom:20px;font-size:0.88rem;font-weight:600;color:{_s_col};
  display:flex;align-items:center;gap:10px;backdrop-filter:blur(12px);'>
  {_s_txt}
</div>""", unsafe_allow_html=True)

st.markdown(f"""
<div style='background:linear-gradient(135deg,rgba(234,88,12,0.20),rgba(153,27,27,0.12) 50%,rgba(12,4,0,0.78));
  border:1px solid rgba(251,146,60,0.32);border-radius:24px;padding:32px 36px;margin:10px 0 24px;
  position:relative;overflow:hidden;backdrop-filter:blur(30px);
  box-shadow:0 20px 60px rgba(0,0,0,0.65),inset 0 1px 0 rgba(255,180,80,0.08);'>
  <div style='position:absolute;top:0;left:0;right:0;height:2px;
    background:linear-gradient(90deg,transparent,#fb923c 25%,#fbbf24 55%,#ef4444,transparent)'></div>
  <div style='position:absolute;right:28px;top:16px;font-size:6rem;opacity:0.07;
    user-select:none;line-height:1'>🔥</div>

  <div style='font-size:0.68rem;font-weight:800;letter-spacing:3.5px;text-transform:uppercase;
    color:rgba(251,146,60,0.75);margin-bottom:10px;'>🔥 Streak Tracker</div>
  <div style='font-family:Barlow Condensed,sans-serif;font-size:clamp(2rem,5vw,3.2rem);
    font-weight:900;text-transform:uppercase;line-height:1;margin-bottom:22px;'>
    <span style='background:linear-gradient(90deg,#fdba74,#fb923c,#ef4444);
      -webkit-background-clip:text;-webkit-text-fill-color:transparent;
      background-clip:text;'>{_display}'s</span>
    <span style='color:#fff;'> Fire Log</span>
  </div>

  <div style='display:grid;grid-template-columns:auto 1fr;gap:28px;align-items:center;'>
    <!-- Big flame + streak number -->
    <div style='text-align:center;'>
      <div style='font-size:{flame_size};animation:firePulse 2s ease-in-out infinite;line-height:1'>🔥</div>
      <div style='font-family:Bebas Neue,sans-serif;font-size:4rem;color:{streak_col};
        line-height:0.9;margin-top:4px;text-shadow:0 0 30px {streak_col}80;'>{real_current}</div>
      <div style='font-size:0.62rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;
        color:rgba(255,200,120,0.55);margin-top:4px;'>day streak</div>
    </div>
    <!-- Stats grid -->
    <div style='display:grid;grid-template-columns:repeat(3,1fr);gap:10px;'>
      <div style='background:rgba(30,12,0,0.80);border:1px solid rgba(251,146,60,0.35);
        border-radius:16px;padding:14px;text-align:center;'>
        <div style='font-size:0.55rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;
          color:rgba(253,186,116,0.55);margin-bottom:5px;'>Best Streak</div>
        <div style='font-family:Bebas Neue,sans-serif;font-size:2.2rem;color:#fbbf24;line-height:1;'>
          {max(longest_st, real_current)}</div>
        <div style='font-size:0.60rem;color:rgba(255,255,255,0.30);margin-top:2px;'>days ever</div>
      </div>
      <div style='background:rgba(30,12,0,0.80);border:1px solid rgba(251,146,60,0.35);
        border-radius:16px;padding:14px;text-align:center;'>
        <div style='font-size:0.55rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;
          color:rgba(253,186,116,0.55);margin-bottom:5px;'>Total Done</div>
        <div style='font-family:Bebas Neue,sans-serif;font-size:2.2rem;color:#fb923c;line-height:1;'>
          {total_done}</div>
        <div style='font-size:0.60rem;color:rgba(255,255,255,0.30);margin-top:2px;'>workouts</div>
      </div>
      <div style='background:rgba(30,12,0,0.80);border:1px solid rgba(251,146,60,0.35);
        border-radius:16px;padding:14px;text-align:center;'>
        <div style='font-size:0.55rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;
          color:rgba(253,186,116,0.55);margin-bottom:5px;'>This Week</div>
        <div style='font-family:Bebas Neue,sans-serif;font-size:2.2rem;color:#34d399;line-height:1;'>
          {sum(1 for h in history if h.get("status")=="completed" and h.get("date","") >= (today-timedelta(days=7)).isoformat())}</div>
        <div style='font-size:0.60rem;color:rgba(255,255,255,0.30);margin-top:2px;'>sessions</div>
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── MILESTONE BADGES ──────────────────────────────────────────────────────────
st.markdown("""<div style='font-size:0.68rem;font-weight:800;letter-spacing:3px;text-transform:uppercase;
color:rgba(251,146,60,0.90);margin-bottom:12px;display:flex;align-items:center;gap:10px'>
<span>🏅 Milestone Badges</span>
<span style='flex:1;height:1px;background:linear-gradient(90deg,rgba(251,146,60,0.30),transparent);display:block'></span>
</div>""", unsafe_allow_html=True)

MILESTONES = [
    (1,   "🌱", "First Step",    "Complete day 1"),
    (7,   "🥉", "Week Warrior",  "7-day streak"),
    (14,  "⚡", "Fortnight",     "14-day streak"),
    (21,  "🔥", "3-Week Fire",   "21-day streak"),
    (30,  "🥈", "Month Beast",   "30-day streak"),
    (60,  "💎", "Diamond",       "60-day streak"),
    (90,  "🥇", "Legend",        "90-day streak"),
    (180, "👑", "Elite",         "180-day streak"),
]

badge_html = "<div style='display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px;margin-bottom:24px;'>"
for days, icon, name, desc in MILESTONES:
    earned   = max(longest_st, real_current) >= days or total_done >= days
    bg       = "rgba(251,146,60,0.15)" if earned else "rgba(25,10,0,0.75)"
    border   = "rgba(251,146,60,0.35)" if earned else "rgba(255,255,255,0.20)"
    opacity  = "1" if earned else "0.35"
    glow     = f"box-shadow:0 0 20px rgba(251,146,60,0.30);" if earned else ""
    badge_html += f"""
<div style='background:{bg};border:1px solid {border};border-radius:16px;padding:16px 12px;
  text-align:center;opacity:{opacity};{glow}transition:all 0.3s;'>
  <div style='font-size:2rem;margin-bottom:6px;{"animation:badgePop 0.5s ease both;" if earned else ""}'>{icon}</div>
  <div style='font-size:0.82rem;font-weight:700;color:#fff;font-weight:800;margin-bottom:3px;'>{name}</div>
  <div style='font-size:0.65rem;color:rgba(255,200,150,0.70);'>{desc}</div>
  {"<div style='font-size:0.60rem;color:#fb923c;margin-top:5px;font-weight:700;'>✓ EARNED</div>" if earned else f"<div style='font-size:0.60rem;color:rgba(255,200,150,0.70);margin-top:5px;'>{days - max(longest_st,real_current)} days to go</div>"}
</div>"""
badge_html += "</div>"
st.markdown(badge_html, unsafe_allow_html=True)

# ── 90-DAY HEATMAP ────────────────────────────────────────────────────────────
st.markdown("""<div style='font-size:0.68rem;font-weight:800;letter-spacing:3px;text-transform:uppercase;
color:rgba(251,146,60,0.90);margin-bottom:12px;display:flex;align-items:center;gap:10px'>
<span>📅 90-Day Activity Heatmap</span>
<span style='flex:1;height:1px;background:linear-gradient(90deg,rgba(251,146,60,0.30),transparent);display:block'></span>
</div>""", unsafe_allow_html=True)

# Build 90 days grid — 13 weeks × 7 days
days_90 = [(today - timedelta(days=89-i)) for i in range(90)]
# Pad to start on Monday
start_dow = days_90[0].weekday()  # 0=Mon
padded    = [None]*start_dow + days_90

weeks = []
week  = []
for d in padded:
    week.append(d)
    if len(week) == 7:
        weeks.append(week)
        week = []
if week:
    while len(week) < 7: week.append(None)
    weeks.append(week)

day_labels_html = "<div style='display:flex;gap:3px;margin-bottom:4px;'>"
day_labels_html += "<div style='width:28px'></div>"  # spacer for week label
for wk in weeks:
    # Show month label for first day of month in this week
    label = ""
    for d in wk:
        if d and d.day == 1:
            label = d.strftime("%b")
            break
        elif d and d == days_90[0]:
            label = d.strftime("%b")
            break
    day_labels_html += f"<div style='width:18px;font-size:0.55rem;color:rgba(255,255,255,0.30);text-align:center'>{label}</div>"
day_labels_html += "</div>"

grid_html = "<div style='background:rgba(15,6,0,0.70);border:1px solid rgba(251,146,60,0.15);border-radius:18px;padding:20px 22px;backdrop-filter:blur(20px);'>"
grid_html += day_labels_html
grid_html += "<div style='display:flex;gap:3px;'>"

# Day-of-week labels
dow_labels = ["Mon","","Wed","","Fri","","Sun"]
grid_html += "<div style='display:flex;flex-direction:column;gap:3px;margin-right:4px;'>"
for lbl in dow_labels:
    grid_html += f"<div style='height:18px;font-size:0.50rem;color:rgba(255,200,150,0.60);display:flex;align-items:center;'>{lbl}</div>"
grid_html += "</div>"

for wk in weeks:
    grid_html += "<div style='display:flex;flex-direction:column;gap:3px;'>"
    for d in wk:
        if d is None:
            grid_html += "<div style='width:18px;height:18px;'></div>"
        else:
            ds     = d.isoformat()
            done   = ds in workout_dates
            is_td  = ds == today_str
            future = d > today
            if future:
                col, brd, tip = "rgba(20,8,0,0.60)", "rgba(255,255,255,0.08)", ""
            elif done:
                # Intensity based on how recent
                days_ago = (today - d).days
                alpha    = max(0.5, 1.0 - days_ago * 0.005)
                col  = f"rgba(251,146,60,{alpha:.2f})"
                brd  = f"rgba(251,146,60,{min(alpha+0.2,1):.2f})"
                tip  = "✓"
            else:
                col, brd, tip = "rgba(35,15,2,0.85)", "rgba(255,180,80,0.18)", ""
            outline = "outline:2px solid #fff;outline-offset:1px;" if is_td else ""
            grid_html += f"<div title='{ds} {tip}' style='width:18px;height:18px;border-radius:4px;background:{col};border:1px solid {brd};{outline}'></div>"
    grid_html += "</div>"

grid_html += "</div>"
# Legend
grid_html += """<div style='display:flex;align-items:center;gap:10px;margin-top:12px;justify-content:flex-end;'>
  <span style='font-size:0.62rem;color:rgba(255,200,150,0.65);'>Less</span>
  <div style='width:14px;height:14px;border-radius:3px;background:rgba(40,20,5,0.70);'></div>
  <div style='width:14px;height:14px;border-radius:3px;background:rgba(251,146,60,0.35);'></div>
  <div style='width:14px;height:14px;border-radius:3px;background:rgba(251,146,60,0.65);'></div>
  <div style='width:14px;height:14px;border-radius:3px;background:rgba(251,146,60,0.90);'></div>
  <span style='font-size:0.62rem;color:rgba(255,255,255,0.30);'>More</span>
  <span style='font-size:0.62rem;color:rgba(255,200,150,0.65);margin-left:8px;'>■ Today</span>
</div>"""
grid_html += "</div>"
st.markdown(grid_html, unsafe_allow_html=True)

# ── WEEKLY COMPLETION RINGS ───────────────────────────────────────────────────
st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
st.markdown("""<div style='font-size:0.68rem;font-weight:800;letter-spacing:3px;text-transform:uppercase;
color:rgba(251,146,60,0.60);margin-bottom:14px;display:flex;align-items:center;gap:10px'>
<span>📊 Last 8 Weeks</span>
<span style='flex:1;height:1px;background:linear-gradient(90deg,rgba(251,146,60,0.30),transparent);display:block'></span>
</div>""", unsafe_allow_html=True)

target_per_week = data.get("days_per_week", 5)
week_bars = "<div style='display:grid;grid-template-columns:repeat(8,1fr);gap:8px;'>"
for w in range(7, -1, -1):
    wk_start = today - timedelta(days=today.weekday() + w*7)
    wk_dates  = [(wk_start + timedelta(days=d)).isoformat() for d in range(7)]
    done_w    = sum(1 for d in wk_dates if d in workout_dates)
    pct       = min(100, int(done_w / max(target_per_week, 1) * 100))
    col       = ("#22c55e" if pct >= 100 else "#fb923c" if pct >= 60 else "#ef4444" if pct > 0 else "rgba(40,20,5,0.70)")
    lbl       = "This week" if w == 0 else f"{w}w ago"
    week_bars += f"""
<div style='text-align:center;'>
  <div style='font-size:0.62rem;font-weight:600;color:{col};margin-bottom:5px;'>{done_w}/{target_per_week}</div>
  <div style='background:rgba(25,10,0,0.80);border-radius:8px;height:80px;
    display:flex;align-items:flex-end;overflow:hidden;'>
    <div style='width:100%;height:{max(pct,4)}%;background:{col};border-radius:8px 8px 0 0;
      transition:height 0.5s ease;'></div>
  </div>
  <div style='font-size:0.55rem;color:rgba(255,255,255,0.30);margin-top:5px;'>{lbl}</div>
</div>"""
week_bars += "</div>"
st.markdown(f"<div style='background:rgba(15,6,0,0.70);border:1px solid rgba(251,146,60,0.15);border-radius:18px;padding:20px 22px;backdrop-filter:blur(20px);'>{week_bars}</div>", unsafe_allow_html=True) 