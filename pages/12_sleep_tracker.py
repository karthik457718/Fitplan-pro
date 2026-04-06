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
    radial-gradient(ellipse at 20% 15%, rgba(139,92,246,0.35) 0%,transparent 40%),
    radial-gradient(ellipse at 80% 10%, rgba(99,60,220,0.25)  0%,transparent 38%),
    radial-gradient(ellipse at 60% 70%, rgba(59,130,246,0.18) 0%,transparent 42%),
    radial-gradient(ellipse at 10% 80%, rgba(167,139,250,0.15)0%,transparent 38%),
    radial-gradient(ellipse at 90% 85%, rgba(109,40,217,0.20) 0%,transparent 40%),
    linear-gradient(170deg,#03020d 0%,#06041a 30%,#080520 60%,#04020f 100%)
    !important;
  color:#fff!important;font-family:'DM Sans',sans-serif!important;}

/* Stars texture via repeating dots */
[data-testid="stAppViewContainer"]>section{
  background-image:
    radial-gradient(circle at 1px 1px,rgba(255,255,255,0.06) 1px,transparent 0),
    radial-gradient(circle at 1px 1px,rgba(167,139,250,0.04) 1px,transparent 0);
  background-size:40px 40px, 80px 80px;}

#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stDecoration"],
[data-testid="stSidebarNav"],section[data-testid="stSidebar"]{display:none!important;}

[data-testid="stAppViewContainer"]>section>div.block-container{
  max-width:1060px!important;margin:0 auto!important;padding:0 22px 100px!important;
  position:relative;z-index:2;}

/* NAV */
.nav-wrap{background:rgba(4,2,15,0.96);backdrop-filter:blur(40px);
  border-bottom:1px solid rgba(139,92,246,0.20);padding:5px 0;margin-bottom:6px;
  box-shadow:0 4px 30px rgba(0,0,0,0.60);}
.nav-logo{font-family:'Bebas Neue',sans-serif;font-size:1.4rem;letter-spacing:5px;
  color:#a78bfa;text-shadow:0 0 20px rgba(167,139,250,0.55);line-height:1;}

div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"]>button{
  background:rgba(8,5,22,0.85)!important;border:1px solid rgba(139,92,246,0.28)!important;
  color:rgba(255,255,255,0.72)!important;border-radius:8px!important;
  font-size:0.78rem!important;font-weight:600!important;height:30px!important;
  min-height:30px!important;white-space:nowrap!important;transition:all 0.15s!important;
  box-shadow:none!important;}
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"]>button:hover{
  background:rgba(139,92,246,0.22)!important;border-color:rgba(167,139,250,0.65)!important;
  color:#fff!important;box-shadow:0 0 12px rgba(139,92,246,0.30)!important;}
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"]:last-child>button{
  background:rgba(229,9,20,0.20)!important;border-color:rgba(229,9,20,0.45)!important;}

/* ACTION BUTTONS */
.stButton>button{
  background:linear-gradient(135deg,#7c3aed 0%,#4f46e5 50%,#2563eb 100%)!important;
  border:none!important;color:#fff!important;border-radius:14px!important;
  font-weight:700!important;font-size:0.95rem!important;letter-spacing:0.5px!important;
  box-shadow:0 6px 24px rgba(109,40,217,0.45),0 0 0 1px rgba(139,92,246,0.20)!important;
  transition:all 0.22s cubic-bezier(0.34,1.56,0.64,1)!important;}
.stButton>button:hover{transform:translateY(-3px) scale(1.02)!important;
  box-shadow:0 10px 32px rgba(109,40,217,0.65)!important;}

/* INPUTS */
[data-testid="stWidgetLabel"],[data-testid="stWidgetLabel"] p{
  color:rgba(196,181,253,0.90)!important;font-size:0.78rem!important;
  font-weight:700!important;letter-spacing:2px!important;text-transform:uppercase!important;}
input,.stTextArea textarea,.stNumberInput input{
  background:rgba(15,10,40,0.80)!important;
  border:1.5px solid rgba(139,92,246,0.28)!important;color:#fff!important;
  border-radius:12px!important;backdrop-filter:blur(10px)!important;}
input:focus{border-color:rgba(167,139,250,0.70)!important;
  box-shadow:0 0 0 3px rgba(139,92,246,0.15)!important;}
.stSelectbox [data-baseweb="select"]>div{
  background:rgba(15,10,40,0.80)!important;
  border:1.5px solid rgba(139,92,246,0.28)!important;color:#fff!important;
  border-radius:12px!important;}
.stMarkdown p{color:rgba(220,210,255,0.80)!important;line-height:1.7!important;}
.stSlider [data-testid="stWidgetLabel"] p{color:rgba(196,181,253,0.90)!important;}

/* GLASS CARDS */
.glass-card{
  background:rgba(15,10,40,0.65);
  border:1px solid rgba(139,92,246,0.22);
  border-radius:20px;
  backdrop-filter:blur(30px);-webkit-backdrop-filter:blur(30px);
  box-shadow:0 8px 40px rgba(0,0,0,0.50),inset 0 1px 0 rgba(255,255,255,0.06);
  position:relative;overflow:hidden;}
.glass-card::before{content:'';position:absolute;top:0;left:0;right:0;height:1.5px;
  background:linear-gradient(90deg,transparent,#7c3aed 35%,#818cf8 65%,transparent);}

@keyframes moonFloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
@keyframes starPulse{0%,100%{opacity:0.6}50%{opacity:1}}
@keyframes fadeUp{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
</style>
""", unsafe_allow_html=True)

# ── NAV ───────────────────────────────────────────────────────────────────────
try:
    from nav_component import render_nav
    render_nav("sleep", uname)
except Exception as _nav_err:
    st.warning(f"Nav error: {_nav_err}")

# ── LOAD DATA ─────────────────────────────────────────────────────────────────
today     = date.today()
today_str = today.isoformat()

@st.cache_data(ttl=120)
def _load_sleep(uname):
    try:
        from utils.db import get_sleep
        return get_sleep(uname, limit=30)
    except Exception:
        return []

if "sleep_log" not in st.session_state:
    st.session_state.sleep_log = _load_sleep(uname)

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

hrs_color  = "#E50914" if avg_hrs < 6 else "#f59e0b" if avg_hrs < 7 else "#22c55e"
qual_stars = "★" * int(round(avg_qual)) + "☆" * (5 - int(round(avg_qual))) if avg_qual > 0 else "☆☆☆☆☆"
qual_label = ("💀 Critical" if avg_qual < 2 else "😴 Poor" if avg_qual < 3
              else "😐 Fair" if avg_qual < 4 else "😊 Good" if avg_qual < 4.5 else "🌟 Excellent")
sleep_tip  = ("⚠️ You need more sleep urgently. Take rest today." if avg_hrs < 6
              else "🟡 Try to get 30 more minutes — it makes a big difference." if avg_hrs < 7
              else "✅ Great sleep habits! Your recovery is on point." if avg_hrs < 9
              else "💤 You're well rested and primed to perform.")

st.markdown(f"""
<div style='background:linear-gradient(135deg,rgba(109,40,217,0.22),rgba(79,70,229,0.12) 50%,rgba(4,2,15,0.75));
  border:1px solid rgba(139,92,246,0.35);border-radius:24px;padding:32px 36px;margin:10px 0 24px;
  position:relative;overflow:hidden;backdrop-filter:blur(30px);
  box-shadow:0 20px 60px rgba(0,0,0,0.60),inset 0 1px 0 rgba(255,255,255,0.07);'>
  <!-- Top glow line -->
  <div style='position:absolute;top:0;left:0;right:0;height:2px;
    background:linear-gradient(90deg,transparent,#7c3aed 30%,#818cf8 60%,#60a5fa,transparent)'></div>
  <!-- Moon decoration -->
  <div style='position:absolute;right:32px;top:24px;font-size:4.5rem;opacity:0.12;
    animation:moonFloat 6s ease-in-out infinite;user-select:none;line-height:1'>🌙</div>
  <!-- Stars decoration -->
  <div style='position:absolute;right:120px;top:18px;font-size:1rem;opacity:0.20;
    animation:starPulse 3s ease-in-out infinite;'>✦</div>
  <div style='position:absolute;right:90px;top:50px;font-size:0.7rem;opacity:0.15;
    animation:starPulse 4s ease-in-out infinite 1s;'>✦</div>
  <div style='position:absolute;right:160px;top:40px;font-size:0.5rem;opacity:0.18;
    animation:starPulse 5s ease-in-out infinite 2s;'>✦</div>

  <div style='font-size:0.68rem;font-weight:800;letter-spacing:3.5px;text-transform:uppercase;
    color:rgba(167,139,250,0.75);margin-bottom:10px;'>🌙 Sleep Tracker</div>
  <div style='font-family:Barlow Condensed,sans-serif;font-size:clamp(2rem,5vw,3.2rem);
    font-weight:900;text-transform:uppercase;line-height:1;margin-bottom:20px;'>
    <span style='background:linear-gradient(90deg,#c4b5fd,#818cf8);
      -webkit-background-clip:text;-webkit-text-fill-color:transparent;
      background-clip:text;'>{_display}'s</span>
    <span style='color:#fff;'> Sleep</span>
  </div>

  <!-- Stat cards row -->
  <div style='display:grid;grid-template-columns:repeat(4,1fr);gap:12px;'>
    <div style='background:rgba(255,255,255,0.05);border:1px solid rgba(139,92,246,0.20);
      border-radius:16px;padding:16px;text-align:center;backdrop-filter:blur(10px);'>
      <div style='font-size:0.58rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;
        color:rgba(196,181,253,0.55);margin-bottom:6px;'>7-Day Avg</div>
      <div style='font-family:Bebas Neue,sans-serif;font-size:2.6rem;color:{hrs_color};
        line-height:1;text-shadow:0 0 20px {hrs_color}40;'>{avg_hrs}h</div>
      <div style='font-size:0.62rem;color:rgba(255,255,255,0.35);margin-top:3px;'>hours/night</div>
    </div>
    <div style='background:rgba(255,255,255,0.05);border:1px solid rgba(139,92,246,0.20);
      border-radius:16px;padding:16px;text-align:center;backdrop-filter:blur(10px);'>
      <div style='font-size:0.58rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;
        color:rgba(196,181,253,0.55);margin-bottom:6px;'>Quality</div>
      <div style='font-family:Bebas Neue,sans-serif;font-size:2.6rem;color:#c4b5fd;
        line-height:1;text-shadow:0 0 20px rgba(196,181,253,0.40);'>{avg_qual if avg_qual > 0 else "—"}</div>
      <div style='font-size:0.62rem;color:rgba(255,255,255,0.35);margin-top:3px;'>{qual_label}</div>
    </div>
    <div style='background:rgba(255,255,255,0.05);border:1px solid rgba(139,92,246,0.20);
      border-radius:16px;padding:16px;text-align:center;backdrop-filter:blur(10px);'>
      <div style='font-size:0.58rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;
        color:rgba(196,181,253,0.55);margin-bottom:6px;'>Streak</div>
      <div style='font-family:Bebas Neue,sans-serif;font-size:2.6rem;color:#60a5fa;
        line-height:1;text-shadow:0 0 20px rgba(96,165,250,0.40);'>{streak_s}</div>
      <div style='font-size:0.62rem;color:rgba(255,255,255,0.35);margin-top:3px;'>days logged</div>
    </div>
    <div style='background:rgba(255,255,255,0.05);border:1px solid rgba(139,92,246,0.20);
      border-radius:16px;padding:16px;text-align:center;backdrop-filter:blur(10px);'>
      <div style='font-size:0.58rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;
        color:rgba(196,181,253,0.55);margin-bottom:6px;'>Total</div>
      <div style='font-family:Bebas Neue,sans-serif;font-size:2.6rem;color:#34d399;
        line-height:1;text-shadow:0 0 20px rgba(52,211,153,0.40);'>{len(sleep_log)}</div>
      <div style='font-size:0.62rem;color:rgba(255,255,255,0.35);margin-top:3px;'>nights logged</div>
    </div>
  </div>

  <!-- Tip bar -->
  <div style='margin-top:16px;background:rgba(139,92,246,0.10);border:1px solid rgba(139,92,246,0.20);
    border-radius:12px;padding:10px 16px;font-size:0.82rem;color:rgba(220,210,255,0.75);'>
    {sleep_tip}
  </div>
</div>
""", unsafe_allow_html=True)

# ── LOG + CHART COLUMNS ───────────────────────────────────────────────────────
col_log, col_chart = st.columns([1, 1.4], gap="large")

# ── LOG FORM ──────────────────────────────────────────────────────────────────
with col_log:
    already_logged = today_entry is not None
    border_col = "rgba(52,211,153,0.40)" if already_logged else "rgba(139,92,246,0.30)"
    top_col    = "#34d399" if already_logged else "#7c3aed"
    status_txt = "✅ Tonight Already Logged" if already_logged else "🌙 Log Tonight's Sleep"
    status_col = "rgba(52,211,153,0.80)" if already_logged else "rgba(196,181,253,0.80)"

    st.markdown(f"""
<div style='background:rgba(12,8,32,0.75);border:1px solid {border_col};border-radius:22px;
  padding:22px 26px;position:relative;overflow:hidden;
  backdrop-filter:blur(30px);-webkit-backdrop-filter:blur(30px);
  box-shadow:0 12px 40px rgba(0,0,0,0.50),inset 0 1px 0 rgba(255,255,255,0.06);
  margin-bottom:16px'>
  <div style='position:absolute;top:0;left:0;right:0;height:1.5px;
    background:linear-gradient(90deg,transparent,{top_col},transparent)'></div>
  <div style='font-size:0.65rem;font-weight:800;letter-spacing:2.5px;text-transform:uppercase;
    color:{status_col};margin-bottom:16px;display:flex;align-items:center;gap:8px;'>
    {status_txt}
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
            _load_sleep.clear()
            st.session_state.sleep_log = get_sleep(uname, limit=30)
            st.session_state.pop("_sleep_stats_done", None)
            # Bust charts page cache so it shows new sleep data
            st.cache_data.clear()
            st.toast("✅ Sleep logged!", icon="😴")
            st.rerun()
        except Exception as e:
            st.error(f"Save failed: {e}")

# ── 7-DAY CHART ───────────────────────────────────────────────────────────────
with col_chart:
    st.markdown(f"""
<div style='background:rgba(12,8,32,0.75);border:1px solid rgba(139,92,246,0.22);border-radius:22px;
  padding:22px 26px;backdrop-filter:blur(30px);-webkit-backdrop-filter:blur(30px);
  box-shadow:0 12px 40px rgba(0,0,0,0.50),inset 0 1px 0 rgba(255,255,255,0.06);
  position:relative;overflow:hidden'>
  <div style='position:absolute;top:0;left:0;right:0;height:1.5px;
    background:linear-gradient(90deg,transparent,#60a5fa,transparent)'></div>
  <div style='font-size:0.65rem;font-weight:800;letter-spacing:2.5px;text-transform:uppercase;
    color:rgba(96,165,250,0.80);margin-bottom:18px;'>📊 Last 7 Nights</div>
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