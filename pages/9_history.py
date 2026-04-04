# -*- coding: utf-8 -*-
import streamlit as st
import os, sys
from datetime import date, timedelta
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth_token import logout

st.set_page_config(page_title="History | FitPlan Pro", page_icon="📅", layout="wide",
                   initial_sidebar_state="collapsed")
if not st.session_state.get("logged_in"): st.switch_page("app.py")
if "user_data" not in st.session_state: st.switch_page("pages/1_Profile.py")

uname = st.session_state.get("username", "Athlete")
data  = st.session_state.user_data

st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:opsz,wght@9..40,400;9..40,600;9..40,700&display=swap');
#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stDecoration"],
[data-testid="stSidebarNav"],section[data-testid="stSidebar"]{display:none!important;}
html,body,.stApp{background:#0d0806!important;color:#fff!important;font-family:'DM Sans',sans-serif!important;}
[data-testid="stAppViewContainer"]{
  background:radial-gradient(ellipse at center,transparent 0%,rgba(0,0,0,0.55) 100%),
    linear-gradient(180deg,rgba(5,2,1,0.78) 0%,rgba(5,2,1,0.66) 50%,rgba(5,2,1,0.83) 100%),
    url('https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=1800&q=80&auto=format&fit=crop')
    center center/cover no-repeat fixed!important;}
[data-testid="stAppViewContainer"]>section>div.block-container{
  max-width:1100px!important;margin:0 auto!important;padding:0 24px 80px!important;}
[data-testid="stWidgetLabel"],[data-testid="stWidgetLabel"] p{color:rgba(255,255,255,0.80)!important;}
.stButton>button{background:linear-gradient(135deg,rgba(229,9,20,0.85),rgba(160,0,10,0.90))!important;
  border:none!important;color:#fff!important;border-radius:10px!important;
  font-size:1.0rem!important;font-weight:700!important;transition:all 0.20s!important;}
.stButton>button:hover{transform:translateY(-2px)!important;}
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"] > button{
  background:rgba(15,5,3,0.82)!important;border:2px solid rgba(229,9,20,0.57)!important;
  color:rgba(255,255,255,0.88)!important;border-radius:9px!important;
  font-size:0.85rem!important;font-weight:700!important;padding:5px 10px!important;
  height:34px!important;min-height:34px!important;}
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"] > button:hover{
  background:rgba(229,9,20,0.26)!important;border-color:rgba(229,9,20,0.82)!important;}
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"]:last-child > button{
  background:linear-gradient(135deg,#c0000c,#8b0000)!important;}
.nav-logo{font-family:'Bebas Neue',cursive;font-size:1.3rem;letter-spacing:4px;
  color:#E50914;text-shadow:0 0 18px rgba(229,9,20,0.55);line-height:1;}
.history-card{background:rgba(8,3,1,0.68);border:2px solid rgba(229,9,20,0.25);
  border-radius:14px;padding:16px 20px;margin-bottom:10px;
  display:flex;align-items:center;gap:16px;backdrop-filter:blur(28px);
  transition:border-color 0.2s;}
.history-card:hover{border-color:rgba(229,9,20,0.50);}
.history-card.done{border-left:4px solid #22c55e;}
.history-card.skipped{border-left:4px solid #fbbf24;}
.history-card.rest{border-left:4px solid #94a3b8;opacity:0.70;}
.history-card.missed{border-left:4px solid #ef4444;}
.h-date{font-size:0.85rem;font-weight:700;color:rgba(255,255,255,0.90);
  min-width:70px;text-align:center;}
.h-day-badge{font-family:'Bebas Neue',sans-serif;font-size:1.6rem;color:#E50914;
  letter-spacing:1px;min-width:60px;}
.h-muscle{font-size:1.05rem;font-weight:600;color:#fff;flex:1;}
.h-status{font-size:0.80rem;font-weight:700;letter-spacing:1.5px;
  text-transform:uppercase;padding:3px 10px;border-radius:20px;}
.h-status.done{background:rgba(34,197,94,0.15);color:#4ade80;border:1px solid rgba(34,197,94,0.35);}
.h-status.skipped{background:rgba(251,191,36,0.12);color:#fbbf24;border:1px solid rgba(251,191,36,0.30);}
.h-status.rest{background:rgba(148,163,184,0.12);color:#94a3b8;border:1px solid rgba(148,163,184,0.28);}
.h-status.missed{background:rgba(239,68,68,0.12);color:#f87171;border:1px solid rgba(239,68,68,0.28);}
.stat-box{background:rgba(229,9,20,0.10);border:2px solid rgba(229,9,20,0.35);
  border-radius:12px;padding:14px 18px;text-align:center;backdrop-filter:blur(28px);}
html,body,.stApp,.stMarkdown,p,div,span,label{text-shadow:0 2px 6px rgba(0,0,0,0.98)!important;}
[data-testid="stWidgetLabel"],[data-testid="stWidgetLabel"] p{color:#fff!important;font-size:1.05rem!important;font-weight:700!important;}
.stMarkdown p,.stMarkdown li{color:#fff!important;font-size:1.05rem!important;line-height:1.75!important;}
</style>""", unsafe_allow_html=True)

# ── NAV ───────────────────────────────────────────────────────────────────────
_n = st.columns([1.5,1,1,1,1,1,1,1.2])
with _n[0]: st.markdown("<div class='nav-logo'>&#9889; FITPLAN PRO</div>", unsafe_allow_html=True)
with _n[1]:
    if st.button("🏠 Home",     key="hi_db", use_container_width=True): st.switch_page("pages/2_Dashboard.py")
with _n[2]:
    if st.button("⚡ Workout",  key="hi_wp", use_container_width=True): st.switch_page("pages/3_Workout_Plan.py")
with _n[3]:
    if st.button("🥗 Diet",     key="hi_dp", use_container_width=True): st.switch_page("pages/4_Diet_Plan.py")
with _n[4]:
    if st.button("🤖 AI Coach", key="hi_ai", use_container_width=True): st.switch_page("pages/5_ai_coach.py")
with _n[5]:
    if st.button("🏆 Records",  key="hi_rc", use_container_width=True): st.switch_page("pages/6_records.py")
with _n[6]:
    if st.button("● 📅 History",key="hi_hi", use_container_width=True): st.switch_page("pages/9_history.py")
with _n[7]:
    if st.button("🚪 Sign Out", key="hi_so", use_container_width=True):
        logout(uname)
        for _k in ["logged_in","username","auth_token","user_data","workout_plan","structured_days",
                   "dietary_type","full_plan_data","plan_id","plan_start","plan_duration","plan_for",
                   "force_regen","tracking","_plan_checked","_db_loaded_dash"]:
            st.session_state.pop(_k, None)
        st.switch_page("app.py")

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='background:rgba(10,6,4,0.80);border:1.5px solid rgba(229,9,20,0.28);
  border-radius:18px;padding:28px 36px;margin-bottom:24px;backdrop-filter:blur(12px);
  position:relative;overflow:hidden'>
  <div style='position:absolute;top:0;left:0;right:0;height:2px;
    background:linear-gradient(90deg,transparent,#E50914,transparent)'></div>
  <div style='font-size:0.85rem;font-weight:700;letter-spacing:4px;text-transform:uppercase;
    color:rgba(229,9,20,0.80);margin-bottom:8px'>&#128197; Workout History</div>
  <div style='font-family:Bebas Neue,sans-serif;font-size:2.4rem;letter-spacing:2px;color:#fff;
    line-height:1;margin-bottom:6px'>Your Journey So Far</div>
  <div style='font-size:1.00rem;color:rgba(255,255,255,0.75)'>
    Every session logged. Every rep counted. History survives plan changes.</div>
</div>
""", unsafe_allow_html=True)

# ── LOAD HISTORY FROM DB (persists across plan changes) ───────────────────────
# History is stored separately in DB — NOT derived from current plan
# This means it survives plan deletion and regeneration
if not st.session_state.get("_hist_loaded"):
    st.session_state._hist_loaded = True
    try:
        from utils.db import get_workout_history
        _db_hist = get_workout_history(uname)
        if _db_hist:
            st.session_state._workout_history = _db_hist
    except Exception:
        pass

# Also build history from current plan tracking (for current plan entries not yet in DB)
_db_history = st.session_state.get("_workout_history", [])

# ── BUILD COMBINED HISTORY ────────────────────────────────────────────────────
# Merge DB history + current session tracking
sdays      = st.session_state.get("structured_days", [])
tracking   = st.session_state.get("tracking", {})
plan_start_str = st.session_state.get("plan_start", date.today().isoformat())
try:
    plan_start = date.fromisoformat(plan_start_str)
except Exception:
    plan_start = date.today()

# Build from current plan if available
current_history = []
if sdays:
    for i, sd in enumerate(sdays):
        dn      = sd.get("day", i+1)
        mg      = sd.get("muscle_group", "Workout")
        is_rest = sd.get("is_rest_day", False)
        ex_cnt  = len(sd.get("workout", []))
        work_date = plan_start + timedelta(days=i)

        if work_date > date.today():
            continue  # skip future

        status_raw = tracking.get(work_date.isoformat(), {}).get("status", "")
        if is_rest:
            status = "rest"
        elif status_raw == "done":
            status = "done"
        elif status_raw == "skipped":
            status = "skipped"
        elif work_date < date.today():
            status = "missed"
        else:
            status = "pending"

        current_history.append({
            "day": dn,
            "date": work_date,
            "date_str": work_date.isoformat(),
            "muscle": mg,
            "status": status,
            "exercises": ex_cnt,
            "is_rest": is_rest,
            "source": "current",
        })

# Merge DB history (old plans) with current plan history
# DB entries for dates not in current plan = old plan data
current_dates = {h["date_str"] for h in current_history}
merged = list(current_history)

for db_entry in _db_history:
    d_str = db_entry.get("date", "")
    if d_str and d_str not in current_dates:
        try:
            d = date.fromisoformat(d_str)
            if d <= date.today():
                merged.append({
                    "day":       db_entry.get("day", "?"),
                    "date":      d,
                    "date_str":  d_str,
                    "muscle":    db_entry.get("muscle_group", "Workout"),
                    "status":    db_entry.get("status", "done"),
                    "exercises": db_entry.get("exercises", 0),
                    "is_rest":   db_entry.get("is_rest", False),
                    "source":    "archive",
                })
        except Exception:
            pass

# Sort most recent first
merged.sort(key=lambda x: x["date"], reverse=True)

# ── SAVE CURRENT TRACKING TO DB ───────────────────────────────────────────────
# Persist current plan's completed workouts to DB so they survive regeneration
if sdays and tracking:
    try:
        from utils.db import save_workout_history
        history_to_save = [h for h in current_history if h["status"] in ("done","skipped")]
        if history_to_save:
            save_workout_history(uname, history_to_save)
    except Exception:
        pass

# ── EMPTY STATE ───────────────────────────────────────────────────────────────
if not merged:
    st.markdown("""
    <div style='text-align:center;padding:60px;color:rgba(255,255,255,0.75)'>
      <div style='font-size:3rem;margin-bottom:12px'>&#128197;</div>
      <div style='font-size:1.1rem;font-weight:600;margin-bottom:6px'>No workout history yet</div>
      <div style='font-size:1.00rem'>Complete workouts to see your history here.<br>
      History is saved permanently and survives plan changes.</div>
    </div>""", unsafe_allow_html=True)
    if st.button("Generate My Plan", use_container_width=False):
        st.switch_page("pages/1_Profile.py")
    st.stop()

# ── SUMMARY STATS ─────────────────────────────────────────────────────────────
done_total    = sum(1 for h in merged if h["status"]=="done")
skipped_total = sum(1 for h in merged if h["status"]=="skipped")
missed_total  = sum(1 for h in merged if h["status"]=="missed")
total_sessions = done_total + skipped_total + missed_total
consistency    = int(done_total / max(total_sessions, 1) * 100)
c_col = "#22c55e" if consistency >= 70 else ("#fbbf24" if consistency >= 40 else "#ef4444")

# Archive badge — show if there are old plan entries
archive_count = sum(1 for h in merged if h.get("source")=="archive")
if archive_count > 0:
    st.markdown(
        f"<div style='background:rgba(251,191,36,0.08);border:1px solid rgba(251,191,36,0.28);"
        f"border-radius:10px;padding:8px 16px;margin-bottom:14px;font-size:0.85rem;"
        f"color:rgba(251,191,36,0.80);display:flex;align-items:center;gap:8px'>"
        f"<span>📦</span>"
        f"<span>{archive_count} session{'s' if archive_count>1 else ''} from previous plans are preserved in your history.</span>"
        f"</div>",
        unsafe_allow_html=True
    )

s1, s2, s3, s4 = st.columns(4)
with s1:
    st.markdown(
        f"<div class='stat-box'>"
        f"<div style='font-family:Bebas Neue,sans-serif;font-size:2.2rem;color:#22c55e'>{done_total}</div>"
        f"<div style='font-size:0.80rem;color:rgba(255,255,255,0.70);letter-spacing:2px;text-transform:uppercase'>Completed</div>"
        f"</div>", unsafe_allow_html=True)
with s2:
    st.markdown(
        f"<div class='stat-box' style='border-color:rgba(251,191,36,0.28)'>"
        f"<div style='font-family:Bebas Neue,sans-serif;font-size:2.2rem;color:#fbbf24'>{skipped_total}</div>"
        f"<div style='font-size:0.80rem;color:rgba(255,255,255,0.70);letter-spacing:2px;text-transform:uppercase'>Skipped</div>"
        f"</div>", unsafe_allow_html=True)
with s3:
    st.markdown(
        f"<div class='stat-box' style='border-color:rgba(239,68,68,0.28)'>"
        f"<div style='font-family:Bebas Neue,sans-serif;font-size:2.2rem;color:#f87171'>{missed_total}</div>"
        f"<div style='font-size:0.80rem;color:rgba(255,255,255,0.70);letter-spacing:2px;text-transform:uppercase'>Missed</div>"
        f"</div>", unsafe_allow_html=True)
with s4:
    st.markdown(
        f"<div class='stat-box' style='border-color:rgba(34,197,94,0.28)'>"
        f"<div style='font-family:Bebas Neue,sans-serif;font-size:2.2rem;color:{c_col}'>{consistency}%</div>"
        f"<div style='font-size:0.80rem;color:rgba(255,255,255,0.70);letter-spacing:2px;text-transform:uppercase'>Consistency</div>"
        f"</div>", unsafe_allow_html=True)

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

# ── FILTER ────────────────────────────────────────────────────────────────────
fc1, fc2 = st.columns([2, 4])
with fc1:
    filter_opt = st.selectbox(
        "Filter", ["All","Completed","Skipped","Missed","Rest Days","Archived (Old Plans)"],
        key="hist_filter", label_visibility="collapsed"
    )

filter_map = {
    "All": None, "Completed":"done", "Skipped":"skipped",
    "Missed":"missed", "Rest Days":"rest", "Archived (Old Plans)":"archive"
}
show_status = filter_map[filter_opt]

if show_status == "archive":
    shown = [h for h in merged if h.get("source")=="archive"]
else:
    shown = [h for h in merged if show_status is None or h["status"]==show_status]

# ── HISTORY LIST ──────────────────────────────────────────────────────────────
st.markdown(
    f"<div style='font-size:0.75rem;color:rgba(255,255,255,0.40);margin-bottom:10px'>"
    f"Showing {len(shown)} of {len(merged)} total sessions</div>",
    unsafe_allow_html=True
)

if not shown:
    st.markdown(
        "<div style='text-align:center;padding:30px;color:rgba(255,255,255,0.55);font-size:1.00rem'>"
        "No entries match this filter.</div>",
        unsafe_allow_html=True
    )
else:
    status_icons  = {"done":"✅","skipped":"⏭️","missed":"❌","rest":"😴","pending":"⏳"}
    status_labels = {"done":"Completed","skipped":"Skipped","missed":"Missed",
                     "rest":"Rest Day","pending":"Pending"}

    for h in shown:
        d_str   = h["date"].strftime("%b %d")
        day_ago = (date.today() - h["date"]).days
        ago_str = "Today" if day_ago==0 else ("Yesterday" if day_ago==1 else f"{day_ago}d ago")
        # Archive badge
        arch_badge = ""
        if h.get("source") == "archive":
            arch_badge = "<span style='font-size:0.65rem;background:rgba(251,191,36,0.12);border:1px solid rgba(251,191,36,0.28);border-radius:10px;padding:2px 7px;color:rgba(251,191,36,0.70);margin-left:8px'>📦 Archive</span>"

            _hstatus = h["status"]
            _hicon   = status_icons.get(_hstatus, "")
            _hlabel  = status_labels.get(_hstatus, "")
            _hexc    = "Rest day" if h["is_rest"] else str(h["exercises"]) + " exercises"
            st.markdown(
                f"<div class='history-card {_hstatus}'>"
                f"<div class='h-date'>{d_str}<br>"
                f"<span style='font-size:0.75rem;color:rgba(255,255,255,0.50)'>{ago_str}</span></div>"
                f"<div class='h-day-badge'>Day {h['day']}</div>"
                f"<div style='flex:1'>"
                f"<div class='h-muscle'>{h['muscle']}{arch_badge}</div>"
                f"<div style='font-size:0.80rem;color:rgba(255,255,255,0.50);margin-top:2px'>{_hexc}</div>"
                f"</div>"
                f"<div class='h-status {_hstatus}'>{_hicon} {_hlabel}</div>"
                f"</div>",
                unsafe_allow_html=True
            )