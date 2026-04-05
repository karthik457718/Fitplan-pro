# -*- coding: utf-8 -*-
import streamlit as st
import os, sys, json
from datetime import date, timedelta
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth_token import logout

st.set_page_config(page_title="Progress Charts | FitPlan Pro", page_icon="📈",
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
    radial-gradient(ellipse at 10% 10%, rgba(16,185,129,0.28)  0%,transparent 40%),
    radial-gradient(ellipse at 88% 12%, rgba(59,130,246,0.22)  0%,transparent 38%),
    radial-gradient(ellipse at 80% 80%, rgba(99,60,220,0.18)   0%,transparent 38%),
    radial-gradient(ellipse at 12% 80%, rgba(16,185,129,0.15)  0%,transparent 35%),
    linear-gradient(160deg,#020e08 0%,#031810 28%,#030e0a 58%,#020c07 100%)
    !important;
  color:#fff!important;font-family:'DM Sans',sans-serif!important;}

#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stDecoration"],
[data-testid="stSidebarNav"],section[data-testid="stSidebar"]{display:none!important;}
[data-testid="stAppViewContainer"]>section>div.block-container{
  max-width:1060px!important;margin:0 auto!important;padding:0 22px 100px!important;position:relative;z-index:2;}

.nav-wrap{background:rgba(2,12,6,0.97);backdrop-filter:blur(40px);
  border-bottom:1px solid rgba(16,185,129,0.20);padding:5px 0;margin-bottom:6px;
  box-shadow:0 4px 30px rgba(0,0,0,0.70);}
.nav-logo{font-family:'Bebas Neue',sans-serif;font-size:1.4rem;letter-spacing:5px;
  color:#10b981;text-shadow:0 0 20px rgba(16,185,129,0.55);line-height:1;}

div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"]>button{
  background:rgba(2,16,8,0.85)!important;border:1px solid rgba(16,185,129,0.22)!important;
  color:rgba(255,255,255,0.72)!important;border-radius:8px!important;
  font-size:0.78rem!important;font-weight:600!important;height:30px!important;
  min-height:30px!important;white-space:nowrap!important;transition:all 0.15s!important;box-shadow:none!important;}
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"]>button:hover{
  background:rgba(16,185,129,0.20)!important;border-color:rgba(16,185,129,0.60)!important;color:#fff!important;}
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"]:last-child>button{
  background:rgba(239,68,68,0.20)!important;border-color:rgba(239,68,68,0.45)!important;}

.stButton>button{
  background:linear-gradient(135deg,#059669,#0284c7)!important;
  border:none!important;color:#fff!important;border-radius:14px!important;
  font-weight:700!important;font-size:0.95rem!important;
  box-shadow:0 6px 24px rgba(5,150,105,0.45)!important;transition:all 0.22s!important;}
.stButton>button:hover{transform:translateY(-3px) scale(1.02)!important;
  box-shadow:0 10px 32px rgba(5,150,105,0.65)!important;}

[data-testid="stWidgetLabel"],[data-testid="stWidgetLabel"] p{
  color:rgba(110,231,183,0.90)!important;font-size:0.78rem!important;
  font-weight:700!important;letter-spacing:2px!important;text-transform:uppercase!important;}
input,.stNumberInput input{background:rgba(2,20,10,0.80)!important;
  border:1.5px solid rgba(16,185,129,0.25)!important;color:#fff!important;border-radius:12px!important;}
.stMarkdown p{color:rgba(167,243,208,0.80)!important;line-height:1.7!important;}
.stTabs [data-baseweb="tab-list"]{background:rgba(2,16,8,0.85)!important;
  border-radius:12px!important;padding:4px!important;border:1px solid rgba(16,185,129,0.15)!important;}
.stTabs [data-baseweb="tab"]{background:transparent!important;color:rgba(255,255,255,0.65)!important;
  border-radius:8px!important;font-weight:600!important;font-size:0.88rem!important;}
.stTabs [aria-selected="true"]{background:linear-gradient(135deg,#059669,#0284c7)!important;
  color:#fff!important;box-shadow:0 3px 12px rgba(5,150,105,0.40)!important;}

@keyframes fadeUp{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:translateY(0)}}
</style>
""", unsafe_allow_html=True)

# ── NAV ───────────────────────────────────────────────────────────────────────
st.markdown("<div class='nav-wrap'>", unsafe_allow_html=True)
_n = st.columns([1.6,1,1,1,1,1,1,1,1,1,1,1.2])
with _n[0]: st.markdown("<div class='nav-logo'>⚡ FITPLAN PRO</div>", unsafe_allow_html=True)
with _n[1]:
    if st.button("🏠 Home", key="ch_db", use_container_width=True):
        try: st.switch_page("pages/2_Dashboard.py")
        except Exception: pass
with _n[2]:
    if st.button("⚡ Workout", key="ch_wp", use_container_width=True):
        try: st.switch_page("pages/3_Workout_Plan.py")
        except Exception: pass
with _n[3]:
    if st.button("🥗 Diet", key="ch_dp", use_container_width=True):
        try: st.switch_page("pages/4_Diet_Plan.py")
        except Exception: pass
with _n[4]:
    if st.button("🍽️ Meals", key="ch_mp", use_container_width=True):
        try: st.switch_page("pages/11_meal_planner.py")
        except Exception: pass
with _n[5]:
    if st.button("😴 Sleep", key="ch_sl", use_container_width=True):
        try: st.switch_page("pages/12_sleep_tracker.py")
        except Exception: pass
with _n[6]:
    if st.button("🏃 Cardio", key="ch_ca", use_container_width=True):
        try: st.switch_page("pages/13_cardio_tracker.py")
        except Exception: pass
with _n[7]:
    if st.button("🔥 Streak", key="ch_st", use_container_width=True):
        try: st.switch_page("pages/14_streaks.py")
        except Exception: pass
with _n[8]:
    if st.button("● 📈 Charts", key="ch_ch", use_container_width=True):
        try: st.switch_page("pages/15_progress_charts.py")
        except Exception: pass
with _n[9]:
    if st.button("🤖 Coach", key="ch_ai", use_container_width=True):
        try: st.switch_page("pages/5_ai_coach.py")
        except Exception: pass
with _n[10]:
    if st.button("🏆 Records", key="ch_rc", use_container_width=True):
        try: st.switch_page("pages/6_records.py")
        except Exception: pass
with _n[11]:
    if st.button("🚪 Sign Out", key="ch_so", use_container_width=True):
        logout(uname)
        for _k in ["logged_in","username","auth_token","user_data","workout_plan","structured_days",
                   "dietary_type","full_plan_data","plan_id","plan_start","plan_duration",
                   "force_regen","tracking","_plan_checked","_db_loaded_dash"]:
            st.session_state.pop(_k, None)
        st.switch_page("app.py")
st.markdown("</div>", unsafe_allow_html=True)

# ── LOAD DATA ─────────────────────────────────────────────────────────────────
today = date.today()

@st.cache_data(ttl=300)
def load_weight(uname):
    try:
        from utils.db import get_weight_log
        return get_weight_log(uname, limit=60)
    except Exception: return []

@st.cache_data(ttl=300)
def load_measurements(uname):
    try:
        from utils.db import get_measurements
        return get_measurements(uname, limit=20)
    except Exception: return []

@st.cache_data(ttl=300)
def load_sleep(uname):
    try:
        from utils.db import get_sleep
        return get_sleep(uname, limit=30)
    except Exception: return []

@st.cache_data(ttl=300)
def load_cardio(uname):
    try:
        from utils.db import get_cardio
        return get_cardio(uname, limit=50)
    except Exception: return []

weight_log   = load_weight(uname)
measurements = load_measurements(uname)
sleep_log    = load_sleep(uname)
cardio_log   = load_cardio(uname)

# ── HERO ──────────────────────────────────────────────────────────────────────
curr_w   = weight_log[-1]["weight_kg"] if weight_log else data.get("weight", 70)
start_w  = weight_log[0]["weight_kg"]  if weight_log else curr_w
w_change = round(curr_w - start_w, 1)
w_arrow  = "↓" if w_change < 0 else "↑" if w_change > 0 else "→"
w_col    = ("#22c55e" if (w_change < 0 and "Loss" in data.get("goal",""))
            or (w_change > 0 and "Muscle" in data.get("goal",""))
            else "#ef4444" if w_change != 0 else "#94a3b8")

avg_sleep  = round(sum(s["hours"] for s in sleep_log[:7]) / max(len(sleep_log[:7]),1), 1) if sleep_log else 0
total_km   = round(sum(c.get("distance_km",0) for c in cardio_log), 1)

st.markdown(f"""
<div style='background:linear-gradient(135deg,rgba(5,150,105,0.18),rgba(2,132,199,0.10) 50%,rgba(2,12,6,0.75));
  border:1px solid rgba(16,185,129,0.28);border-radius:24px;padding:28px 36px;margin:10px 0 22px;
  position:relative;overflow:hidden;backdrop-filter:blur(30px);
  box-shadow:0 20px 60px rgba(0,0,0,0.60),inset 0 1px 0 rgba(100,255,180,0.06);'>
  <div style='position:absolute;top:0;left:0;right:0;height:2px;
    background:linear-gradient(90deg,transparent,#10b981 30%,#3b82f6 65%,transparent)'></div>
  <div style='font-size:0.68rem;font-weight:800;letter-spacing:3.5px;text-transform:uppercase;
    color:rgba(52,211,153,0.75);margin-bottom:10px;'>📈 Progress Charts</div>
  <div style='font-family:Barlow Condensed,sans-serif;font-size:clamp(2rem,5vw,3rem);
    font-weight:900;text-transform:uppercase;line-height:1;margin-bottom:20px;'>
    <span style='background:linear-gradient(90deg,#6ee7b7,#10b981);
      -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;'>{_display}'s</span>
    <span style='color:#fff;'> Progress</span>
  </div>
  <div style='display:grid;grid-template-columns:repeat(4,1fr);gap:10px;'>
    <div style='background:rgba(255,255,255,0.05);border:1px solid rgba(16,185,129,0.18);border-radius:16px;padding:14px;text-align:center;'>
      <div style='font-size:0.55rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:rgba(110,231,183,0.50);margin-bottom:5px;'>Current Weight</div>
      <div style='font-family:Bebas Neue,sans-serif;font-size:2.2rem;color:#10b981;line-height:1;text-shadow:0 0 20px rgba(16,185,129,0.40);'>{curr_w}kg</div>
    </div>
    <div style='background:rgba(255,255,255,0.05);border:1px solid rgba(16,185,129,0.18);border-radius:16px;padding:14px;text-align:center;'>
      <div style='font-size:0.55rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:rgba(110,231,183,0.50);margin-bottom:5px;'>Change</div>
      <div style='font-family:Bebas Neue,sans-serif;font-size:2.2rem;color:{w_col};line-height:1;text-shadow:0 0 20px {w_col}60;'>{w_arrow}{abs(w_change)}kg</div>
    </div>
    <div style='background:rgba(255,255,255,0.05);border:1px solid rgba(16,185,129,0.18);border-radius:16px;padding:14px;text-align:center;'>
      <div style='font-size:0.55rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:rgba(110,231,183,0.50);margin-bottom:5px;'>Avg Sleep</div>
      <div style='font-family:Bebas Neue,sans-serif;font-size:2.2rem;color:#a78bfa;line-height:1;text-shadow:0 0 20px rgba(167,139,250,0.40);'>{avg_sleep}h</div>
    </div>
    <div style='background:rgba(255,255,255,0.05);border:1px solid rgba(16,185,129,0.18);border-radius:16px;padding:14px;text-align:center;'>
      <div style='font-size:0.55rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:rgba(110,231,183,0.50);margin-bottom:5px;'>Total Cardio</div>
      <div style='font-family:Bebas Neue,sans-serif;font-size:2.2rem;color:#60a5fa;line-height:1;text-shadow:0 0 20px rgba(96,165,250,0.40);'>{total_km}km</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["⚖️ Weight", "😴 Sleep", "🏃 Cardio", "📏 Measurements"])

def make_chart(data_pts, label, color, unit="", height=200):
    """Build an inline SVG line chart"""
    if len(data_pts) < 2:
        return f"<div style='height:{height}px;display:flex;align-items:center;justify-content:center;color:rgba(255,255,255,0.30);font-size:0.85rem;'>Log more data to see your {label} trend</div>"
    vals = [p[1] for p in data_pts]
    mn, mx = min(vals), max(vals)
    rng  = mx - mn or 1
    w, h = 900, height
    pad  = 40
    pts  = []
    for i,(_, v) in enumerate(data_pts):
        x = pad + (i / max(len(data_pts)-1,1)) * (w - 2*pad)
        y = h - pad - ((v - mn) / rng) * (h - 2*pad)
        pts.append((x, y))

    # Polyline path
    line = " ".join(f"{x:.1f},{y:.1f}" for x,y in pts)
    # Area fill path
    area = f"M{pts[0][0]:.1f},{h-pad} " + " ".join(f"L{x:.1f},{y:.1f}" for x,y in pts) + f" L{pts[-1][0]:.1f},{h-pad} Z"

    # Axis labels
    y_labels = ""
    for frac in [0, 0.25, 0.5, 0.75, 1.0]:
        v   = mn + frac * rng
        y_p = h - pad - frac * (h - 2*pad)
        y_labels += f"<text x='{pad-6}' y='{y_p:.1f}' text-anchor='end' fill='rgba(255,255,255,0.30)' font-size='10'>{v:.1f}</text>"

    # X-axis date labels (show 5 evenly)
    x_labels = ""
    step = max(1, len(data_pts)//5)
    for i in range(0, len(data_pts), step):
        d_str = data_pts[i][0][-5:]  # MM-DD
        x_p   = pad + (i / max(len(data_pts)-1,1)) * (w - 2*pad)
        x_labels += f"<text x='{x_p:.1f}' y='{h-pad+14}' text-anchor='middle' fill='rgba(255,255,255,0.30)' font-size='10'>{d_str}</text>"

    # Dots for last point
    lx, ly = pts[-1]
    last_val = vals[-1]

    svg = f"""<svg viewBox='0 0 {w} {h}' xmlns='http://www.w3.org/2000/svg' style='width:100%;height:{height}px;'>
  <defs>
    <linearGradient id='ag{label[:3]}' x1='0' y1='0' x2='0' y2='1'>
      <stop offset='0%' stop-color='{color}' stop-opacity='0.35'/>
      <stop offset='100%' stop-color='{color}' stop-opacity='0.02'/>
    </linearGradient>
  </defs>
  <!-- Grid lines -->
  {"".join(f"<line x1='{pad}' y1='{h-pad-f*(h-2*pad):.1f}' x2='{w-pad}' y2='{h-pad-f*(h-2*pad):.1f}' stroke='rgba(255,255,255,0.06)' stroke-width='1'/>" for f in [0.25,0.5,0.75,1.0])}
  <!-- Area -->
  <path d='{area}' fill='url(#ag{label[:3]})'/>
  <!-- Line -->
  <polyline points='{line}' fill='none' stroke='{color}' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'/>
  <!-- Last point dot -->
  <circle cx='{lx:.1f}' cy='{ly:.1f}' r='5' fill='{color}' stroke='rgba(0,0,0,0.50)' stroke-width='2'/>
  <text x='{min(lx+8, w-50):.1f}' y='{ly-8:.1f}' fill='{color}' font-size='11' font-weight='bold'>{last_val:.1f}{unit}</text>
  <!-- Axis labels -->
  {y_labels}
  {x_labels}
  <!-- Axis lines -->
  <line x1='{pad}' y1='{pad}' x2='{pad}' y2='{h-pad}' stroke='rgba(255,255,255,0.10)' stroke-width='1'/>
  <line x1='{pad}' y1='{h-pad}' x2='{w-pad}' y2='{h-pad}' stroke='rgba(255,255,255,0.10)' stroke-width='1'/>
</svg>"""
    return svg

def chart_card(title, color, svg_content, stats_html=""):
    return f"""
<div style='background:rgba(4,18,8,0.75);border:1px solid rgba(16,185,129,0.18);border-radius:20px;
  padding:22px 24px;backdrop-filter:blur(24px);position:relative;overflow:hidden;margin-bottom:16px;'>
  <div style='position:absolute;top:0;left:0;right:0;height:1.5px;
    background:linear-gradient(90deg,transparent,{color},transparent);'></div>
  <div style='font-size:0.68rem;font-weight:800;letter-spacing:2.5px;text-transform:uppercase;
    color:rgba(110,231,183,0.70);margin-bottom:6px;'>{title}</div>
  {stats_html}
  {svg_content}
</div>"""

# ── TAB 1: WEIGHT ─────────────────────────────────────────────────────────────
with tab1:
    # Add weight entry
    col_form, col_chart = st.columns([1, 2.2])
    with col_form:
        st.markdown("""<div style='background:rgba(4,18,8,0.75);border:1px solid rgba(16,185,129,0.20);
border-radius:18px;padding:20px;backdrop-filter:blur(20px);position:relative;overflow:hidden;'>
<div style='position:absolute;top:0;left:0;right:0;height:1.5px;
  background:linear-gradient(90deg,transparent,#10b981,transparent);'></div>
<div style='font-size:0.65rem;font-weight:800;letter-spacing:2px;text-transform:uppercase;
  color:rgba(52,211,153,0.75);margin-bottom:14px;'>⚖️ Log Weight</div>
""", unsafe_allow_html=True)
        _wt_date = st.date_input("Date", value=today, max_value=today, key="pc_wt_date")
        _wt_val  = st.number_input("Weight (kg)", min_value=30.0, max_value=300.0,
                                    value=float(curr_w), step=0.1, key="pc_wt_val")
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.button("💾 Save Weight", key="pc_wt_save", use_container_width=True):
            try:
                from utils.db import save_weight_log
                save_weight_log(uname, _wt_date.isoformat(), _wt_val)
                load_weight.clear()
                st.toast(f"✅ {_wt_val}kg logged!", icon="⚖️")
                st.rerun()
            except Exception as e:
                st.error(str(e))

    with col_chart:
        pts = [(r["date"], r["weight_kg"]) for r in weight_log]
        pts.sort()
        # Stats
        goal_txt = data.get("goal","")
        if len(pts) >= 2:
            trend = pts[-1][1] - pts[0][1]
            t_col = "#22c55e" if ("Loss" in goal_txt and trend < 0) or ("Muscle" in goal_txt and trend > 0) else "#ef4444"
            stats = f"<div style='display:flex;gap:16px;margin-bottom:12px;font-size:0.78rem;'><span style='color:rgba(255,255,255,0.45);'>Start: <b style='color:#fff'>{pts[0][1]}kg</b></span><span style='color:rgba(255,255,255,0.45);'>Now: <b style='color:#10b981'>{pts[-1][1]}kg</b></span><span style='color:rgba(255,255,255,0.45);'>Change: <b style='color:{t_col}'>{'+' if trend>0 else ''}{trend:.1f}kg</b></span></div>"
        else:
            stats = ""
        svg = make_chart(pts, "Weight", "#10b981", "kg", 220)
        st.markdown(chart_card("⚖️ Weight Trend", "#10b981", svg, stats), unsafe_allow_html=True)

# ── TAB 2: SLEEP ──────────────────────────────────────────────────────────────
with tab2:
    sl_pts = [(s["date"], s["hours"]) for s in sleep_log]
    sl_pts.sort()
    sq_pts = [(s["date"], s["quality"]) for s in sleep_log]
    sq_pts.sort()

    c1, c2 = st.columns(2)
    with c1:
        svg = make_chart(sl_pts, "Sleep", "#a78bfa", "h", 200)
        st.markdown(chart_card("😴 Hours Slept", "#a78bfa", svg), unsafe_allow_html=True)
    with c2:
        svg = make_chart(sq_pts, "Quality", "#60a5fa", "/5", 200)
        st.markdown(chart_card("⭐ Sleep Quality", "#60a5fa", svg), unsafe_allow_html=True)

    # 7-day sleep summary
    if sleep_log:
        recent = sleep_log[:7]
        avg_h  = round(sum(s["hours"] for s in recent)/len(recent),1)
        avg_q  = round(sum(s["quality"] for s in recent)/len(recent),1)
        below7 = sum(1 for s in recent if s["hours"] < 7)
        st.markdown(f"""
<div style='background:rgba(4,18,8,0.75);border:1px solid rgba(167,139,250,0.18);border-radius:18px;
  padding:16px 22px;backdrop-filter:blur(20px);'>
  <div style='font-size:0.65rem;font-weight:800;letter-spacing:2px;text-transform:uppercase;
    color:rgba(167,139,250,0.70);margin-bottom:12px;'>📊 7-Day Sleep Summary</div>
  <div style='display:flex;gap:20px;flex-wrap:wrap;'>
    <div><div style='font-size:1.4rem;font-weight:800;color:#a78bfa;'>{avg_h}h</div><div style='font-size:0.62rem;color:rgba(255,255,255,0.40);'>avg hours</div></div>
    <div><div style='font-size:1.4rem;font-weight:800;color:#60a5fa;'>{avg_q}/5</div><div style='font-size:0.62rem;color:rgba(255,255,255,0.40);'>avg quality</div></div>
    <div><div style='font-size:1.4rem;font-weight:800;color:{"#ef4444" if below7>2 else "#22c55e"};'>{below7}/7</div><div style='font-size:0.62rem;color:rgba(255,255,255,0.40);'>nights under 7h</div></div>
    <div><div style='font-size:1.4rem;font-weight:800;color:#34d399;'>{7-below7}/7</div><div style='font-size:0.62rem;color:rgba(255,255,255,0.40);'>good nights</div></div>
  </div>
</div>""", unsafe_allow_html=True)

# ── TAB 3: CARDIO ─────────────────────────────────────────────────────────────
with tab3:
    ca_pts  = {}
    for c in cardio_log:
        d = c.get("date","")
        ca_pts[d] = ca_pts.get(d, 0) + c.get("distance_km",0)
    ca_sorted = sorted(ca_pts.items())

    cal_pts = {}
    for c in cardio_log:
        d = c.get("date","")
        cal_pts[d] = cal_pts.get(d, 0) + c.get("calories",0)
    cal_sorted = sorted(cal_pts.items())

    c1, c2 = st.columns(2)
    with c1:
        svg = make_chart(ca_sorted, "Distance", "#ef4444", "km", 200)
        st.markdown(chart_card("🏃 Distance per Day", "#ef4444", svg), unsafe_allow_html=True)
    with c2:
        svg = make_chart(cal_sorted, "Calories", "#f97316", "cal", 200)
        st.markdown(chart_card("🔥 Calories Burned", "#f97316", svg), unsafe_allow_html=True)

    # Activity breakdown
    if cardio_log:
        act_km = {}
        for c in cardio_log:
            a = c.get("activity","Other")
            act_km[a] = act_km.get(a, 0) + c.get("distance_km",0)
        total_ca = sum(act_km.values()) or 1
        breakdown = "".join(f"""
<div style='display:flex;align-items:center;gap:12px;margin-bottom:8px;'>
  <div style='width:110px;font-size:0.78rem;color:rgba(255,255,255,0.65);'>{act[:20]}</div>
  <div style='flex:1;background:rgba(255,255,255,0.05);border-radius:6px;height:8px;overflow:hidden;'>
    <div style='width:{int(km/total_ca*100)}%;height:100%;background:#ef4444;border-radius:6px;'></div>
  </div>
  <div style='font-size:0.75rem;font-weight:700;color:#ef4444;min-width:45px;text-align:right;'>{round(km,1)}km</div>
</div>""" for act,km in sorted(act_km.items(),key=lambda x:-x[1]))
        st.markdown(f"""
<div style='background:rgba(4,18,8,0.75);border:1px solid rgba(239,68,68,0.18);border-radius:18px;
  padding:18px 22px;backdrop-filter:blur(20px);'>
  <div style='font-size:0.65rem;font-weight:800;letter-spacing:2px;text-transform:uppercase;
    color:rgba(252,165,165,0.70);margin-bottom:14px;'>🏅 Activity Breakdown — All Time</div>
  {breakdown}
</div>""", unsafe_allow_html=True)

# ── TAB 4: MEASUREMENTS ───────────────────────────────────────────────────────
with tab4:
    if not measurements:
        st.markdown("""<div style='background:rgba(4,18,8,0.75);border:1px solid rgba(16,185,129,0.15);
border-radius:18px;padding:40px;text-align:center;backdrop-filter:blur(20px);'>
  <div style='font-size:2.5rem;margin-bottom:12px;'>📏</div>
  <div style='color:rgba(255,255,255,0.45);font-size:0.90rem;'>No measurements logged yet.<br>
  Go to Records → Body Measurements to add your first entry.</div>
</div>""", unsafe_allow_html=True)
    else:
        # Show latest vs first measurement
        first = measurements[-1]  # oldest
        last  = measurements[0]   # newest
        fields = [
            ("Chest",  "chest",  "#10b981"),
            ("Waist",  "waist",  "#3b82f6"),
            ("Hips",   "hips",   "#a855f7"),
            ("Arms",   "arms",   "#f59e0b"),
            ("Thighs", "thighs", "#ef4444"),
        ]
        st.markdown("""<div style='background:rgba(4,18,8,0.75);border:1px solid rgba(16,185,129,0.18);
border-radius:20px;padding:22px 24px;backdrop-filter:blur(20px);position:relative;overflow:hidden;'>
<div style='position:absolute;top:0;left:0;right:0;height:1.5px;
  background:linear-gradient(90deg,transparent,#10b981,transparent);'></div>
<div style='font-size:0.65rem;font-weight:800;letter-spacing:2px;text-transform:uppercase;
  color:rgba(52,211,153,0.70);margin-bottom:16px;'>📏 Measurement Changes</div>""", unsafe_allow_html=True)

        cols = st.columns(5)
        for i,(name, key, col) in enumerate(fields):
            fv = first.get(key, 0) or 0
            lv = last.get(key,  0) or 0
            diff = round(lv - fv, 1)
            d_col = "#22c55e" if diff < 0 else "#ef4444" if diff > 0 else "#94a3b8"
            arrow = "↓" if diff < 0 else "↑" if diff > 0 else "→"
            with cols[i]:
                st.markdown(f"""
<div style='background:rgba(255,255,255,0.04);border:1px solid {col}30;border-radius:14px;
  padding:14px;text-align:center;'>
  <div style='font-size:0.60rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;
    color:{col}99;margin-bottom:6px;'>{name}</div>
  <div style='font-size:1.6rem;font-weight:800;color:{col};'>{lv}cm</div>
  <div style='font-size:0.72rem;color:{d_col};margin-top:4px;font-weight:600;'>
    {arrow} {abs(diff)}cm</div>
  <div style='font-size:0.60rem;color:rgba(255,255,255,0.25);'>from {fv}cm</div>
</div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # History table
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        rows = "".join(f"""
<div style='display:grid;grid-template-columns:110px repeat(5,1fr);gap:8px;
  background:rgba(4,18,8,0.65);border:1px solid rgba(16,185,129,0.12);
  border-radius:10px;padding:10px 16px;margin-bottom:6px;font-size:0.80rem;'>
  <div style='color:rgba(255,255,255,0.50);'>{m.get("date","")[-8:]}</div>
  {"".join(f"<div style='color:#fff;text-align:center;'>{m.get(k,0)}cm</div>" for _,k,_ in fields)}
</div>""" for m in measurements[:10])
        header = f"""<div style='display:grid;grid-template-columns:110px repeat(5,1fr);gap:8px;
  padding:6px 16px;margin-bottom:4px;font-size:0.62rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:rgba(255,255,255,0.30);'>
  <div>Date</div>{"".join(f"<div style='text-align:center;'>{n}</div>" for n,_,_ in fields)}
</div>"""
        st.markdown(f"<div style='background:rgba(4,18,8,0.50);border:1px solid rgba(16,185,129,0.15);border-radius:16px;padding:16px;'>{header}{rows}</div>", unsafe_allow_html=True)