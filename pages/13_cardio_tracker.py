# -*- coding: utf-8 -*-
import streamlit as st
import os, sys
from datetime import date, timedelta
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth_token import logout

st.set_page_config(page_title="Cardio Tracker | FitPlan Pro", page_icon="🏃",
                   layout="wide", initial_sidebar_state="collapsed")

if not st.session_state.get("logged_in"):   st.switch_page("app.py")
if "user_data" not in st.session_state:     st.switch_page("pages/1_Profile.py")

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
    radial-gradient(ellipse at 8%   8%,  rgba(239,68,68,0.30)  0%,transparent 38%),
    radial-gradient(ellipse at 92%  10%, rgba(249,115,22,0.25) 0%,transparent 35%),
    radial-gradient(ellipse at 85%  78%, rgba(251,191,36,0.18) 0%,transparent 38%),
    radial-gradient(ellipse at 12%  82%, rgba(239,68,68,0.15)  0%,transparent 35%),
    radial-gradient(ellipse at 50%  40%, rgba(30,5,5,0.50)     0%,transparent 55%),
    linear-gradient(160deg,#0f0202 0%,#1a0303 25%,#120202 55%,#0d0202 100%)
    !important;
  color:#fff!important;font-family:'DM Sans',sans-serif!important;}

/* Speed lines texture */
[data-testid="stAppViewContainer"]>section{
  background-image:repeating-linear-gradient(
    105deg,
    transparent,transparent 120px,
    rgba(239,68,68,0.015) 120px,rgba(239,68,68,0.015) 121px
  );}

#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stDecoration"],
[data-testid="stSidebarNav"],section[data-testid="stSidebar"]{display:none!important;}

[data-testid="stAppViewContainer"]>section>div.block-container{
  max-width:1060px!important;margin:0 auto!important;padding:0 22px 100px!important;
  position:relative;z-index:2;}

/* NAV */
.nav-wrap{background:rgba(12,2,2,0.96);backdrop-filter:blur(40px);
  border-bottom:1px solid rgba(239,68,68,0.18);padding:5px 0;margin-bottom:6px;
  box-shadow:0 4px 30px rgba(0,0,0,0.70);}
.nav-logo{font-family:'Bebas Neue',sans-serif;font-size:1.4rem;letter-spacing:5px;
  color:#ef4444;text-shadow:0 0 20px rgba(239,68,68,0.55);line-height:1;}

div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"]>button{
  background:rgba(20,4,4,0.85)!important;border:1px solid rgba(239,68,68,0.25)!important;
  color:rgba(255,255,255,0.72)!important;border-radius:8px!important;
  font-size:0.78rem!important;font-weight:600!important;height:30px!important;
  min-height:30px!important;white-space:nowrap!important;transition:all 0.15s!important;
  box-shadow:none!important;}
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"]>button:hover{
  background:rgba(239,68,68,0.20)!important;border-color:rgba(239,68,68,0.65)!important;
  color:#fff!important;box-shadow:0 0 12px rgba(239,68,68,0.30)!important;}
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"]:last-child>button{
  background:rgba(239,68,68,0.22)!important;border-color:rgba(239,68,68,0.50)!important;}

/* ACTION BUTTONS */
.stButton>button{
  background:linear-gradient(135deg,#dc2626 0%,#b91c1c 50%,#991b1b 100%)!important;
  border:none!important;color:#fff!important;border-radius:14px!important;
  font-weight:700!important;font-size:0.95rem!important;letter-spacing:0.5px!important;
  box-shadow:0 6px 24px rgba(220,38,38,0.50),0 0 0 1px rgba(239,68,68,0.20)!important;
  transition:all 0.22s cubic-bezier(0.34,1.56,0.64,1)!important;}
.stButton>button:hover{transform:translateY(-3px) scale(1.02)!important;
  box-shadow:0 10px 32px rgba(220,38,38,0.70)!important;}

/* INPUTS */
[data-testid="stWidgetLabel"],[data-testid="stWidgetLabel"] p{
  color:rgba(252,165,165,0.90)!important;font-size:0.78rem!important;
  font-weight:700!important;letter-spacing:2px!important;text-transform:uppercase!important;}
input,.stTextArea textarea,.stNumberInput input{
  background:rgba(25,5,5,0.80)!important;
  border:1.5px solid rgba(239,68,68,0.25)!important;color:#fff!important;
  border-radius:12px!important;backdrop-filter:blur(10px)!important;}
input:focus{border-color:rgba(239,68,68,0.65)!important;
  box-shadow:0 0 0 3px rgba(239,68,68,0.15)!important;}
.stSelectbox [data-baseweb="select"]>div{
  background:rgba(25,5,5,0.80)!important;
  border:1.5px solid rgba(239,68,68,0.25)!important;color:#fff!important;
  border-radius:12px!important;}
.stMarkdown p{color:rgba(255,220,210,0.80)!important;line-height:1.7!important;}
.stNumberInput [data-testid="stNumberInputStepUp"],
.stNumberInput [data-testid="stNumberInputStepDown"]{
  background:rgba(239,68,68,0.20)!important;border:none!important;
  color:#fff!important;border-radius:6px!important;}

/* GLASS CARDS */
.glass-card-red{
  background:rgba(25,5,5,0.70);
  border:1px solid rgba(239,68,68,0.20);
  border-radius:22px;
  backdrop-filter:blur(30px);-webkit-backdrop-filter:blur(30px);
  box-shadow:0 12px 40px rgba(0,0,0,0.55),inset 0 1px 0 rgba(255,100,100,0.06);
  position:relative;overflow:hidden;}
.glass-card-red::before{content:'';position:absolute;top:0;left:0;right:0;height:1.5px;
  background:linear-gradient(90deg,transparent,#ef4444 35%,#f97316 65%,transparent);}

@keyframes pulse-run{0%,100%{transform:scale(1)}50%{transform:scale(1.05)}}
@keyframes fadeUp{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
@keyframes shimmer{0%{background-position:200% center}100%{background-position:-200% center}}
</style>
""", unsafe_allow_html=True)

try:
    from nav_component import render_nav
    render_nav("cardio", uname)
except Exception as _nav_err:
    st.warning(f"Nav error: {_nav_err}")

# ── CONSTANTS ─────────────────────────────────────────────────────────────────
ACTIVITIES = {
    "🏃 Running":    {"icon":"🏃","cal_per_km": 65, "color":"#E50914"},
    "🚶 Walking":    {"icon":"🚶","cal_per_km": 45, "color":"#f59e0b"},
    "🚴 Cycling":    {"icon":"🚴","cal_per_km": 35, "color":"#3b82f6"},
    "🏊 Swimming":   {"icon":"🏊","cal_per_km": 80, "color":"#06b6d4"},
    "⛹️ HIIT":       {"icon":"⛹️","cal_per_km": 90, "color":"#a855f7"},
    "🧘 Yoga":       {"icon":"🧘","cal_per_km": 20, "color":"#22c55e"},
    "🥊 Boxing":     {"icon":"🥊","cal_per_km": 70, "color":"#f97316"},
    "🏋️ CrossFit":   {"icon":"🏋️","cal_per_km": 85, "color":"#ec4899"},
    "⛷️ Jump Rope":  {"icon":"⛷️","cal_per_km": 75, "color":"#34d399"},
    "🤸 Other":      {"icon":"🤸","cal_per_km": 50, "color":"#94a3b8"},
}

today     = date.today()
today_str = today.isoformat()

# ── LOAD DATA ─────────────────────────────────────────────────────────────────
if "cardio_log" not in st.session_state:
    try:
        from utils.db import get_cardio
        st.session_state.cardio_log = get_cardio(uname, limit=50)
    except Exception:
        st.session_state.cardio_log = []

cardio_log = st.session_state.cardio_log

# ── STATS ─────────────────────────────────────────────────────────────────────
week_ago  = (today - timedelta(days=7)).isoformat()
week_log  = [c for c in cardio_log if c.get("date","") >= week_ago]
total_km  = round(sum(c.get("distance_km",0) for c in week_log), 1)
total_min = sum(c.get("duration_min",0) for c in week_log)
total_cal = sum(c.get("calories",0) for c in week_log)
sessions  = len(week_log)
all_km    = round(sum(c.get("distance_km",0) for c in cardio_log), 1)

# ── HERO ──────────────────────────────────────────────────────────────────────
# Performance insight
perf_tip = ("🔥 Beast mode! You're crushing your cardio this week." if total_km > 20
            else "💪 Solid week — keep pushing for more distance!" if total_km > 10
            else "🏃 Good start — aim for 3+ sessions this week." if sessions > 0
            else "👟 No sessions yet this week. Lace up and go!")

st.markdown(f"""
<div style='background:linear-gradient(135deg,rgba(220,38,38,0.18),rgba(153,27,27,0.10) 50%,rgba(12,2,2,0.75));
  border:1px solid rgba(239,68,68,0.30);border-radius:24px;padding:32px 36px;margin:10px 0 24px;
  position:relative;overflow:hidden;backdrop-filter:blur(30px);
  box-shadow:0 20px 60px rgba(0,0,0,0.65),inset 0 1px 0 rgba(255,150,150,0.07);'>
  <!-- Top accent line -->
  <div style='position:absolute;top:0;left:0;right:0;height:2px;
    background:linear-gradient(90deg,transparent,#ef4444 25%,#f97316 55%,#fbbf24,transparent)'></div>
  <!-- BG runner icon -->
  <div style='position:absolute;right:28px;top:20px;font-size:5rem;opacity:0.08;
    animation:pulse-run 2s ease-in-out infinite;user-select:none;line-height:1'>🏃</div>

  <div style='font-size:0.68rem;font-weight:800;letter-spacing:3.5px;text-transform:uppercase;
    color:rgba(252,165,165,0.75);margin-bottom:10px;'>🏃 Cardio Tracker</div>
  <div style='font-family:Barlow Condensed,sans-serif;font-size:clamp(2rem,5vw,3.2rem);
    font-weight:900;text-transform:uppercase;line-height:1;margin-bottom:22px;'>
    <span style='background:linear-gradient(90deg,#fca5a5,#ef4444);
      -webkit-background-clip:text;-webkit-text-fill-color:transparent;
      background-clip:text;'>{_display}'s</span>
    <span style='color:#fff;'> Cardio Log</span>
  </div>

  <!-- 5 stats in a grid -->
  <div style='display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin-bottom:16px;'>
    <div style='background:rgba(239,68,68,0.12);border:1px solid rgba(239,68,68,0.22);
      border-radius:16px;padding:14px 10px;text-align:center;'>
      <div style='font-size:0.55rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;
        color:rgba(252,165,165,0.55);margin-bottom:5px;'>KM · Week</div>
      <div style='font-family:Bebas Neue,sans-serif;font-size:2.2rem;color:#ef4444;line-height:1;
        text-shadow:0 0 20px rgba(239,68,68,0.45);'>{total_km}</div>
    </div>
    <div style='background:rgba(249,115,22,0.10);border:1px solid rgba(249,115,22,0.20);
      border-radius:16px;padding:14px 10px;text-align:center;'>
      <div style='font-size:0.55rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;
        color:rgba(253,186,116,0.55);margin-bottom:5px;'>Minutes</div>
      <div style='font-family:Bebas Neue,sans-serif;font-size:2.2rem;color:#f97316;line-height:1;
        text-shadow:0 0 20px rgba(249,115,22,0.40);'>{total_min}</div>
    </div>
    <div style='background:rgba(251,191,36,0.10);border:1px solid rgba(251,191,36,0.20);
      border-radius:16px;padding:14px 10px;text-align:center;'>
      <div style='font-size:0.55rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;
        color:rgba(252,211,77,0.55);margin-bottom:5px;'>Calories</div>
      <div style='font-family:Bebas Neue,sans-serif;font-size:2.2rem;color:#fbbf24;line-height:1;
        text-shadow:0 0 20px rgba(251,191,36,0.40);'>{total_cal}</div>
    </div>
    <div style='background:rgba(34,197,94,0.10);border:1px solid rgba(34,197,94,0.20);
      border-radius:16px;padding:14px 10px;text-align:center;'>
      <div style='font-size:0.55rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;
        color:rgba(134,239,172,0.55);margin-bottom:5px;'>Sessions</div>
      <div style='font-family:Bebas Neue,sans-serif;font-size:2.2rem;color:#34d399;line-height:1;
        text-shadow:0 0 20px rgba(52,211,153,0.40);'>{sessions}</div>
    </div>
    <div style='background:rgba(96,165,250,0.10);border:1px solid rgba(96,165,250,0.20);
      border-radius:16px;padding:14px 10px;text-align:center;'>
      <div style='font-size:0.55rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;
        color:rgba(147,197,253,0.55);margin-bottom:5px;'>Total KM</div>
      <div style='font-family:Bebas Neue,sans-serif;font-size:2.2rem;color:#60a5fa;line-height:1;
        text-shadow:0 0 20px rgba(96,165,250,0.40);'>{all_km}</div>
    </div>
  </div>

  <!-- Perf tip -->
  <div style='background:rgba(239,68,68,0.10);border:1px solid rgba(239,68,68,0.18);
    border-radius:12px;padding:10px 16px;font-size:0.82rem;color:rgba(255,220,210,0.80);'>
    {perf_tip}
  </div>
</div>
""", unsafe_allow_html=True)

# ── LOG FORM + HISTORY ────────────────────────────────────────────────────────
col_form, col_hist = st.columns([1, 1.4], gap="large")

with col_form:
    st.markdown("""
<div style='background:rgba(22,4,4,0.75);border:1px solid rgba(239,68,68,0.22);border-radius:22px;
  padding:22px 26px;position:relative;overflow:hidden;
  backdrop-filter:blur(30px);-webkit-backdrop-filter:blur(30px);
  box-shadow:0 12px 40px rgba(0,0,0,0.55),inset 0 1px 0 rgba(255,100,100,0.06);
  margin-bottom:16px'>
  <div style='position:absolute;top:0;left:0;right:0;height:1.5px;
    background:linear-gradient(90deg,transparent,#ef4444 35%,#f97316 65%,transparent)'></div>
  <div style='font-size:0.65rem;font-weight:800;letter-spacing:2.5px;text-transform:uppercase;
    color:rgba(252,165,165,0.80);margin-bottom:16px;'>➕ Log New Session</div>
""", unsafe_allow_html=True)

    _act_label = st.selectbox("Activity", list(ACTIVITIES.keys()), key="ca_act")
    _act       = ACTIVITIES[_act_label]

    _ca_date = st.date_input("Date", value=today, max_value=today,
                              min_value=today - timedelta(days=60), key="ca_date")

    _c1, _c2 = st.columns(2)
    with _c1:
        _dist = st.number_input("Distance (km)", min_value=0.0, max_value=500.0,
                                 value=5.0, step=0.1, key="ca_dist")
    with _c2:
        _dur  = st.number_input("Duration (min)", min_value=1, max_value=600,
                                 value=30, step=1, key="ca_dur")

    # Auto-calculate calories
    _weight = data.get("weight", 70)
    _cal_auto = int(_dist * _act["cal_per_km"] * (_weight / 70))
    _cal  = st.number_input("Calories burned", min_value=0, max_value=5000,
                             value=_cal_auto, step=10, key="ca_cal",
                             help="Auto-calculated from distance & weight. Edit if needed.")

    # Pace calculation
    if _dist > 0 and _dur > 0:
        pace_min = int(_dur / _dist)
        pace_sec = int((_dur / _dist - pace_min) * 60)
        pace_str = f"{pace_min}:{pace_sec:02d} min/km"
        speed    = round(_dist / (_dur / 60), 1)
        st.markdown(f"""
<div style='background:rgba(229,9,20,0.08);border:1px solid rgba(229,9,20,0.20);
  border-radius:10px;padding:10px 14px;display:flex;gap:20px;margin-top:4px'>
  <div style='text-align:center'>
    <div style='font-size:1.1rem;font-weight:700;color:#E50914'>{pace_str}</div>
    <div style='font-size:0.62rem;text-transform:uppercase;letter-spacing:1px;color:rgba(255,255,255,0.40)'>Pace</div>
  </div>
  <div style='text-align:center'>
    <div style='font-size:1.1rem;font-weight:700;color:#fcd34d'>{speed} km/h</div>
    <div style='font-size:0.62rem;text-transform:uppercase;letter-spacing:1px;color:rgba(255,255,255,0.40)'>Speed</div>
  </div>
  <div style='text-align:center'>
    <div style='font-size:1.1rem;font-weight:700;color:#86efac'>{_cal_auto} kcal</div>
    <div style='font-size:0.62rem;text-transform:uppercase;letter-spacing:1px;color:rgba(255,255,255,0.40)'>Est. burn</div>
  </div>
</div>""", unsafe_allow_html=True)

    _notes_c = st.text_input("Notes (optional)", placeholder="e.g. morning run, felt great...",
                              key="ca_notes")
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    if st.button("🏃 Save Cardio Session", key="ca_save", use_container_width=True):
        try:
            from utils.db import save_cardio, get_cardio
            save_cardio(uname, _ca_date.isoformat(), _act_label,
                        _dist, _dur, _cal, _notes_c)
            st.session_state.cardio_log = get_cardio(uname, limit=50)
            st.toast(f"✅ {_act_label} logged!", icon="🏃")
            st.rerun()
        except Exception as e:
            st.error(f"Save failed: {e}")

# ── WEEKLY BAR CHART ──────────────────────────────────────────────────────────
with col_hist:
    st.markdown("""
<div style='background:rgba(22,4,4,0.75);border:1px solid rgba(239,68,68,0.18);border-radius:22px;
  padding:22px 26px;backdrop-filter:blur(30px);-webkit-backdrop-filter:blur(30px);
  box-shadow:0 12px 40px rgba(0,0,0,0.55),inset 0 1px 0 rgba(255,100,100,0.06);
  position:relative;overflow:hidden;margin-bottom:16px'>
  <div style='position:absolute;top:0;left:0;right:0;height:1.5px;
    background:linear-gradient(90deg,transparent,#f97316,transparent)'></div>
  <div style='font-size:0.65rem;font-weight:800;letter-spacing:2.5px;text-transform:uppercase;
    color:rgba(253,186,116,0.80);margin-bottom:18px;'>📊 Weekly Distance (km)</div>
""", unsafe_allow_html=True)

    # Build 7-day distance data
    days7 = []
    for i in range(6, -1, -1):
        d = (today - timedelta(days=i)).isoformat()
        day_entries = [c for c in cardio_log if c.get("date") == d]
        km = round(sum(c.get("distance_km",0) for c in day_entries), 1)
        days7.append({"date": d, "km": km, "sessions": len(day_entries),
                      "cal": sum(c.get("calories",0) for c in day_entries)})

    max_km = max((d["km"] for d in days7), default=5)
    max_km = max(max_km, 5)

    bars = "<div style='display:flex;align-items:flex-end;gap:8px;height:150px;margin-bottom:10px'>"
    for d in days7:
        km     = d["km"]
        pct    = int(km / max_km * 100) if km > 0 else 0
        day    = date.fromisoformat(d["date"]).strftime("%a")
        istoday= d["date"] == today_str
        col    = ("#E50914" if km > 0 else "rgba(255,255,255,0.06)")
        border = "border:2px solid #fff;" if istoday else ""
        bars  += f"""
<div style='flex:1;display:flex;flex-direction:column;align-items:center;gap:4px'>
  <div style='font-size:0.65rem;color:rgba(255,255,255,0.50);font-weight:600'>
    {f"{km}km" if km > 0 else "–"}</div>
  <div style='width:100%;background:rgba(255,255,255,0.05);border-radius:6px 6px 0 0;
    display:flex;align-items:flex-end;flex:1'>
    <div style='width:100%;height:{max(pct,3)}%;background:{col};border-radius:6px 6px 0 0;
      {border}'></div>
  </div>
  <div style='font-size:0.68rem;font-weight:{"800" if istoday else "500"};
    color:{"#E50914" if istoday else "rgba(255,255,255,0.40)"}'>{day}</div>
</div>"""
    bars += "</div>"
    st.markdown(bars + "</div>", unsafe_allow_html=True)

    # Activity breakdown donut (text version)
    if cardio_log:
        act_counts = {}
        for c in week_log:
            a = c.get("activity","Other")
            act_counts[a] = act_counts.get(a,0) + 1
        if act_counts:
            st.markdown("""
<div style='background:rgba(20,4,4,0.85);border:1px solid rgba(229,9,20,0.18);border-radius:14px;
  padding:14px 18px;backdrop-filter:blur(12px)'>
  <div style='font-size:0.65rem;font-weight:800;letter-spacing:2px;text-transform:uppercase;
    color:rgba(229,9,20,0.60);margin-bottom:10px'>This week's activities</div>""",
                unsafe_allow_html=True)
            for act, count in sorted(act_counts.items(), key=lambda x:-x[1]):
                info = ACTIVITIES.get(act, {"color":"#94a3b8","icon":"🤸"})
                w_km = round(sum(c.get("distance_km",0) for c in week_log if c.get("activity")==act),1)
                st.markdown(f"""
<div style='display:flex;align-items:center;gap:10px;margin-bottom:6px'>
  <div style='font-size:1rem;width:24px'>{info["icon"]}</div>
  <div style='flex:1'>
    <div style='display:flex;justify-content:space-between;margin-bottom:3px'>
      <span style='font-size:0.78rem;color:rgba(255,255,255,0.75)'>{act.split(" ",1)[-1]}</span>
      <span style='font-size:0.72rem;color:rgba(255,255,255,0.40)'>{count}x · {w_km}km</span>
    </div>
    <div style='background:rgba(255,255,255,0.06);border-radius:4px;height:5px;overflow:hidden'>
      <div style='width:{int(count/max(act_counts.values())*100)}%;height:100%;
        background:{info["color"]};border-radius:4px'></div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

# ── HISTORY LOG ───────────────────────────────────────────────────────────────
if cardio_log:
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    st.markdown("""<div style='font-size:0.68rem;font-weight:800;letter-spacing:3px;text-transform:uppercase;
color:rgba(229,9,20,0.55);margin-bottom:10px;display:flex;align-items:center;gap:10px'>
<span>🕐 Recent Sessions</span>
<span style='flex:1;height:1px;background:linear-gradient(90deg,rgba(229,9,20,0.28),transparent);display:block'></span>
</div>""", unsafe_allow_html=True)

    for c in cardio_log[:15]:
        d         = c.get("date","")
        act       = c.get("activity","")
        dist      = c.get("distance_km",0)
        dur       = c.get("duration_min",0)
        cal       = c.get("calories",0)
        notes     = c.get("notes","") or ""
        row_id    = c.get("id","")
        info      = ACTIVITIES.get(act, {"color":"#94a3b8","icon":"🤸"})
        pace_str  = ""
        if dist > 0 and dur > 0:
            pm = int(dur/dist); ps = int((dur/dist - pm)*60)
            pace_str = f"{pm}:{ps:02d}/km"
        try:
            dobj  = date.fromisoformat(d)
            ddisp = dobj.strftime("%d %b %Y")
            if dobj == today: ddisp = "Today"
            elif dobj == today - timedelta(days=1): ddisp = "Yesterday"
        except: ddisp = d

        del_col, card_col = st.columns([0.06, 1])
        with card_col:
            st.markdown(f"""
<div style='display:flex;align-items:center;gap:14px;background:rgba(20,4,4,0.85);
  border:1px solid rgba(229,9,20,0.15);border-left:3px solid {info["color"]};
  border-radius:12px;padding:12px 18px;backdrop-filter:blur(12px)'>
  <div style='font-size:1.6rem;flex-shrink:0'>{info["icon"]}</div>
  <div style='min-width:90px'>
    <div style='font-size:0.85rem;font-weight:600;color:#fff'>{act.split(" ",1)[-1]}</div>
    <div style='font-size:0.68rem;color:rgba(255,255,255,0.40)'>{ddisp}</div>
  </div>
  <div style='display:flex;gap:16px;flex:1;flex-wrap:wrap'>
    <div style='text-align:center'>
      <div style='font-size:1rem;font-weight:700;color:{info["color"]}'>{dist}km</div>
      <div style='font-size:0.60rem;text-transform:uppercase;letter-spacing:1px;color:rgba(255,255,255,0.35)'>dist</div>
    </div>
    <div style='text-align:center'>
      <div style='font-size:1rem;font-weight:700;color:#fcd34d'>{dur}m</div>
      <div style='font-size:0.60rem;text-transform:uppercase;letter-spacing:1px;color:rgba(255,255,255,0.35)'>time</div>
    </div>
    <div style='text-align:center'>
      <div style='font-size:1rem;font-weight:700;color:#fdba74'>{cal}</div>
      <div style='font-size:0.60rem;text-transform:uppercase;letter-spacing:1px;color:rgba(255,255,255,0.35)'>kcal</div>
    </div>
    {f'<div style="text-align:center"><div style="font-size:1rem;font-weight:700;color:#93c5fd">{pace_str}</div><div style="font-size:0.60rem;text-transform:uppercase;letter-spacing:1px;color:rgba(255,255,255,0.35)">pace</div></div>' if pace_str else ""}
  </div>
  {f'<div style="font-size:0.75rem;color:rgba(255,255,255,0.38);font-style:italic;max-width:140px">{notes}</div>' if notes else ""}
</div>""", unsafe_allow_html=True)
        with del_col:
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            if st.button("🗑", key=f"del_ca_{row_id}", help="Delete this entry"):
                try:
                    from utils.db import delete_cardio, get_cardio
                    delete_cardio(uname, row_id)
                    st.session_state.cardio_log = get_cardio(uname, limit=50)
                    st.toast("Deleted", icon="🗑")
                    st.rerun()
                except Exception as e:
                    st.error(str(e))