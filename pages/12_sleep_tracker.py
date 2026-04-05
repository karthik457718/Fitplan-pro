# -*- coding: utf-8 -*-
import streamlit as st
import os, sys
from datetime import date, timedelta
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth_token import logout

st.set_page_config(page_title="Sleep Tracker | FitPlan Pro", page_icon="😴",
                   layout="wide", initial_sidebar_state="collapsed")

if not st.session_state.get("logged_in"):    st.switch_page("app.py")
if "user_data" not in st.session_state:      st.switch_page("pages/1_Profile.py")

uname = st.session_state.get("username", "Athlete")
data  = st.session_state.user_data
_dn   = data.get("display_name","").strip() or data.get("name","").strip() or uname
_display = _dn if "@" not in _dn else uname

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow+Condensed:wght@700;800;900&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700&display=swap');

html,body,.stApp,[data-testid="stAppViewContainer"]{
  background:
    radial-gradient(ellipse at 15% 10%, rgba(99,60,220,0.22) 0%,transparent 45%),
    radial-gradient(ellipse at 85% 15%, rgba(59,130,246,0.15) 0%,transparent 40%),
    radial-gradient(ellipse at 90% 80%, rgba(139,92,246,0.12) 0%,transparent 40%),
    radial-gradient(ellipse at 10% 85%, rgba(30,20,60,0.80)   0%,transparent 50%),
    linear-gradient(160deg,#06040f 0%,#09061a 35%,#070414 65%,#05030e 100%)
    !important;
  color:#fff!important;font-family:'DM Sans',sans-serif!important;}

#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stDecoration"],
[data-testid="stSidebarNav"],section[data-testid="stSidebar"]{display:none!important;}

[data-testid="stAppViewContainer"]>section>div.block-container{
  max-width:1000px!important;margin:0 auto!important;padding:0 22px 100px!important;}

/* NAV */
.nav-wrap{background:rgba(6,4,15,0.97);backdrop-filter:blur(36px);
  border-bottom:1.5px solid rgba(99,60,220,0.25);padding:5px 0;margin-bottom:4px;}
.nav-logo{font-family:'Bebas Neue',sans-serif;font-size:1.4rem;letter-spacing:5px;
  color:#a78bfa;text-shadow:0 0 18px rgba(167,139,250,0.45);line-height:1;}

div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"]>button{
  background:rgba(10,6,24,0.90)!important;border:1px solid rgba(99,60,220,0.30)!important;
  color:rgba(255,255,255,0.75)!important;border-radius:8px!important;
  font-size:0.80rem!important;font-weight:600!important;height:30px!important;
  min-height:30px!important;white-space:nowrap!important;transition:all 0.15s!important;
  box-shadow:none!important;}
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"]>button:hover{
  background:rgba(99,60,220,0.20)!important;border-color:rgba(99,60,220,0.70)!important;color:#fff!important;}
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"]:last-child>button{
  background:rgba(229,9,20,0.18)!important;border-color:rgba(229,9,20,0.45)!important;}

/* GENERAL BUTTONS */
.stButton>button{
  background:linear-gradient(135deg,#6b3bdc,#3b82f6)!important;
  border:none!important;color:#fff!important;border-radius:12px!important;
  font-weight:700!important;font-size:0.92rem!important;
  box-shadow:0 4px 18px rgba(99,60,220,0.40)!important;transition:all 0.22s!important;}
.stButton>button:hover{transform:translateY(-2px) scale(1.02)!important;
  box-shadow:0 8px 26px rgba(99,60,220,0.60)!important;}

/* INPUTS */
[data-testid="stWidgetLabel"],[data-testid="stWidgetLabel"] p{
  color:rgba(255,255,255,0.80)!important;font-size:0.88rem!important;
  font-weight:600!important;letter-spacing:1.5px!important;text-transform:uppercase!important;}
.stSlider [data-testid="stWidgetLabel"] p{color:rgba(255,255,255,0.80)!important;}
input,.stTextArea textarea{background:#0d0a1e!important;
  border:1.5px solid rgba(99,60,220,0.30)!important;color:#fff!important;border-radius:10px!important;}
.stSelectbox [data-baseweb="select"]>div{background:#0d0a1e!important;
  border:1.5px solid rgba(99,60,220,0.30)!important;color:#fff!important;}
.stMarkdown p{color:rgba(255,255,255,0.80)!important;}
</style>
""", unsafe_allow_html=True)

# ── NAV ───────────────────────────────────────────────────────────────────────
st.markdown("<div class='nav-wrap'>", unsafe_allow_html=True)
_n = st.columns([1.6,1,1,1,1,1,1,1,1,1.2])
with _n[0]: st.markdown("<div class='nav-logo'>⚡ FITPLAN PRO</div>", unsafe_allow_html=True)
for idx, (lbl, pg, key) in enumerate([
    ("🏠 Home",    "pages/2_Dashboard.py",       "sl_db"),
    ("⚡ Workout", "pages/3_Workout_Plan.py",    "sl_wp"),
    ("🥗 Diet",    "pages/4_Diet_Plan.py",        "sl_dp"),
    ("🍽️ Meals",  "pages/11_meal_planner.py",   "sl_mp"),
    ("😴 Sleep",   "pages/12_sleep_tracker.py",  "sl_sl"),
    ("🏃 Cardio",  "pages/13_cardio_tracker.py", "sl_ca"),
    ("🤖 Coach",   "pages/5_ai_coach.py",         "sl_ai"),
    ("🏆 Records", "pages/6_records.py",          "sl_rc"),
]):
    with _n[idx+1]:
        if st.button(lbl, key=key, use_container_width=True):
            try: st.switch_page(pg)
            except Exception: pass
with _n[9]:
    if st.button("🚪 Sign Out", key="sl_so", use_container_width=True):
        logout(uname)
        for k in ["logged_in","username","auth_token","user_data","workout_plan","structured_days",
                  "dietary_type","full_plan_data","plan_id","force_regen","tracking","_plan_checked"]:
            st.session_state.pop(k, None)
        st.switch_page("app.py")
st.markdown("</div>", unsafe_allow_html=True)

# ── LOAD DATA ─────────────────────────────────────────────────────────────────
today     = date.today()
today_str = today.isoformat()

if "sleep_log" not in st.session_state:
    try:
        from utils.db import get_sleep
        st.session_state.sleep_log = get_sleep(uname, limit=30)
    except Exception:
        st.session_state.sleep_log = []

sleep_log = st.session_state.sleep_log

# Today's entry
today_entry = next((s for s in sleep_log if s.get("date") == today_str), None)

# ── HERO ──────────────────────────────────────────────────────────────────────
avg_hrs  = round(sum(s["hours"] for s in sleep_log[:7]) / max(len(sleep_log[:7]),1), 1) if sleep_log else 0
avg_qual = round(sum(s["quality"] for s in sleep_log[:7]) / max(len(sleep_log[:7]),1), 1) if sleep_log else 0
streak_s = 0
for i in range(len(sleep_log)):
    exp = (today - timedelta(days=i)).isoformat()
    if i < len(sleep_log) and sleep_log[i].get("date") == exp:
        streak_s += 1
    else:
        break

quality_label = ("💀 Critical" if avg_qual < 2 else "😴 Poor" if avg_qual < 3
                 else "😐 Fair" if avg_qual < 4 else "😊 Good" if avg_qual < 4.5 else "🌟 Excellent")
hrs_color = "#E50914" if avg_hrs < 6 else "#f59e0b" if avg_hrs < 7 else "#22c55e"

st.markdown(f"""
<div style='background:linear-gradient(135deg,rgba(99,60,220,0.16),rgba(59,130,246,0.08) 50%,rgba(6,4,15,0.70));
  border:1.5px solid rgba(99,60,220,0.40);border-radius:20px;padding:26px 32px;margin:10px 0 20px;
  position:relative;overflow:hidden;backdrop-filter:blur(20px);'>
  <div style='position:absolute;top:0;left:0;right:0;height:2px;
    background:linear-gradient(90deg,transparent,#6b3bdc 35%,#3b82f6 65%,transparent)'></div>
  <div style='position:absolute;top:-40px;right:-40px;width:180px;height:180px;border-radius:50%;
    background:radial-gradient(circle,rgba(99,60,220,0.20) 0%,transparent 70%);pointer-events:none'></div>
  <div style='font-size:0.72rem;font-weight:800;letter-spacing:3px;text-transform:uppercase;
    color:rgba(167,139,250,0.80);margin-bottom:8px'>😴 Sleep Tracker</div>
  <div style='font-family:Barlow Condensed,sans-serif;font-size:clamp(1.8rem,4vw,2.8rem);
    font-weight:900;text-transform:uppercase;color:#fff;line-height:1;margin-bottom:6px'>
    <span style='color:#a78bfa'>{_display}'s</span> Sleep Dashboard
  </div>
  <div style='display:flex;gap:24px;margin-top:16px;flex-wrap:wrap'>
    <div style='text-align:center'>
      <div style='font-family:Bebas Neue,sans-serif;font-size:2.4rem;color:{hrs_color};line-height:1'>{avg_hrs}h</div>
      <div style='font-size:0.60rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.40)'>7-day avg</div>
    </div>
    <div style='width:1px;background:rgba(255,255,255,0.10)'></div>
    <div style='text-align:center'>
      <div style='font-family:Bebas Neue,sans-serif;font-size:2.4rem;color:#a78bfa;line-height:1'>{avg_qual}/5</div>
      <div style='font-size:0.60rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.40)'>quality · {quality_label}</div>
    </div>
    <div style='width:1px;background:rgba(255,255,255,0.10)'></div>
    <div style='text-align:center'>
      <div style='font-family:Bebas Neue,sans-serif;font-size:2.4rem;color:#60a5fa;line-height:1'>{streak_s}</div>
      <div style='font-size:0.60rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.40)'>day streak</div>
    </div>
    <div style='width:1px;background:rgba(255,255,255,0.10)'></div>
    <div style='text-align:center'>
      <div style='font-family:Bebas Neue,sans-serif;font-size:2.4rem;color:#34d399;line-height:1'>{len(sleep_log)}</div>
      <div style='font-size:0.60rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.40)'>nights logged</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── LOG + CHART COLUMNS ───────────────────────────────────────────────────────
col_log, col_chart = st.columns([1, 1.4], gap="large")

# ── LOG FORM ──────────────────────────────────────────────────────────────────
with col_log:
    already_logged = today_entry is not None
    border_col = "rgba(34,197,94,0.40)" if already_logged else "rgba(99,60,220,0.35)"
    top_col    = "#22c55e" if already_logged else "#6b3bdc"

    st.markdown(f"""
<div style='background:rgba(8,5,20,0.90);border:1.5px solid {border_col};border-radius:18px;
  padding:20px 24px;position:relative;overflow:hidden;backdrop-filter:blur(20px);margin-bottom:16px'>
  <div style='position:absolute;top:0;left:0;right:0;height:2px;
    background:linear-gradient(90deg,transparent,{top_col},transparent)'></div>
  <div style='font-size:0.68rem;font-weight:800;letter-spacing:2.5px;text-transform:uppercase;
    color:{"rgba(34,197,94,0.80)" if already_logged else "rgba(167,139,250,0.80)"};margin-bottom:14px'>
    {"✅ Tonight Logged" if already_logged else "🌙 Log Tonight's Sleep"}
  </div>
""", unsafe_allow_html=True)

    _log_date = st.date_input("Date", value=today, max_value=today,
                               min_value=today - timedelta(days=30), key="sl_date")
    _hours = st.slider("Hours slept", min_value=0.0, max_value=14.0,
                       value=float(today_entry["hours"]) if today_entry else 7.0,
                       step=0.5, key="sl_hours",
                       help="Drag to set hours slept")

    # Quality stars
    st.markdown("<div style='font-size:0.88rem;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;color:rgba(255,255,255,0.80);margin-bottom:6px'>Sleep Quality</div>", unsafe_allow_html=True)
    _quality_map = {"😴 Poor (1)":1,"😐 Fair (2)":2,"🙂 Okay (3)":3,"😊 Good (4)":4,"🌟 Excellent (5)":5}
    _default_q = today_entry["quality"] if today_entry else 3
    _default_label = [k for k,v in _quality_map.items() if v == _default_q][0]
    _quality_label = st.selectbox("Quality", list(_quality_map.keys()),
                                   index=list(_quality_map.keys()).index(_default_label),
                                   key="sl_quality", label_visibility="collapsed")
    _quality = _quality_map[_quality_label]

    # Quality stars display
    stars = "⭐" * _quality + "☆" * (5 - _quality)
    st.markdown(f"<div style='font-size:1.4rem;margin:4px 0 10px'>{stars}</div>", unsafe_allow_html=True)

    _notes = st.text_input("Notes (optional)", value=today_entry.get("notes","") if today_entry else "",
                            placeholder="e.g. woke up twice, vivid dreams...",
                            key="sl_notes")

    # Sleep quality tip
    tip_map = {
        1:"🔴 Less than 5h — your body needs emergency rest. Skip intense workouts today.",
        2:"🟠 5–6h — recovery is compromised. Consider lighter training.",
        3:"🟡 6–7h — adequate but not optimal. Stay hydrated.",
        4:"🟢 7–8h — good sleep! You're ready to train hard.",
        5:"⭐ 8h+ — peak recovery. Perfect day to set a PR!"
    }
    if _hours > 0:
        bucket = 1 if _hours < 5 else 2 if _hours < 6 else 3 if _hours < 7 else 4 if _hours < 8 else 5
        st.markdown(f"<div style='background:rgba(99,60,220,0.10);border:1px solid rgba(99,60,220,0.22);border-radius:10px;padding:10px 14px;font-size:0.80rem;color:rgba(255,255,255,0.65);margin-top:8px;line-height:1.5'>{tip_map[bucket]}</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    if st.button("💾 Save Sleep Entry", key="sl_save", use_container_width=True):
        try:
            from utils.db import save_sleep, get_sleep
            save_sleep(uname, _log_date.isoformat(), _hours, _quality, _notes)
            st.session_state.sleep_log = get_sleep(uname, limit=30)
            st.toast("✅ Sleep logged!", icon="😴")
            st.rerun()
        except Exception as e:
            st.error(f"Save failed: {e}")

# ── 7-DAY CHART ───────────────────────────────────────────────────────────────
with col_chart:
    st.markdown(f"""
<div style='background:rgba(8,5,20,0.90);border:1.5px solid rgba(99,60,220,0.28);border-radius:18px;
  padding:20px 24px;backdrop-filter:blur(20px);position:relative;overflow:hidden'>
  <div style='position:absolute;top:0;left:0;right:0;height:2px;
    background:linear-gradient(90deg,transparent,#3b82f6,transparent)'></div>
  <div style='font-size:0.68rem;font-weight:800;letter-spacing:2.5px;text-transform:uppercase;
    color:rgba(96,165,250,0.80);margin-bottom:16px'>📊 Last 7 Nights</div>
""", unsafe_allow_html=True)

    # Build 7-day data
    days7 = []
    for i in range(6, -1, -1):
        d = (today - timedelta(days=i)).isoformat()
        entry = next((s for s in sleep_log if s.get("date") == d), None)
        days7.append({"date": d, "hours": entry["hours"] if entry else 0,
                      "quality": entry["quality"] if entry else 0,
                      "logged": entry is not None})

    max_h = max((d["hours"] for d in days7), default=8)
    max_h = max(max_h, 8)

    bars_html = "<div style='display:flex;align-items:flex-end;gap:8px;height:160px;margin-bottom:10px'>"
    for d in days7:
        h    = d["hours"]
        pct  = int(h / max_h * 100) if h > 0 else 0
        day  = date.fromisoformat(d["date"]).strftime("%a")
        istoday = d["date"] == today_str
        col  = ("#22c55e" if h >= 8 else "#a78bfa" if h >= 7 else
                "#f59e0b" if h >= 6 else "#ef4444" if h > 0 else "rgba(255,255,255,0.08)")
        border = f"border:2px solid #fff;" if istoday else ""
        bars_html += f"""
<div style='flex:1;display:flex;flex-direction:column;align-items:center;gap:4px'>
  <div style='font-size:0.65rem;color:rgba(255,255,255,0.50);font-weight:600'>
    {f"{h}h" if h > 0 else "–"}</div>
  <div style='width:100%;background:rgba(255,255,255,0.06);border-radius:6px 6px 0 0;
    display:flex;align-items:flex-end;flex:1'>
    <div style='width:100%;height:{max(pct,3)}%;background:{col};border-radius:6px 6px 0 0;
      {border}transition:height 0.5s;'></div>
  </div>
  <div style='font-size:0.68rem;font-weight:{"800" if istoday else "500"};
    color:{"#a78bfa" if istoday else "rgba(255,255,255,0.40)"}'>{day}</div>
</div>"""

    bars_html += "</div>"

    # Legend
    bars_html += """<div style='display:flex;gap:12px;flex-wrap:wrap;margin-top:4px'>
  <div style='display:flex;align-items:center;gap:5px'>
    <div style='width:10px;height:10px;border-radius:2px;background:#22c55e'></div>
    <span style='font-size:0.68rem;color:rgba(255,255,255,0.45)'>8h+ optimal</span></div>
  <div style='display:flex;align-items:center;gap:5px'>
    <div style='width:10px;height:10px;border-radius:2px;background:#a78bfa'></div>
    <span style='font-size:0.68rem;color:rgba(255,255,255,0.45)'>7–8h good</span></div>
  <div style='display:flex;align-items:center;gap:5px'>
    <div style='width:10px;height:10px;border-radius:2px;background:#f59e0b'></div>
    <span style='font-size:0.68rem;color:rgba(255,255,255,0.45)'>6–7h fair</span></div>
  <div style='display:flex;align-items:center;gap:5px'>
    <div style='width:10px;height:10px;border-radius:2px;background:#ef4444'></div>
    <span style='font-size:0.68rem;color:rgba(255,255,255,0.45)'>&lt;6h poor</span></div>
</div>"""
    st.markdown(bars_html + "</div>", unsafe_allow_html=True)

# ── SLEEP HISTORY TABLE ───────────────────────────────────────────────────────
if sleep_log:
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    st.markdown("""<div style='font-size:0.68rem;font-weight:800;letter-spacing:3px;text-transform:uppercase;
color:rgba(167,139,250,0.60);margin-bottom:10px;display:flex;align-items:center;gap:10px'>
<span>🕐 Recent Nights</span>
<span style='flex:1;height:1px;background:linear-gradient(90deg,rgba(99,60,220,0.30),transparent);display:block'></span>
</div>""", unsafe_allow_html=True)

    rows_html = ""
    for s in sleep_log[:14]:
        d       = s.get("date","")
        h       = s.get("hours", 0)
        q       = s.get("quality", 0)
        notes   = s.get("notes","") or ""
        stars   = "⭐"*q + "☆"*(5-q)
        h_col   = "#22c55e" if h>=8 else "#a78bfa" if h>=7 else "#f59e0b" if h>=6 else "#ef4444"
        label   = ("Excellent" if q==5 else "Good" if q==4 else "Okay" if q==3 else "Poor" if q==2 else "Bad")
        try:
            dobj  = date.fromisoformat(d)
            ddisp = dobj.strftime("%d %b %Y")
            if dobj == today: ddisp = "Today"
            elif dobj == today - timedelta(days=1): ddisp = "Yesterday"
        except: ddisp = d
        rows_html += f"""
<div style='display:flex;align-items:center;gap:16px;background:rgba(8,5,20,0.80);
  border:1px solid rgba(99,60,220,0.15);border-radius:12px;padding:12px 18px;margin-bottom:8px;
  backdrop-filter:blur(12px)'>
  <div style='min-width:90px'>
    <div style='font-size:0.80rem;font-weight:600;color:rgba(255,255,255,0.80)'>{ddisp}</div>
    <div style='font-size:0.65rem;color:rgba(255,255,255,0.35)'>{d}</div>
  </div>
  <div style='min-width:60px;text-align:center'>
    <div style='font-family:Bebas Neue,sans-serif;font-size:1.6rem;color:{h_col};line-height:1'>{h}h</div>
  </div>
  <div style='min-width:80px'>
    <div style='font-size:0.85rem'>{stars}</div>
    <div style='font-size:0.65rem;color:rgba(255,255,255,0.40)'>{label}</div>
  </div>
  <div style='flex:1;font-size:0.78rem;color:rgba(255,255,255,0.45);font-style:italic'>
    {notes if notes else "—"}</div>
</div>"""
    st.markdown(rows_html, unsafe_allow_html=True)