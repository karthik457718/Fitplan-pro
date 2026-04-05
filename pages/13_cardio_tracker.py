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
    radial-gradient(ellipse at 10% 10%, rgba(229,9,20,0.16)  0%,transparent 40%),
    radial-gradient(ellipse at 88% 12%, rgba(251,191,36,0.14) 0%,transparent 38%),
    radial-gradient(ellipse at 92% 78%, rgba(249,115,22,0.12) 0%,transparent 38%),
    radial-gradient(ellipse at 8%  80%, rgba(34,197,94,0.10)  0%,transparent 35%),
    linear-gradient(160deg,#0f0404 0%,#180604 30%,#100403 65%,#0c0302 100%)
    !important;
  color:#fff!important;font-family:'DM Sans',sans-serif!important;}

#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stDecoration"],
[data-testid="stSidebarNav"],section[data-testid="stSidebar"]{display:none!important;}

[data-testid="stAppViewContainer"]>section>div.block-container{
  max-width:1060px!important;margin:0 auto!important;padding:0 22px 100px!important;}

.nav-wrap{background:rgba(15,4,4,0.97);backdrop-filter:blur(36px);
  border-bottom:1.5px solid rgba(229,9,20,0.22);padding:5px 0;margin-bottom:4px;}
.nav-logo{font-family:'Bebas Neue',sans-serif;font-size:1.4rem;letter-spacing:5px;
  color:#E50914;text-shadow:0 0 18px rgba(229,9,20,0.45);line-height:1;}

div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"]>button{
  background:rgba(20,4,4,0.90)!important;border:1px solid rgba(229,9,20,0.28)!important;
  color:rgba(255,255,255,0.75)!important;border-radius:8px!important;
  font-size:0.80rem!important;font-weight:600!important;height:30px!important;
  min-height:30px!important;white-space:nowrap!important;transition:all 0.15s!important;
  box-shadow:none!important;}
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"]>button:hover{
  background:rgba(229,9,20,0.20)!important;border-color:rgba(229,9,20,0.70)!important;color:#fff!important;}
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"]:last-child>button{
  background:rgba(229,9,20,0.22)!important;border-color:rgba(229,9,20,0.50)!important;}

.stButton>button{
  background:linear-gradient(135deg,#E50914,#b0000a)!important;
  border:none!important;color:#fff!important;border-radius:12px!important;
  font-weight:700!important;font-size:0.92rem!important;
  box-shadow:0 4px 18px rgba(229,9,20,0.40)!important;transition:all 0.22s!important;}
.stButton>button:hover{transform:translateY(-2px) scale(1.02)!important;
  box-shadow:0 8px 26px rgba(229,9,20,0.60)!important;}

[data-testid="stWidgetLabel"],[data-testid="stWidgetLabel"] p{
  color:rgba(255,255,255,0.80)!important;font-size:0.88rem!important;
  font-weight:600!important;letter-spacing:1.5px!important;text-transform:uppercase!important;}
input,.stTextArea textarea,.stNumberInput input{background:#1a0404!important;
  border:1.5px solid rgba(229,9,20,0.28)!important;color:#fff!important;border-radius:10px!important;}
.stSelectbox [data-baseweb="select"]>div{background:#1a0404!important;
  border:1.5px solid rgba(229,9,20,0.28)!important;color:#fff!important;}
.stMarkdown p{color:rgba(255,255,255,0.80)!important;}
</style>
""", unsafe_allow_html=True)

# ── NAV ───────────────────────────────────────────────────────────────────────
st.markdown("<div class='nav-wrap'>", unsafe_allow_html=True)
_n = st.columns([1.6,1,1,1,1,1,1,1,1,1.2])
with _n[0]: st.markdown("<div class='nav-logo'>⚡ FITPLAN PRO</div>", unsafe_allow_html=True)
for idx, (lbl, pg, key) in enumerate([
    ("🏠 Home",    "pages/2_Dashboard.py",       "ca_db"),
    ("⚡ Workout", "pages/3_Workout_Plan.py",    "ca_wp"),
    ("🥗 Diet",    "pages/4_Diet_Plan.py",        "ca_dp"),
    ("🍽️ Meals",  "pages/11_meal_planner.py",   "ca_mp"),
    ("😴 Sleep",   "pages/12_sleep_tracker.py",  "ca_sl"),
    ("🏃 Cardio",  "pages/13_cardio_tracker.py", "ca_ca"),
    ("🤖 Coach",   "pages/5_ai_coach.py",         "ca_ai"),
    ("🏆 Records", "pages/6_records.py",          "ca_rc"),
]):
    with _n[idx+1]:
        if st.button(lbl, key=key, use_container_width=True):
            try: st.switch_page(pg)
            except Exception: pass
with _n[9]:
    if st.button("🚪 Sign Out", key="ca_so", use_container_width=True):
        logout(uname)
        for k in ["logged_in","username","auth_token","user_data","workout_plan","structured_days",
                  "dietary_type","full_plan_data","plan_id","force_regen","tracking","_plan_checked"]:
            st.session_state.pop(k, None)
        st.switch_page("app.py")
st.markdown("</div>", unsafe_allow_html=True)

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
st.markdown(f"""
<div style='background:linear-gradient(135deg,rgba(229,9,20,0.14),rgba(120,0,8,0.08) 50%,rgba(15,4,4,0.70));
  border:1.5px solid rgba(229,9,20,0.42);border-radius:20px;padding:26px 32px;margin:10px 0 20px;
  position:relative;overflow:hidden;backdrop-filter:blur(20px);'>
  <div style='position:absolute;top:0;left:0;right:0;height:2px;
    background:linear-gradient(90deg,transparent,#E50914 35%,rgba(251,191,36,0.60) 65%,transparent)'></div>
  <div style='position:absolute;bottom:-40px;right:-40px;width:200px;height:200px;border-radius:50%;
    background:radial-gradient(circle,rgba(229,9,20,0.14) 0%,transparent 70%);pointer-events:none'></div>
  <div style='font-size:0.72rem;font-weight:800;letter-spacing:3px;text-transform:uppercase;
    color:rgba(229,9,20,0.80);margin-bottom:8px'>🏃 Cardio Tracker</div>
  <div style='font-family:Barlow Condensed,sans-serif;font-size:clamp(1.8rem,4vw,2.8rem);
    font-weight:900;text-transform:uppercase;color:#fff;line-height:1;margin-bottom:16px'>
    <span style='color:#E50914'>{_display}'s</span> Cardio Log
  </div>
  <div style='display:flex;gap:20px;flex-wrap:wrap'>
    <div style='background:rgba(229,9,20,0.12);border:1px solid rgba(229,9,20,0.28);
      border-radius:12px;padding:12px 20px;text-align:center;min-width:90px'>
      <div style='font-family:Bebas Neue,sans-serif;font-size:2rem;color:#E50914;line-height:1'>{total_km}</div>
      <div style='font-size:0.60rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.40)'>km this week</div>
    </div>
    <div style='background:rgba(251,191,36,0.10);border:1px solid rgba(251,191,36,0.25);
      border-radius:12px;padding:12px 20px;text-align:center;min-width:90px'>
      <div style='font-family:Bebas Neue,sans-serif;font-size:2rem;color:#fcd34d;line-height:1'>{total_min}</div>
      <div style='font-size:0.60rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.40)'>min this week</div>
    </div>
    <div style='background:rgba(249,115,22,0.10);border:1px solid rgba(249,115,22,0.25);
      border-radius:12px;padding:12px 20px;text-align:center;min-width:90px'>
      <div style='font-family:Bebas Neue,sans-serif;font-size:2rem;color:#fdba74;line-height:1'>{total_cal}</div>
      <div style='font-size:0.60rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.40)'>kcal burned</div>
    </div>
    <div style='background:rgba(34,197,94,0.10);border:1px solid rgba(34,197,94,0.25);
      border-radius:12px;padding:12px 20px;text-align:center;min-width:90px'>
      <div style='font-family:Bebas Neue,sans-serif;font-size:2rem;color:#86efac;line-height:1'>{sessions}</div>
      <div style='font-size:0.60rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.40)'>sessions</div>
    </div>
    <div style='background:rgba(59,130,246,0.10);border:1px solid rgba(59,130,246,0.25);
      border-radius:12px;padding:12px 20px;text-align:center;min-width:90px'>
      <div style='font-family:Bebas Neue,sans-serif;font-size:2rem;color:#93c5fd;line-height:1'>{all_km}</div>
      <div style='font-size:0.60rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.40)'>total km</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── LOG FORM + HISTORY ────────────────────────────────────────────────────────
col_form, col_hist = st.columns([1, 1.4], gap="large")

with col_form:
    st.markdown("""
<div style='background:rgba(20,4,4,0.90);border:1.5px solid rgba(229,9,20,0.32);border-radius:18px;
  padding:20px 24px;position:relative;overflow:hidden;backdrop-filter:blur(20px);margin-bottom:16px'>
  <div style='position:absolute;top:0;left:0;right:0;height:2px;
    background:linear-gradient(90deg,transparent,#E50914,transparent)'></div>
  <div style='font-size:0.68rem;font-weight:800;letter-spacing:2.5px;text-transform:uppercase;
    color:rgba(229,9,20,0.80);margin-bottom:14px'>➕ Log New Session</div>
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
<div style='background:rgba(20,4,4,0.90);border:1.5px solid rgba(229,9,20,0.25);border-radius:18px;
  padding:20px 24px;backdrop-filter:blur(20px);position:relative;overflow:hidden;margin-bottom:16px'>
  <div style='position:absolute;top:0;left:0;right:0;height:2px;
    background:linear-gradient(90deg,transparent,#f59e0b,transparent)'></div>
  <div style='font-size:0.68rem;font-weight:800;letter-spacing:2.5px;text-transform:uppercase;
    color:rgba(251,191,36,0.80);margin-bottom:16px'>📊 Weekly Distance (km)</div>
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