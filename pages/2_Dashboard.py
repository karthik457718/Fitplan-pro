import streamlit as st
import os, sys, re
from datetime import datetime, date, timedelta
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth_token import logout

st.set_page_config(page_title="Dashboard | FitPlan Pro", page_icon="🏠", layout="wide", initial_sidebar_state="collapsed")

if not st.session_state.get("logged_in"):
    st.switch_page("app.py")
if "user_data" not in st.session_state:
    try:
        from utils.db import get_user_profile
        _u = st.session_state.get("username","")
        if _u:
            _p = get_user_profile(_u)
            if _p: st.session_state.user_data = _p
            else: st.switch_page("pages/1_Profile.py")
        else: st.switch_page("pages/1_Profile.py")
    except Exception: st.switch_page("pages/1_Profile.py")

uname     = st.session_state.get("username","Athlete")
data      = st.session_state.user_data
today_str = date.today().isoformat()

# ── Load from DB once ─────────────────────────────────────────────────────────
if not st.session_state.get("_db_loaded_dash"):
    st.session_state._db_loaded_dash = True
    if not st.session_state.get("structured_days"):
        try:
            from utils.db import get_active_plan
            ex = get_active_plan(uname)
            if ex and ex.get("days"):
                sd = sorted([{
                    "day":d.get("day_number",1),"is_rest_day":d.get("is_rest_day",False),
                    "muscle_group":d.get("muscle_group","Full Body"),
                    "workout":d.get("workout_json",[]),"dietary":d.get("dietary_json",{}),
                    "pre_stretch":d.get("pre_stretch_json",[]),"post_stretch":d.get("post_stretch_json",[]),
                } for d in ex["days"]], key=lambda x:x["day"])
                st.session_state.structured_days = sd
                st.session_state.dietary_type    = ex.get("dietary_type","veg")
                st.session_state.plan_id         = ex.get("plan_id","")
                st.session_state.plan_start      = ex.get("created_at_date",today_str)
                st.session_state.plan_duration   = len(sd)
        except Exception: pass
    try:
        from utils.db import get_all_progress
        pid = st.session_state.get("plan_id","")
        if pid:
            for prog in get_all_progress(uname, pid):
                dn = prog["day_number"]
                for k,v in prog["workout_checks"].items():
                    if v: st.session_state[f"ex_d{dn}_{k.replace('ex_','')}"] = True
                for meal,v in prog["dietary_checks"].items():
                    if v: st.session_state[f"meal_d{dn}_{meal}"] = True
    except Exception: pass
    try:
        from utils.db import get_streak
        sd2 = get_streak(uname)
        st.session_state._db_streak = sd2.get("current_streak",0)
    except Exception: st.session_state._db_streak = 0

# ── State ─────────────────────────────────────────────────────────────────────
_actual = len(st.session_state.get("structured_days",[])) or data.get("total_days",20)
for k,v in [("tracking",{}),("plan_start",today_str),("plan_duration",_actual)]:
    if k not in st.session_state: st.session_state[k] = v
_sdc = len(st.session_state.get("structured_days",[]))
if _sdc > 0: st.session_state.plan_duration = _sdc

tracking      = st.session_state.tracking
plan_start    = date.fromisoformat(st.session_state.plan_start)
plan_duration = int(st.session_state.plan_duration) or 1

calendar_days = []
for i in range(plan_duration):
    d = plan_start + timedelta(days=i)
    calendar_days.append({"date":d,"day_idx":i%plan_duration,
                          "status":tracking.get(d.isoformat(),{}).get("status","pending")})

done_count    = sum(1 for cd in calendar_days if cd["status"]=="done")
skipped_count = sum(1 for cd in calendar_days if cd["status"]=="skipped")
pct           = int(done_count/plan_duration*100)

if not st.session_state.get("_streak_synced"):
    try:
        from utils.db import get_streak as _gs2
        _sd_fresh = _gs2(uname)
        st.session_state._db_streak = _sd_fresh.get("current_streak", 0)
        st.session_state._streak_synced = True
    except Exception:
        pass
streak = st.session_state.get("_db_streak", 0)

today_entry  = next((cd for cd in calendar_days if cd["date"]==date.today()),
                    {"date":date.today(),"day_idx":0,"status":"pending"})
today_status = today_entry["status"]

_sdays    = st.session_state.get("structured_days",[])
_today_offset = (date.today() - plan_start).days
_tid = max(0, min(_today_offset, len(_sdays)-1)) if _sdays else today_entry["day_idx"]
_today_sd = _sdays[_tid] if _sdays and _tid < len(_sdays) else None
if _today_sd:
    _mg           = _today_sd.get("muscle_group","Workout")
    _dn           = _today_sd.get("day",_tid+1)
    today_title   = f"DAY {_dn} — {_mg.upper()}"
    _IC           = ["🏋","💪","🔄","🦵","⬆️","🤸","🏃","🥊","🧗","🚴","🔥","⚡"]
    today_exercises = [{"icon":_IC[i%len(_IC)],"name":e.get("name",f"Ex {i+1}"),
                        "sets":str(e.get("sets",3)),"reps":str(e.get("reps","12")),
                        "rest":e.get("rest","60s")}
                       for i,e in enumerate(_today_sd.get("workout",[]))]
else:
    today_title     = f"DAY {_tid+1}"
    today_exercises = []

week_start = date.today()-timedelta(days=date.today().weekday())
DAYS_S     = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
week_data  = [{"day":DAYS_S[i],
               "done":  tracking.get((week_start+timedelta(days=i)).isoformat(),{}).get("status","")=="done",
               "skipped":tracking.get((week_start+timedelta(days=i)).isoformat(),{}).get("status","")=="skipped",
               "date":week_start+timedelta(days=i)} for i in range(7)]

# ══════════════════════════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow+Condensed:wght@700;800;900&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700&display=swap');
#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stDecoration"],
[data-testid="stSidebarNav"],section[data-testid="stSidebar"]{display:none!important;}
html,body,.stApp{background:#050202!important;color:#fff!important;font-family:'DM Sans',sans-serif!important;}
[data-testid="stAppViewContainer"]::before{
  content:'';position:fixed;inset:0;z-index:0;
  background:url('https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=1800&q=80&auto=format&fit=crop')
    center center/cover no-repeat;
  filter:blur(8px) brightness(0.25) saturate(0.55);transform:scale(1.06);}
[data-testid="stAppViewContainer"]{
  background:linear-gradient(160deg,rgba(3,1,0,0.88) 0%,rgba(5,2,0,0.78) 40%,rgba(3,1,0,0.92) 100%)!important;position:relative;}
[data-testid="stAppViewContainer"]>section>div.block-container{
  max-width:1200px!important;margin:0 auto!important;padding:0 24px 80px!important;position:relative;z-index:2;}
[data-testid="stWidgetLabel"],[data-testid="stWidgetLabel"] p{color:rgba(255,255,255,0.75)!important;font-size:1.05rem!important;font-weight:600!important;}
.stNumberInput>div>div>input,.stTextInput>div>div>input,.stTextArea>div>div>textarea{
  background:rgba(255,255,255,0.08)!important;border:1.5px solid rgba(255,255,255,0.20)!important;
  color:#fff!important;border-radius:14px!important;backdrop-filter:blur(28px)!important;
  font-size:1.05rem!important;font-weight:500!important;}
.stNumberInput [data-testid="stNumberInputStepUp"],.stNumberInput [data-testid="stNumberInputStepDown"]{
  background:rgba(229,9,20,0.25)!important;border:none!important;color:#fff!important;border-radius:8px!important;}
[data-baseweb="select"]>div{background:rgba(255,255,255,0.08)!important;border:1.5px solid rgba(255,255,255,0.20)!important;
  border-radius:14px!important;backdrop-filter:blur(28px)!important;color:#fff!important;}
[data-baseweb="popover"] [role="option"]{background:rgba(12,6,4,0.97)!important;color:#fff!important;}
[data-baseweb="popover"] [role="option"]:hover{background:rgba(229,9,20,0.22)!important;}
.stButton>button{background:linear-gradient(135deg,rgba(229,9,20,0.85),rgba(160,0,10,0.90))!important;
  border:2px solid rgba(229,9,20,0.65)!important;color:#fff!important;border-radius:10px!important;
  font-family:'DM Sans',sans-serif!important;font-size:1.0rem!important;font-weight:700!important;
  box-shadow:0 0 12px rgba(229,9,20,0.30)!important;transition:all 0.20s!important;}
.stButton>button:hover{transform:translateY(-2px)!important;box-shadow:0 0 24px rgba(229,9,20,0.60)!important;}
.done-btn .stButton>button{background:linear-gradient(135deg,rgba(34,197,94,0.85),rgba(22,163,74,0.90))!important;
  border-color:rgba(34,197,94,0.55)!important;box-shadow:0 0 12px rgba(34,197,94,0.32)!important;}
.plan-btn .stButton>button{background:linear-gradient(135deg,#E50914,#c0000c)!important;
  animation:glow-r 2.4s ease-in-out infinite!important;}
@keyframes glow-r{0%,100%{box-shadow:0 0 14px rgba(229,9,20,0.45);}50%{box-shadow:0 0 30px rgba(229,9,20,0.75);}}
.stat-mini-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:20px;}
@media(max-width:900px){.stat-mini-grid{grid-template-columns:repeat(2,1fr)!important;}}
.stat-mini{background:rgba(10,3,1,0.88);border:2px solid rgba(229,9,20,0.50);border-radius:12px;
  padding:16px 12px;text-align:center;position:relative;overflow:hidden;
  backdrop-filter:blur(28px) saturate(1.5)!important;
  box-shadow:inset 0 1px 0 rgba(255,255,255,0.08),0 10px 36px rgba(0,0,0,0.70)!important;}
.stat-mini::before{content:'';position:absolute;top:0;left:0;right:0;height:1.5px;
  background:linear-gradient(90deg,transparent,rgba(229,9,20,0.45),transparent);}
.stat-mini.fire{border-color:rgba(229,9,20,0.45);background:rgba(229,9,20,0.10);}
.stat-mini-icon{font-size:1.4rem;margin-bottom:6px;}
.stat-mini-val{font-family:'Bebas Neue',sans-serif;font-size:2rem;color:#fff;letter-spacing:1px;line-height:1;}
.stat-mini-val.red{color:#E50914;}
.stat-mini-lbl{font-size:0.85rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.90);margin-top:4px;}
.sec-lbl{font-size:1.05rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;
  color:rgba(229,9,20,0.75);margin:20px 0 12px;display:flex;align-items:center;gap:8px;}
.sec-lbl::before{content:'';width:16px;height:1.5px;background:#E50914;border-radius:1px;}
.sec-lbl::after{content:'';flex:1;height:1px;background:linear-gradient(90deg,rgba(229,9,20,0.18),transparent);}
.g-panel{background:rgba(8,3,1,0.88);border:2px solid rgba(229,9,20,0.45);border-radius:14px;
  padding:20px 24px;margin-bottom:14px;position:relative;overflow:hidden;backdrop-filter:blur(32px) saturate(1.5)!important;
  box-shadow:inset 0 1px 0 rgba(255,255,255,0.10),0 12px 48px rgba(0,0,0,0.75)!important;}
.g-panel::before{content:'';position:absolute;top:0;left:0;right:0;height:1.5px;
  background:linear-gradient(90deg,transparent,rgba(229,9,20,0.40),transparent);}
.prog-bg{height:8px;background:rgba(255,255,255,0.08);border-radius:4px;overflow:hidden;}
.prog-fill{height:100%;background:linear-gradient(90deg,#E50914,#ff4444);border-radius:4px;}
.status-chip{display:inline-block;padding:3px 12px;border-radius:20px;font-size:0.85rem;font-weight:700;letter-spacing:1px;text-transform:uppercase;}
.status-chip.done{background:rgba(34,197,94,0.15);border:1px solid rgba(34,197,94,0.35);color:#4ade80;}
.status-chip.skipped{background:rgba(251,191,36,0.12);border:1px solid rgba(251,191,36,0.30);color:#fbbf24;}
.status-chip.pending{background:rgba(229,9,20,0.12);border:2px solid rgba(229,9,20,0.45);color:#ff6b6b;}
.ex-list{margin:10px 0;}
.ex-item{display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.05);}
.ex-item:last-child{border-bottom:none;}
.ex-ico{width:28px;height:28px;border-radius:6px;background:rgba(229,9,20,0.12);border:2px solid rgba(229,9,20,0.37);
  display:flex;align-items:center;justify-content:center;font-size:0.75rem;flex-shrink:0;}
.ex-nm{font-size:1.00rem;font-weight:600;color:#fff;flex:1;}
.ex-badges{display:flex;gap:4px;}
.ex-badge{font-size:0.85rem;font-weight:700;padding:2px 7px;border-radius:5px;}
.ex-badge.sets{background:rgba(100,160,255,0.13);color:#93c5fd;border:1px solid rgba(100,160,255,0.22);}
.ex-badge.reps{background:rgba(100,230,180,0.11);color:#6ee7b7;border:1px solid rgba(100,230,180,0.20);}
.ex-badge.rest{background:rgba(255,180,80,0.11);color:#fdba74;border:1px solid rgba(255,180,80,0.20);}
.act-grid{display:flex;gap:6px;align-items:flex-end;height:80px;margin:8px 0 4px;}
.act-bar-wrap{flex:1;display:flex;flex-direction:column;align-items:center;gap:4px;}
.act-bar{width:100%;border-radius:4px 4px 0 0;}
.act-bar.done{background:linear-gradient(180deg,#E50914,rgba(229,9,20,0.55));}
.act-bar.skipped{background:rgba(251,191,36,0.45);}
.act-bar.pending{background:rgba(255,255,255,0.08);}
.act-day{font-size:0.85rem;color:rgba(255,255,255,0.90);font-weight:600;}
.cal-hdr-row{display:grid;grid-template-columns:repeat(7,1fr);gap:3px;margin-bottom:4px;}
.cal-dow{font-size:0.85rem;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:rgba(255,255,255,0.90);text-align:center;padding:4px 0;}
.cal-grid-7{display:grid;grid-template-columns:repeat(7,1fr);gap:3px;margin-bottom:3px;}
.cal-cell{aspect-ratio:1;border-radius:6px;display:flex;flex-direction:column;align-items:center;justify-content:center;background:rgba(0,0,0,0.85);border:1.5px solid rgba(255,255,255,0.28);}
.cal-cell.done-cell{background:rgba(34,197,94,0.32)!important;border:2px solid rgba(34,197,94,0.75)!important;}
.cal-cell.skipped-cell{background:rgba(251,191,36,0.12);border-color:rgba(251,191,36,0.28);}
.cal-cell.today-cell{background:rgba(229,9,20,0.40)!important;border:2.5px solid #E50914!important;}
.cal-cell.past-cell{opacity:0.55;}
.cal-num{font-size:0.80rem;font-weight:800;color:#fff;}
.cal-dot{width:5px;height:5px;border-radius:50%;margin-top:2px;}
.d-done{background:#E50914;}.d-skipped{background:#fbbf24;}.d-today{background:rgba(229,9,20,0.70);}.d-pending{background:rgba(255,255,255,0.15);}
.prof-card{background:rgba(8,3,1,0.90);border:2px solid rgba(229,9,20,0.50);border-radius:14px;padding:18px;margin-bottom:12px;backdrop-filter:blur(28px) saturate(1.5)!important;}
.prof-avatar{width:44px;height:44px;border-radius:10px;background:rgba(229,9,20,0.18);border:2px solid rgba(229,9,20,0.50);display:flex;align-items:center;justify-content:center;font-size:1.3rem;}
.prof-name{font-family:'Barlow Condensed',sans-serif;font-size:1.2rem;font-weight:700;text-transform:uppercase;color:#fff;letter-spacing:1px;}
.prof-sub{font-size:0.85rem;color:rgba(229,9,20,0.70);font-weight:600;}
.db-stat-card{background:rgba(8,3,1,0.88);border:2px solid rgba(229,9,20,0.48);border-radius:10px;padding:12px 14px;margin-bottom:8px;backdrop-filter:blur(24px)!important;}
.db-stat-lbl{font-size:0.85rem;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;color:rgba(255,255,255,0.90);margin-bottom:6px;}
html,body,.stApp,.stMarkdown,p,div,span,label{text-shadow:0 2px 6px rgba(0,0,0,0.98)!important;}
[data-testid="stWidgetLabel"],[data-testid="stWidgetLabel"] p{color:#fff!important;font-size:1.05rem!important;font-weight:700!important;}
.stMarkdown p,.stMarkdown li{color:#fff!important;font-size:1.05rem!important;line-height:1.75!important;}
</style>
""", unsafe_allow_html=True)

# ── NAV ───────────────────────────────────────────────────────────────────────
try:
    from nav_component import render_nav
    render_nav("dashboard", uname)
except Exception as _nav_err:
    st.warning(f"Nav error: {_nav_err}")

# ── AUTO-REDIRECT ─────────────────────────────────────────────────────────────
if st.session_state.get("force_regen") and not st.session_state.get("structured_days"):
    st.switch_page("pages/3_Workout_Plan.py")

# ── STAT MINI CARDS ───────────────────────────────────────────────────────────
fire_cls = "stat-mini fire" if streak >= 3 else "stat-mini"
st.markdown(f"""
<div class='stat-mini-grid'>
  <div class='{fire_cls}'><div class='stat-mini-icon'>🔥</div>
    <div class='stat-mini-val red'>{streak}</div><div class='stat-mini-lbl'>Day Streak</div></div>
  <div class='stat-mini'><div class='stat-mini-icon'>✅</div>
    <div class='stat-mini-val'>{done_count}</div><div class='stat-mini-lbl'>Completed</div></div>
  <div class='stat-mini'><div class='stat-mini-icon'>📊</div>
    <div class='stat-mini-val'>{pct}%</div><div class='stat-mini-lbl'>Progress</div></div>
  <div class='stat-mini'><div class='stat-mini-icon'>📅</div>
    <div class='stat-mini-val'>{plan_duration}</div><div class='stat-mini-lbl'>Total Days</div></div>
</div>
""", unsafe_allow_html=True)

# ── ACHIEVEMENTS ──────────────────────────────────────────────────────────────
try:
    from utils.achievements import compute_stats, get_earned_badges, get_next_badge, render_badges_html
    _stats  = compute_stats(uname, st.session_state)
    _earned = get_earned_badges(_stats)
    _next   = get_next_badge(_stats)
    if _earned or _next:
        _badge_html = (
            "<div style='background:rgba(229,9,20,0.08);border:1.5px solid rgba(229,9,20,0.22);"
            "border-radius:14px;padding:12px 18px;margin-bottom:18px;"
            "display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px'>"
            "<div style='display:flex;align-items:center;gap:12px;flex-wrap:wrap'>"
            "<div style='font-size:0.85rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;"
            "color:rgba(229,9,20,0.80);white-space:nowrap'>&#127942; " + str(len(_earned)) + " BADGES</div>"
            + render_badges_html(_earned, compact=True) + "</div>"
        )
        if _next:
            _badge_html += (
                "<div style='font-size:0.85rem;color:rgba(255,255,255,0.90);white-space:nowrap'>"
                "Next: <b style='color:#fbbf24'>" + _next["icon"] + " " + _next["title"] + "</b></div>"
            )
        _badge_html += "</div>"
        st.markdown(_badge_html, unsafe_allow_html=True)
        if "last_badge_count" not in st.session_state:
            st.session_state.last_badge_count = len(_earned)
        elif len(_earned) > st.session_state.last_badge_count:
            for _nb in _earned[st.session_state.last_badge_count:]:
                st.toast(f"{_nb['icon']} Badge Unlocked: {_nb['title']}!", icon="🏆")
            st.session_state.last_badge_count = len(_earned)
except Exception:
    pass

# ── BMI ───────────────────────────────────────────────────────────────────────
from prompt_builder import calculate_bmi, bmi_category
bmi_val = calculate_bmi(data["weight"], data["height"])
bmi_cat = bmi_category(bmi_val)

# ── TODAY HERO BAR ─────────────────────────────────────────────────────────────
chip_cls  = {"done":"done","skipped":"skipped","pending":"pending"}[today_status]
chip_text = {"done":"✅ Completed","skipped":"⏭️ Skipped","pending":"⚡ Not Done Yet"}[today_status]
st.markdown(f"""
<div style='background:linear-gradient(135deg,rgba(10,6,4,0.85),rgba(229,9,20,0.08) 60%,rgba(10,6,4,0.90));
  border:1.5px solid rgba(229,9,20,0.28);border-radius:18px;padding:22px 28px;margin-bottom:18px;
  position:relative;overflow:hidden;backdrop-filter:blur(14px)'>
  <div style='position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,#E50914 40%,transparent)'></div>
  <div style='display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:14px'>
    <div>
      <div style='font-size:0.85rem;font-weight:700;letter-spacing:4px;text-transform:uppercase;color:rgba(229,9,20,0.75);margin-bottom:6px'>📅 {date.today().strftime('%A, %B %d')}</div>
      <div style='font-family:Bebas Neue,sans-serif;font-size:clamp(1.6rem,3vw,2.4rem);color:#fff;letter-spacing:2px;line-height:1'>{today_title}</div>
    </div>
    <div style='display:flex;gap:12px;flex-wrap:wrap;align-items:center'>
      <span class='status-chip {chip_cls}'>{chip_text}</span>
      <div style='background:rgba(229,9,20,0.12);border:1px solid rgba(229,9,20,0.28);border-radius:20px;padding:5px 14px;font-size:0.85rem;font-weight:700;color:#E50914'>
        Day {today_entry["day_idx"]+1} / {plan_duration}</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── 3-COLUMN LAYOUT ──────────────────────────────────────────────────────────
col_left, col_mid, col_right = st.columns([5, 4, 3], gap="medium")

with col_left:
    st.markdown("<div class='sec-lbl'>Today's Exercises</div>", unsafe_allow_html=True)
    if today_exercises:
        ex_html = ""
        for ex in today_exercises[:8]:
            badges = f"<span class='ex-badge sets'>{ex['sets']}×{ex['reps']}</span>"
            if ex["rest"]: badges += f"<span class='ex-badge rest'>{ex['rest']}</span>"
            ex_html += (f"<div class='ex-item'><div class='ex-ico'>{ex['icon']}</div>"
                        f"<div class='ex-nm'>{ex['name']}</div><div class='ex-badges'>{badges}</div></div>")
        if len(today_exercises) > 8:
            ex_html += f"<div style='font-size:0.85rem;color:rgba(255,255,255,0.90);padding:6px 0 2px'>+{len(today_exercises)-8} more exercises</div>"
        st.markdown(f"<div class='g-panel' style='padding:16px 18px'><div class='ex-list'>{ex_html}</div></div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='g-panel' style='text-align:center;padding:32px 20px'>"
                    "<div style='font-size:2rem;margin-bottom:8px'>😴</div>"
                    "<div style='font-size:1.05rem;color:rgba(255,255,255,0.90)'>Rest Day — Recovery is progress too!</div>"
                    "</div>", unsafe_allow_html=True)

    if today_status == "pending":
        ba, bb = st.columns(2)
        with ba:
            st.markdown("<div class='done-btn'>", unsafe_allow_html=True)
            if st.button("✅ Mark Complete", use_container_width=True, key="mc"):
                tracking[date.today().isoformat()] = {"day_idx": today_entry["day_idx"], "status": "done"}
                st.session_state.tracking = tracking
                try:
                    from utils.db import save_streak, get_streak as _gs
                    _sd3 = _gs(uname)
                    _sd3["current_streak"]      = _sd3.get("current_streak",0) + 1
                    _sd3["longest_streak"]       = max(_sd3.get("longest_streak",0), _sd3["current_streak"])
                    _sd3["last_completed_date"]  = today_str
                    _sd3["username"]             = uname
                    save_streak(_sd3)
                    st.session_state._db_streak  = _sd3["current_streak"]
                    st.toast("🔥 Workout complete! Streak: " + str(_sd3["current_streak"]) + " days!", icon="💪")
                except Exception: pass
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        with bb:
            if st.button("⏭️ Skip Today", use_container_width=True, key="sk"):
                tracking[date.today().isoformat()] = {"day_idx": today_entry["day_idx"], "status": "skipped"}
                st.session_state.tracking = tracking; st.rerun()
    else:
        undo_col, plan_col = st.columns(2)
        with undo_col:
            if st.button("↩️ Undo", use_container_width=True, key="undo"):
                tracking.pop(date.today().isoformat(), None); st.session_state.tracking = tracking; st.rerun()
        with plan_col:
            st.markdown("<div class='plan-btn'>", unsafe_allow_html=True)
            if st.button("📋 Full Plan", use_container_width=True, key="fp2"):
                try: st.switch_page("pages/3_Workout_Plan.py")
                except Exception as _e: st.error(f"Navigation error: {_e}")
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='g-panel' style='padding:16px 18px'>
      <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:8px'>
        <span style='font-size:0.85rem;color:rgba(255,255,255,0.90)'>Plan Progress</span>
        <span style='font-family:Bebas Neue,sans-serif;font-size:1.6rem;color:#E50914;letter-spacing:1px;line-height:1'>{pct}%</span>
      </div>
      <div class='prog-bg'><div class='prog-fill' style='width:{pct}%'></div></div>
      <div style='display:flex;justify-content:space-between;margin-top:6px'>
        <span style='font-size:0.85rem;color:rgba(255,255,255,0.90)'>{done_count} done</span>
        <span style='font-size:0.85rem;color:rgba(255,255,255,0.90)'>{plan_duration - done_count} remaining</span>
      </div>
    </div>""", unsafe_allow_html=True)

    import random as _random
    _quotes = [
        ("The pain you feel today is the strength you feel tomorrow.", "Unknown"),
        ("No matter how slow you go, you are still lapping everyone on the couch.", "Unknown"),
        ("Your body can stand almost anything. It is your mind you have to convince.", "Unknown"),
        ("Success is not always about greatness. It is about consistency.", "Dwayne Johnson"),
        ("Train hard, turn up, run your best and the rest will take care of itself.", "Usain Bolt"),
        ("The only bad workout is the one that did not happen.", "Unknown"),
        ("Strength does not come from the body. It comes from the will of the soul.", "Gandhi"),
    ]
    _q, _a = _quotes[(done_count + streak) % len(_quotes)]
    st.markdown(
        f"<div style='background:rgba(229,9,20,0.06);border-left:3px solid rgba(229,9,20,0.55);"
        f"border-radius:0 12px 12px 0;padding:14px 18px;margin-top:4px'>"
        f"<div style='font-size:0.80rem;color:rgba(255,255,255,0.90);line-height:1.65;font-style:italic;margin-bottom:6px'>&ldquo;{_q}&rdquo;</div>"
        f"<div style='font-size:0.85rem;font-weight:700;color:rgba(229,9,20,0.65);letter-spacing:1px;text-transform:uppercase'>— {_a}</div>"
        f"</div>", unsafe_allow_html=True)

with col_mid:
    st.markdown("<div class='sec-lbl'>This Week</div>", unsafe_allow_html=True)
    week_done = sum(1 for w in week_data if w["done"])
    max_bar_h = 72
    bars_html = ""
    for wd in week_data:
        if wd["done"]:       cls = "done";    h = max_bar_h
        elif wd["skipped"]:  cls = "skipped"; h = int(max_bar_h*0.45)
        else:                cls = "pending"; h = int(max_bar_h*0.12)
        bars_html += (f"<div class='act-bar-wrap'><div class='act-bar {cls}' style='height:{h}px'></div>"
                      f"<div class='act-day'>{wd['day']}</div></div>")
    _dpw = int(data.get("days_per_week", 7))
    week_pct = int(week_done/max(_dpw,1)*100)
    week_msg = ("🔥 Perfect week!" if week_done==7 else "💪 Almost there!" if week_done>=5
                else "⚡ Keep pushing!" if week_done>=3 else "🚀 Get started!")
    st.markdown(f"""
    <div class='g-panel' style='padding:16px 18px'>
      <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:10px'>
        <div style='font-size:1.05rem;color:rgba(255,255,255,0.90)'>{week_msg}</div>
        <div style='font-family:Bebas Neue,sans-serif;font-size:1.8rem;color:#E50914;line-height:1'>
          {week_done}<span style='font-size:0.9rem;color:rgba(255,255,255,0.90)'>/7</span></div>
      </div>
      <div class='act-grid'>{bars_html}</div>
      <div style='height:4px;background:rgba(255,255,255,0.06);border-radius:2px;overflow:hidden;margin-top:10px'>
        <div style='height:100%;width:{week_pct}%;background:linear-gradient(90deg,#E50914,#ff5555);border-radius:2px'></div>
      </div>
    </div>""", unsafe_allow_html=True)

    _days_left = max(0, plan_duration - done_count)
    st.markdown(
        f"<div style='display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-bottom:14px'>"
        f"<div style='background:rgba(229,9,20,0.10);border:1.5px solid rgba(229,9,20,0.25);border-radius:12px;padding:12px 8px;text-align:center'>"
        f"<div style='font-family:Bebas Neue,sans-serif;font-size:1.6rem;color:#E50914'>{done_count}</div>"
        f"<div style='font-size:0.85rem;color:rgba(255,255,255,0.90);letter-spacing:1.5px;text-transform:uppercase'>Done</div></div>"
        f"<div style='background:rgba(251,191,36,0.08);border:1.5px solid rgba(251,191,36,0.22);border-radius:12px;padding:12px 8px;text-align:center'>"
        f"<div style='font-family:Bebas Neue,sans-serif;font-size:1.6rem;color:#fbbf24'>{skipped_count}</div>"
        f"<div style='font-size:0.85rem;color:rgba(255,255,255,0.90);letter-spacing:1.5px;text-transform:uppercase'>Skipped</div></div>"
        f"<div style='background:rgba(96,165,250,0.08);border:1.5px solid rgba(96,165,250,0.22);border-radius:12px;padding:12px 8px;text-align:center'>"
        f"<div style='font-family:Bebas Neue,sans-serif;font-size:1.6rem;color:#60a5fa'>{_days_left}</div>"
        f"<div style='font-size:0.85rem;color:rgba(255,255,255,0.90);letter-spacing:1.5px;text-transform:uppercase'>Left</div></div>"
        f"</div>", unsafe_allow_html=True)

    st.markdown("<div class='sec-lbl'>Weight Log</div>", unsafe_allow_html=True)
    _wlog_key = f"wlog_loaded_{uname}"
    if not st.session_state.get(_wlog_key):
        try:
            from utils.db import get_weight_log as _gwl
            st.session_state["_wlog_history"] = _gwl(uname, limit=30)
            st.session_state[_wlog_key] = True
        except Exception:
            st.session_state["_wlog_history"] = []; st.session_state[_wlog_key] = True
    _wlog = st.session_state.get("_wlog_history",[])
    _cw   = float(data.get("weight",70))
    _new_w = st.number_input("Today's weight (kg)", min_value=30.0, max_value=250.0,
                              value=_cw, step=0.1, format="%.1f", key="wlog_input_dash")
    if st.button("📈 Log Weight", use_container_width=True, key="wlog_save"):
        try:
            from utils.db import save_weight_log as _swl, get_weight_log as _gwl2
            _swl(uname, today_str, _new_w)
            st.session_state["_wlog_history"] = _gwl2(uname, limit=30)
            st.session_state.pop(_wlog_key, None)
            st.toast(f"⚖️ Weight {_new_w}kg logged!", icon="📈"); st.rerun()
        except Exception as _we: st.error(str(_we))

    if _wlog and len(_wlog) >= 2:
        _dates   = [e["date"][-5:] for e in _wlog]
        _weights = [e["weight_kg"] for e in _wlog]
        _min_w, _max_w = min(_weights)-1, max(_weights)+1
        _delta   = _weights[-1] - _weights[0]
        _dcol    = "#22c55e" if _delta <= 0 else "#ef4444"
        _dsym    = "▼" if _delta <= 0 else "▲"
        _N       = len(_weights)
        _pts  = " ".join(f"{int(i*(180/max(_N-1,1)))},{int(((_max_w-w)/(_max_w-_min_w))*80)}" for i,w in enumerate(_weights))
        _dots = "".join(f'<circle cx="{int(i*(180/max(_N-1,1)))}" cy="{int(((_max_w-w)/(_max_w-_min_w))*80)}" r="3" fill="#E50914"/>' for i,w in enumerate(_weights))
        st.markdown(f"""
<div style='background:rgba(10,6,4,0.88);border:1px solid rgba(229,9,20,0.18);border-radius:12px;padding:12px 14px;margin-top:8px'>
  <div style='display:flex;justify-content:space-between;margin-bottom:8px'>
    <span style='font-size:0.85rem;color:rgba(255,255,255,0.90);letter-spacing:2px;text-transform:uppercase'>Weight History</span>
    <span style='font-size:1.05rem;font-weight:700;color:{_dcol}'>{_dsym} {abs(_delta):.1f} kg</span>
  </div>
  <svg viewBox="0 0 200 100" style="width:100%">
    <polyline points="{_pts}" fill="none" stroke="#E50914" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    {_dots}
    <text x="0" y="95" fill="rgba(255,255,255,0.90)" font-size="7">{_dates[0]}</text>
    <text x="180" y="95" fill="rgba(255,255,255,0.90)" font-size="7" text-anchor="end">{_dates[-1]}</text>
  </svg>
</div>""", unsafe_allow_html=True)

    missed = [cd for cd in calendar_days if cd["date"] < date.today() and cd["status"] == "pending"]
    if missed:
        st.markdown("<div class='sec-lbl' style='margin-top:14px'>Missed — Log Anyway</div>", unsafe_allow_html=True)
        for cd in missed[:3]:
            _sd_m = _sdays[cd["day_idx"]] if _sdays and cd["day_idx"] < len(_sdays) else None
            _mg_m = _sd_m.get("muscle_group","Workout") if _sd_m else "Workout"
            _days_ago = (date.today() - cd["date"]).days
            m1, m2, m3 = st.columns([4,1,1])
            with m1:
                st.markdown(f"<div style='font-size:1.05rem;color:rgba(255,255,255,0.90);padding:7px 0;display:flex;align-items:center;gap:8px'>"
                            f"<span style='font-size:0.85rem;color:rgba(239,68,68,0.70);font-weight:700'>{_days_ago}d ago</span>"
                            f"<span style='color:#fff;font-weight:600'>{_mg_m[:18]}</span></div>", unsafe_allow_html=True)
            with m2:
                if st.button("✅", key=f"mc_{cd['date'].isoformat()}", use_container_width=True):
                    tracking[cd["date"].isoformat()] = {"day_idx":cd["day_idx"],"status":"done"}
                    st.session_state.tracking = tracking; st.toast(f"✅ {_mg_m} logged!", icon="💪"); st.rerun()
            with m3:
                if st.button("⏭️", key=f"ms_{cd['date'].isoformat()}", use_container_width=True):
                    tracking[cd["date"].isoformat()] = {"day_idx":cd["day_idx"],"status":"skipped"}
                    st.session_state.tracking = tracking; st.rerun()

with col_right:
    st.markdown(f"""
    <div class='prof-card'>
      <div style='display:flex;align-items:center;gap:12px;margin-bottom:14px'>
        <div class='prof-avatar'>💪</div>
        <div><div class='prof-name'>{uname}</div><div class='prof-sub'>{data.get("goal","Fitness")}</div></div>
      </div>
      <div style='display:grid;grid-template-columns:1fr 1fr;gap:8px'>
        <div class='db-stat-card'><div class='db-stat-lbl'>Weight</div>
          <div style='font-family:Bebas Neue,sans-serif;font-size:1.4rem;color:#fff'>{data.get("weight","–")} kg</div></div>
        <div class='db-stat-card'><div class='db-stat-lbl'>Height</div>
          <div style='font-family:Bebas Neue,sans-serif;font-size:1.4rem;color:#fff'>{data.get("height","–")} cm</div></div>
        <div class='db-stat-card'><div class='db-stat-lbl'>Age</div>
          <div style='font-family:Bebas Neue,sans-serif;font-size:1.4rem;color:#fff'>{data.get("age","–")} yrs</div></div>
        <div class='db-stat-card' style='border-color:rgba(229,9,20,0.22)'><div class='db-stat-lbl'>BMI</div>
          <div style='font-family:Bebas Neue,sans-serif;font-size:1.4rem;color:#E50914'>{bmi_val:.1f}</div></div>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<div class='sec-lbl'>Workout Calendar</div>", unsafe_allow_html=True)
    _plan_end_date = plan_start + timedelta(days=plan_duration - 1)
    _same_month    = plan_start.month == _plan_end_date.month and plan_start.year == _plan_end_date.year
    month_label    = plan_start.strftime("%B %Y") if _same_month else plan_start.strftime("%b %Y") + " – " + _plan_end_date.strftime("%b %Y")
    st.markdown(
        f"<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:10px'>"
        f"<span style='font-size:0.80rem;font-weight:700;color:rgba(255,255,255,0.90)'>{month_label}</span>"
        f"<span style='font-size:0.85rem;color:rgba(255,255,255,0.90);letter-spacing:1px'>{done_count} done &middot; {skipped_count} skipped</span></div>",
        unsafe_allow_html=True)
    DOWS = ["MON","TUE","WED","THU","FRI","SAT","SUN"]
    st.markdown("<div class='cal-hdr-row'>"+"".join(f"<div class='cal-dow'>{d}</div>" for d in DOWS)+"</div>", unsafe_allow_html=True)
    _first_day  = plan_start
    _pad        = _first_day.weekday()
    _cal_cells  = [None] * _pad + calendar_days
    while len(_cal_cells) % 7 != 0: _cal_cells.append(None)
    for _wk_start in range(0, len(_cal_cells), 7):
        week_cells = _cal_cells[_wk_start:_wk_start+7]
        html = "<div class='cal-grid-7'>"
        for cd in week_cells:
            if cd is None:
                html += "<div class='cal-cell' style='opacity:0;pointer-events:none'><div class='cal-num'></div><div class='cal-dot d-pending' style='opacity:0'></div></div>"
                continue
            d = cd["date"]; st_ = cd["status"]
            is_today = d == date.today(); is_past = d < date.today()
            cell_cls = "cal-cell"
            if st_ == "done":      cell_cls += " done-cell"
            elif st_ == "skipped": cell_cls += " skipped-cell"
            elif is_today:         cell_cls += " today-cell"
            elif is_past:          cell_cls += " past-cell"
            dot_cls = "cal-dot " + ("d-done" if st_=="done" else "d-skipped" if st_=="skipped" else "d-today" if is_today else "d-pending")
            html += f"<div class='{cell_cls}'><div class='cal-num'>{d.day}</div><div class='{dot_cls}'></div></div>"
        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)

# ── ROW 3 ─────────────────────────────────────────────────────────────────────
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
row3_left, row3_right = st.columns([7, 5], gap="medium")

with row3_left:
    st.markdown("<div class='sec-lbl'>Up Next</div>", unsafe_allow_html=True)
    W_ICONS = ["🏋️","💪","🏃","🥊","🧗","🚴","🤸","⚡","🔥","🎯","⚡","💥"]
    MUSCLE_COLORS = {"chest":"#E50914","back":"#3b82f6","legs":"#22c55e","shoulders":"#f97316",
                     "arms":"#a855f7","core":"#fbbf24","cardio":"#06b6d4","full":"#E50914",
                     "rest":"#64748b","push":"#E50914","pull":"#3b82f6","lower":"#22c55e"}
    upcoming = [cd for cd in calendar_days if cd["date"] >= date.today() and cd["status"] == "pending"]
    if upcoming:
        _up_pairs = [upcoming[i:i+2] for i in range(0, min(len(upcoming), 6), 2)]
        for pair in _up_pairs:
            up_c1, up_c2 = st.columns(2, gap="small")
            for _col_widget, cd in zip([up_c1, up_c2], pair):
                with _col_widget:
                    _si    = _sdays[cd["day_idx"]] if _sdays and cd["day_idx"] < len(_sdays) else None
                    _mg2   = _si.get("muscle_group","Workout") if _si else f"Day {cd['day_idx']+1}"
                    _ex_ct = len(_si.get("workout",[])) if _si else 0
                    _ico   = W_ICONS[cd["day_idx"] % len(W_ICONS)]
                    _da    = (cd["date"] - date.today()).days
                    _dl    = "Today" if _da==0 else ("Tomorrow" if _da==1 else cd["date"].strftime("%b %d"))
                    _rest  = _si.get("is_rest_day",False) if _si else False
                    _accent = "#64748b" if _rest else next((v for k,v in MUSCLE_COLORS.items() if k in _mg2.lower()), "#E50914")
                    _sub_txt   = "Recovery 😴" if _rest else f"{_ex_ct} exercises"
                    _title_txt = "Rest & Recovery" if _rest else _mg2
                    _date_style = f"color:#E50914;background:rgba(229,9,20,0.15);border:1px solid rgba(229,9,20,0.35);border-radius:5px;padding:1px 7px;" if _da==0 else "color:rgba(229,9,20,0.75);"
                    st.markdown(
                        f"<div style='background:rgba(10,6,4,0.75);border:1.5px solid {_accent}33;"
                        f"border-left:4px solid {_accent};border-radius:12px;padding:12px 14px;margin-bottom:8px;backdrop-filter:blur(10px)'>"
                        f"<div style='display:flex;align-items:center;justify-content:space-between;margin-bottom:6px'>"
                        f"<div style='display:flex;align-items:center;gap:8px'>"
                        f"<div style='width:32px;height:32px;border-radius:8px;background:{_accent}22;border:1px solid {_accent}44;display:flex;align-items:center;justify-content:center;font-size:1.1rem'>{_ico}</div>"
                        f"<div><div style='font-size:0.85rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:{_accent};margin-bottom:2px'>{_mg2.split()[0].upper()[:8] if not _rest else 'REST'}</div>"
                        f"<div style='font-size:1.00rem;font-weight:700;color:#fff;line-height:1.2'>{_title_txt[:20]}</div></div></div>"
                        f"<div style='text-align:right'><div style='font-size:0.85rem;font-weight:700;{_date_style}'>{_dl}</div>"
                        f"<div style='font-size:0.85rem;color:rgba(255,255,255,0.90);margin-top:2px'>Day {cd['day_idx']+1}</div></div></div>"
                        f"<div style='font-size:0.85rem;color:rgba(255,255,255,0.90)'>{_sub_txt}</div></div>",
                        unsafe_allow_html=True)
    else:
        st.markdown("<div style='background:rgba(34,197,94,0.08);border:1.5px solid rgba(34,197,94,0.25);border-radius:14px;padding:24px;text-align:center'>"
                    "<div style='font-size:2rem;margin-bottom:8px'>🎉</div>"
                    "<div style='font-size:1.05rem;font-weight:700;color:#4ade80'>All workouts complete!</div>"
                    "<div style='font-size:0.85rem;color:rgba(255,255,255,0.90);margin-top:4px'>You crushed this plan!</div></div>", unsafe_allow_html=True)

with row3_right:
    st.markdown("<div class='sec-lbl'>Quick Access</div>", unsafe_allow_html=True)
    _nav_items = [
        ("✏️", "Edit Profile",  "Update your goals & details", "pages/1_Profile.py",        "ep"),
        ("🏆", "Records",       "PRs, measurements & 1RM",     "pages/6_records.py",        "db_rec"),
        ("🤖", "AI Coach",      "Chat with your fitness coach","pages/5_ai_coach.py",       "db_ai2"),
        ("📅", "History",       "Past workouts timeline",      "pages/9_history.py",        "go_history"),
        ("🥗", "Diet Plan",     "Today's meals & nutrition",    "pages/4_Diet_Plan.py",      "go_diet"),
        ("📸", "Photos",        "Track your transformation",   "pages/7_progress_photos.py","go_photos"),
    ]
    for _ni_row in [_nav_items[:3], _nav_items[3:]]:
        _nc = st.columns(3, gap="small")
        for _col_w, (_ico, _lbl, _desc, _path, _key) in zip(_nc, _ni_row):
            with _col_w:
                st.markdown(
                    f"<div style='background:rgba(10,6,4,0.75);border:1.5px solid rgba(229,9,20,0.22);"
                    f"border-radius:12px;padding:14px 10px;text-align:center;backdrop-filter:blur(10px);margin-bottom:8px'>"
                    f"<div style='font-size:1.6rem;margin-bottom:6px'>{_ico}</div>"
                    f"<div style='font-size:0.85rem;font-weight:700;color:#fff;letter-spacing:0.3px'>{_lbl}</div>"
                    f"<div style='font-size:0.85rem;color:rgba(255,255,255,0.90);margin-top:3px;line-height:1.3'>{_desc}</div>"
                    f"</div>", unsafe_allow_html=True)
                if st.button(_lbl, key=_key, use_container_width=True):
                    try: st.switch_page(_path)
                    except Exception: pass
    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='plan-btn'>", unsafe_allow_html=True)
    if st.button("⚡  View Full Workout Plan", key="vfp", use_container_width=True):
        try: st.switch_page("pages/3_Workout_Plan.py")
        except Exception: pass
    st.markdown("</div>", unsafe_allow_html=True)

# CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow+Condensed:wght@700;800;900&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700&display=swap');
#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stDecoration"],
[data-testid="stSidebarNav"],section[data-testid="stSidebar"]{display:none!important;}
html,body,.stApp{background:#050202!important;color:#fff!important;font-family:'DM Sans',sans-serif!important;}
[data-testid="stAppViewContainer"]::before{
  content:'';position:fixed;inset:0;z-index:0;
  background:url('https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=1800&q=80&auto=format&fit=crop')
    center center/cover no-repeat;
  filter:blur(8px) brightness(0.25) saturate(0.55);
  transform:scale(1.06);}
[data-testid="stAppViewContainer"]{
  background:linear-gradient(160deg,rgba(3,1,0,0.88) 0%,rgba(5,2,0,0.78) 40%,rgba(3,1,0,0.92) 100%)!important;
  position:relative;}
[data-testid="stAppViewContainer"]>section>div.block-container{
  max-width:1200px!important;margin:0 auto!important;padding:0 24px 80px!important;position:relative;z-index:2;}
[data-testid="stWidgetLabel"],[data-testid="stWidgetLabel"] p{color:rgba(255,255,255,0.75)!important;font-size:1.05rem!important;font-weight:600!important;}
.stNumberInput>div>div>input,.stTextInput>div>div>input,.stTextArea>div>div>textarea{
  background:rgba(255,255,255,0.08)!important;border:1.5px solid rgba(255,255,255,0.20)!important;
  color:#fff!important;border-radius:14px!important;backdrop-filter:blur(28px)!important;font-size:1.05rem!important;}
[data-baseweb="select"]>div{background:rgba(255,255,255,0.08)!important;border:1.5px solid rgba(255,255,255,0.20)!important;
  border-radius:14px!important;backdrop-filter:blur(28px)!important;color:#fff!important;}
[data-baseweb="popover"] [role="option"]{background:rgba(12,6,4,0.97)!important;color:#fff!important;}
[data-baseweb="popover"] [role="option"]:hover{background:rgba(229,9,20,0.22)!important;}
.stButton>button{background:linear-gradient(135deg,rgba(229,9,20,0.85),rgba(160,0,10,0.90))!important;
  border:2px solid rgba(229,9,20,0.65)!important;color:#fff!important;border-radius:10px!important;
  font-family:'DM Sans',sans-serif!important;font-size:1.0rem!important;font-weight:700!important;
  box-shadow:0 0 12px rgba(229,9,20,0.30)!important;transition:all 0.20s!important;}
.stButton>button:hover{transform:translateY(-2px)!important;box-shadow:0 0 24px rgba(229,9,20,0.60)!important;}
.done-btn .stButton>button{background:linear-gradient(135deg,rgba(34,197,94,0.85),rgba(22,163,74,0.90))!important;
  border-color:rgba(34,197,94,0.55)!important;box-shadow:0 0 12px rgba(34,197,94,0.32)!important;}
.plan-btn .stButton>button{background:linear-gradient(135deg,#E50914,#c0000c)!important;
  animation:glow-r 2.4s ease-in-out infinite!important;}
@keyframes glow-r{0%,100%{box-shadow:0 0 14px rgba(229,9,20,0.45);}50%{box-shadow:0 0 30px rgba(229,9,20,0.75);}}
.stat-mini-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:20px;}
.stat-mini{background:rgba(10,3,1,0.88);border:2px solid rgba(229,9,20,0.50);
  border-radius:12px;padding:16px 12px;text-align:center;position:relative;overflow:hidden;
  backdrop-filter:blur(28px) saturate(1.5)!important;
  box-shadow:inset 0 1px 0 rgba(255,255,255,0.08),0 10px 36px rgba(0,0,0,0.70)!important;}
.stat-mini::before{content:'';position:absolute;top:0;left:0;right:0;height:1.5px;
  background:linear-gradient(90deg,transparent,rgba(229,9,20,0.45),transparent);}
.stat-mini.fire{border-color:rgba(229,9,20,0.45);background:rgba(229,9,20,0.10);}
.stat-mini-icon{font-size:1.4rem;margin-bottom:6px;}
.stat-mini-val{font-family:'Bebas Neue',sans-serif;font-size:2rem;color:#fff;letter-spacing:1px;line-height:1;}
.stat-mini-val.red{color:#E50914;}
.stat-mini-lbl{font-size:0.85rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.90);margin-top:4px;}
.sec-lbl{font-size:1.05rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;
  color:rgba(229,9,20,0.75);margin:20px 0 12px;display:flex;align-items:center;gap:8px;}
.sec-lbl::before{content:'';width:16px;height:1.5px;background:#E50914;border-radius:1px;}
.sec-lbl::after{content:'';flex:1;height:1px;background:linear-gradient(90deg,rgba(229,9,20,0.18),transparent);}
.g-panel{background:rgba(8,3,1,0.88);border:2px solid rgba(229,9,20,0.45);
  border-radius:14px;padding:20px 24px;margin-bottom:14px;position:relative;overflow:hidden;
  backdrop-filter:blur(32px) saturate(1.5)!important;
  box-shadow:inset 0 1px 0 rgba(255,255,255,0.10),0 12px 48px rgba(0,0,0,0.75)!important;}
.g-panel::before{content:'';position:absolute;top:0;left:0;right:0;height:1.5px;
  background:linear-gradient(90deg,transparent,rgba(229,9,20,0.40),transparent);}
.prog-bg{height:8px;background:rgba(255,255,255,0.08);border-radius:4px;overflow:hidden;}
.prog-fill{height:100%;background:linear-gradient(90deg,#E50914,#ff4444);border-radius:4px;}
.status-chip{display:inline-block;padding:3px 12px;border-radius:20px;font-size:0.85rem;font-weight:700;letter-spacing:1px;text-transform:uppercase;}
.status-chip.done{background:rgba(34,197,94,0.15);border:1px solid rgba(34,197,94,0.35);color:#4ade80;}
.status-chip.skipped{background:rgba(251,191,36,0.12);border:1px solid rgba(251,191,36,0.30);color:#fbbf24;}
.status-chip.pending{background:rgba(229,9,20,0.12);border:2px solid rgba(229,9,20,0.45);color:#ff6b6b;}
.ex-list{margin:10px 0;}
.ex-item{display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.05);}
.ex-item:last-child{border-bottom:none;}
.ex-ico{width:28px;height:28px;border-radius:6px;background:rgba(229,9,20,0.12);border:2px solid rgba(229,9,20,0.37);
  display:flex;align-items:center;justify-content:center;font-size:0.75rem;flex-shrink:0;}
.ex-nm{font-size:1.00rem;font-weight:600;color:#fff;flex:1;}
.ex-badges{display:flex;gap:4px;}
.ex-badge{font-size:0.85rem;font-weight:700;padding:2px 7px;border-radius:5px;}
.ex-badge.sets{background:rgba(100,160,255,0.13);color:#93c5fd;border:1px solid rgba(100,160,255,0.22);}
.ex-badge.reps{background:rgba(100,230,180,0.11);color:#6ee7b7;border:1px solid rgba(100,230,180,0.20);}
.ex-badge.rest{background:rgba(255,180,80,0.11);color:#fdba74;border:1px solid rgba(255,180,80,0.20);}
.act-grid{display:flex;gap:6px;align-items:flex-end;height:80px;margin:8px 0 4px;}
.act-bar-wrap{flex:1;display:flex;flex-direction:column;align-items:center;gap:4px;}
.act-bar{width:100%;border-radius:4px 4px 0 0;}
.act-bar.done{background:linear-gradient(180deg,#E50914,rgba(229,9,20,0.55));}
.act-bar.skipped{background:rgba(251,191,36,0.45);}
.act-bar.pending{background:rgba(255,255,255,0.08);}
.act-day{font-size:0.85rem;color:rgba(255,255,255,0.90);font-weight:600;}
.cal-hdr-row{display:grid;grid-template-columns:repeat(7,1fr);gap:3px;margin-bottom:4px;}
.cal-dow{font-size:0.85rem;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:rgba(255,255,255,0.90);text-align:center;padding:4px 0;}
.cal-grid-7{display:grid;grid-template-columns:repeat(7,1fr);gap:3px;margin-bottom:3px;}
.cal-cell{aspect-ratio:1;border-radius:6px;display:flex;flex-direction:column;align-items:center;
  justify-content:center;background:rgba(0,0,0,0.85);border:1.5px solid rgba(255,255,255,0.28);}
.cal-cell.done-cell{background:rgba(34,197,94,0.32)!important;border:2px solid rgba(34,197,94,0.75)!important;}
.cal-cell.skipped-cell{background:rgba(251,191,36,0.12);border-color:rgba(251,191,36,0.28);}
.cal-cell.today-cell{background:rgba(229,9,20,0.40)!important;border:2.5px solid #E50914!important;}
.cal-cell.past-cell{opacity:0.55;}
.cal-num{font-size:0.80rem;font-weight:800;color:#fff!important;}
.cal-dot{width:5px;height:5px;border-radius:50%;margin-top:2px;}
.d-done{background:#E50914;}.d-skipped{background:#fbbf24;}.d-today{background:rgba(229,9,20,0.70);}.d-pending{background:rgba(255,255,255,0.15);}
.prof-card{background:rgba(8,3,1,0.90);border:2px solid rgba(229,9,20,0.50);border-radius:14px;padding:18px;margin-bottom:12px;}
.prof-avatar{width:44px;height:44px;border-radius:10px;background:rgba(229,9,20,0.18);border:2px solid rgba(229,9,20,0.50);
  display:flex;align-items:center;justify-content:center;font-size:1.3rem;}
.prof-name{font-family:'Barlow Condensed',sans-serif;font-size:1.2rem;font-weight:700;text-transform:uppercase;color:#fff;letter-spacing:1px;}
.prof-sub{font-size:0.85rem;color:rgba(229,9,20,0.70);font-weight:600;}
.db-stat-card{background:rgba(8,3,1,0.88);border:2px solid rgba(229,9,20,0.48);border-radius:10px;padding:12px 14px;margin-bottom:8px;}
.db-stat-lbl{font-size:0.85rem;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;color:rgba(255,255,255,0.90);margin-bottom:6px;}
html,body,.stApp,.stMarkdown,p,div,span,label{text-shadow:0 2px 6px rgba(0,0,0,0.98)!important;}
[data-testid="stWidgetLabel"],[data-testid="stWidgetLabel"] p{color:#fff!important;font-weight:700!important;}
.stMarkdown p,.stMarkdown li{color:#fff!important;font-size:1.05rem!important;line-height:1.75!important;}
.act-day{color:#fff!important;font-weight:800!important;}
.cal-dow{color:rgba(255,255,255,0.95)!important;font-weight:800!important;}
@media(max-width:900px){.stat-mini-grid{grid-template-columns:repeat(2,1fr)!important;}}
</style>
""", unsafe_allow_html=True)

# ── NAV ───────────────────────────────────────────────────────────────────────
try:
    from nav_component import render_nav
    render_nav("dashboard", uname)
except Exception as _nav_err:
    st.warning(f"Nav error: {_nav_err}")

# ── Auto-redirect if force_regen set
if st.session_state.get("force_regen") and not st.session_state.get("structured_days"):
    st.switch_page("pages/3_Workout_Plan.py")

# ── STAT CARDS ────────────────────────────────────────────────────────────────
fire_cls = "stat-mini fire" if streak >= 3 else "stat-mini"
st.markdown(f"""
<div class='stat-mini-grid'>
  <div class='{fire_cls}'><div class='stat-mini-icon'>\U0001f525</div>
    <div class='stat-mini-val red'>{streak}</div><div class='stat-mini-lbl'>Day Streak</div></div>
  <div class='stat-mini'><div class='stat-mini-icon'>\u2705</div>
    <div class='stat-mini-val'>{done_count}</div><div class='stat-mini-lbl'>Completed</div></div>
  <div class='stat-mini'><div class='stat-mini-icon'>\U0001f4ca</div>
    <div class='stat-mini-val'>{pct}%</div><div class='stat-mini-lbl'>Progress</div></div>
  <div class='stat-mini'><div class='stat-mini-icon'>\U0001f4c5</div>
    <div class='stat-mini-val'>{plan_duration}</div><div class='stat-mini-lbl'>Total Days</div></div>
</div>
""", unsafe_allow_html=True)

# ── TODAY HERO ────────────────────────────────────────────────────────────────
chip_cls  = {"done":"done","skipped":"skipped","pending":"pending"}[today_status]
chip_text = {"done":"\u2705 Completed","skipped":"\u23ed\ufe0f Skipped","pending":"\u26a1 Not Done Yet"}[today_status]

st.markdown(f"""
<div style='background:linear-gradient(135deg,rgba(10,6,4,0.85),rgba(229,9,20,0.08) 60%,rgba(10,6,4,0.90));
  border:1.5px solid rgba(229,9,20,0.28);border-radius:18px;padding:22px 28px;margin-bottom:18px;
  position:relative;overflow:hidden;backdrop-filter:blur(14px)'>
  <div style='position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,#E50914 40%,transparent)'></div>
  <div style='display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:14px'>
    <div>
      <div style='font-size:0.85rem;font-weight:700;letter-spacing:4px;text-transform:uppercase;
        color:rgba(229,9,20,0.75);margin-bottom:6px'>\U0001f4c5 {date.today().strftime('%A, %B %d')}</div>
      <div style='font-family:Bebas Neue,sans-serif;font-size:clamp(1.6rem,3vw,2.4rem);
        color:#fff;letter-spacing:2px;line-height:1'>{today_title}</div>
    </div>
    <div style='display:flex;gap:12px;flex-wrap:wrap;align-items:center'>
      <span class='status-chip {chip_cls}'>{chip_text}</span>
      <div style='background:rgba(229,9,20,0.12);border:1px solid rgba(229,9,20,0.28);
        border-radius:20px;padding:5px 14px;font-size:0.85rem;font-weight:700;color:#E50914'>
        Day {today_entry["day_idx"]+1} / {plan_duration}</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── 3-COLUMN LAYOUT ───────────────────────────────────────────────────────────
col_left, col_mid, col_right = st.columns([5, 4, 3], gap="medium")

with col_left:
    st.markdown("<div class='sec-lbl'>Today's Exercises</div>", unsafe_allow_html=True)
    if today_exercises:
        ex_html = ""
        for ex in today_exercises[:8]:
            badges = ""
            if ex["sets"]: badges += f"<span class='ex-badge sets'>{ex['sets']}\xd7{ex['reps']}</span>"
            if ex["rest"]: badges += f"<span class='ex-badge rest'>{ex['rest']}</span>"
            ex_html += (f"<div class='ex-item'><div class='ex-ico'>{ex['icon']}</div>"
                        f"<div class='ex-nm'>{ex['name']}</div>"
                        f"<div class='ex-badges'>{badges}</div></div>")
        if len(today_exercises) > 8:
            ex_html += f"<div style='font-size:0.85rem;color:rgba(255,255,255,0.90);padding:6px 0 2px'>+{len(today_exercises)-8} more exercises</div>"
        st.markdown(f"<div class='g-panel' style='padding:16px 18px'><div class='ex-list'>{ex_html}</div></div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='g-panel' style='text-align:center;padding:32px 20px'>"
                    "<div style='font-size:2rem;margin-bottom:8px'>\U0001f634</div>"
                    "<div style='font-size:1.05rem;color:rgba(255,255,255,0.90)'>Rest Day \u2014 Recovery is progress too!</div>"
                    "</div>", unsafe_allow_html=True)

    if today_status == "pending":
        ba, bb = st.columns(2)
        with ba:
            st.markdown("<div class='done-btn'>", unsafe_allow_html=True)
            if st.button("\u2705 Mark Complete", use_container_width=True, key="mc"):
                tracking[date.today().isoformat()] = {"day_idx": today_entry["day_idx"], "status": "done"}
                st.session_state.tracking = tracking
                try:
                    from utils.db import save_streak, get_streak as _gs
                    _sd3 = _gs(uname)
                    _sd3["current_streak"]  = _sd3.get("current_streak",0) + 1
                    _sd3["longest_streak"]  = max(_sd3.get("longest_streak",0), _sd3["current_streak"])
                    _sd3["last_completed_date"] = today_str
                    _sd3["username"] = uname
                    save_streak(_sd3)
                    st.session_state._db_streak = _sd3["current_streak"]
                    st.toast("\U0001f525 Workout complete! Streak: " + str(_sd3["current_streak"]) + " days!", icon="\U0001f4aa")
                except Exception: pass
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        with bb:
            if st.button("\u23ed\ufe0f Skip Today", use_container_width=True, key="sk"):
                tracking[date.today().isoformat()] = {"day_idx": today_entry["day_idx"], "status": "skipped"}
                st.session_state.tracking = tracking
                st.rerun()
    else:
        undo_col, plan_col = st.columns(2)
        with undo_col:
            if st.button("\u21a9\ufe0f Undo", use_container_width=True, key="undo"):
                tracking.pop(date.today().isoformat(), None)
                st.session_state.tracking = tracking
                st.rerun()
        with plan_col:
            st.markdown("<div class='plan-btn'>", unsafe_allow_html=True)
            if st.button("\U0001f4cb Full Plan", use_container_width=True, key="fp2"):
                try: st.switch_page("pages/3_Workout_Plan.py")
                except Exception as _e: st.error(f"Navigation error: {_e}")
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='g-panel' style='padding:16px 18px'>
      <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:8px'>
        <span style='font-size:0.85rem;color:rgba(255,255,255,0.90)'>Plan Progress</span>
        <span style='font-family:Bebas Neue,sans-serif;font-size:1.6rem;color:#E50914;letter-spacing:1px;line-height:1'>{pct}%</span>
      </div>
      <div class='prog-bg'><div class='prog-fill' style='width:{pct}%'></div></div>
      <div style='display:flex;justify-content:space-between;margin-top:6px'>
        <span style='font-size:0.85rem;color:rgba(255,255,255,0.90)'>{done_count} done</span>
        <span style='font-size:0.85rem;color:rgba(255,255,255,0.90)'>{plan_duration - done_count} remaining</span>
      </div>
    </div>""", unsafe_allow_html=True)

    import random as _random
    _quotes = [
        ("The pain you feel today is the strength you feel tomorrow.", "Unknown"),
        ("No matter how slow you go, you are still lapping everyone on the couch.", "Unknown"),
        ("Your body can stand almost anything. It is your mind you have to convince.", "Unknown"),
        ("Success is not always about greatness. It is about consistency.", "Dwayne Johnson"),
        ("Train hard, turn up, run your best and the rest will take care of itself.", "Usain Bolt"),
        ("The only bad workout is the one that did not happen.", "Unknown"),
        ("Strength does not come from the body. It comes from the will of the soul.", "Gandhi"),
    ]
    _q, _a = _quotes[(done_count + streak) % len(_quotes)]
    st.markdown(
        f"<div style='background:rgba(229,9,20,0.06);border-left:3px solid rgba(229,9,20,0.55);"
        f"border-radius:0 12px 12px 0;padding:14px 18px;margin-top:4px'>"
        f"<div style='font-size:0.80rem;color:rgba(255,255,255,0.90);line-height:1.65;font-style:italic;margin-bottom:6px'>&ldquo;{_q}&rdquo;</div>"
        f"<div style='font-size:0.85rem;font-weight:700;color:rgba(229,9,20,0.65);letter-spacing:1px;text-transform:uppercase'>\u2014 {_a}</div>"
        f"</div>", unsafe_allow_html=True)

with col_mid:
    st.markdown("<div class='sec-lbl'>This Week</div>", unsafe_allow_html=True)
    week_done = sum(1 for w in week_data if w["done"])
    max_bar_h = 72
    bars_html = ""
    _dpw = int(data.get("days_per_week", 7))
    for wd in week_data:
        if wd["done"]:       cls = "done";    h = max_bar_h
        elif wd["skipped"]:  cls = "skipped"; h = int(max_bar_h*0.45)
        else:                cls = "pending"; h = int(max_bar_h*0.12)
        bars_html += (f"<div class='act-bar-wrap'>"
                      f"<div class='act-bar {cls}' style='height:{h}px'></div>"
                      f"<div class='act-day'>{wd['day']}</div></div>")
    week_pct = int(week_done/max(_dpw,1)*100)
    week_msg = ("\U0001f525 Perfect week!" if week_done==7 else "\U0001f4aa Almost there!" if week_done>=5
                else "\u26a1 Keep pushing!" if week_done>=3 else "\U0001f680 Get started!")
    st.markdown(f"""
    <div class='g-panel' style='padding:16px 18px'>
      <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:10px'>
        <div style='font-size:1.05rem;color:rgba(255,255,255,0.90)'>{week_msg}</div>
        <div style='font-family:Bebas Neue,sans-serif;font-size:1.8rem;color:#E50914;line-height:1'>
          {week_done}<span style='font-size:0.9rem;color:rgba(255,255,255,0.90)'>/7</span></div>
      </div>
      <div class='act-grid'>{bars_html}</div>
      <div style='height:4px;background:rgba(255,255,255,0.06);border-radius:2px;overflow:hidden;margin-top:10px'>
        <div style='height:100%;width:{week_pct}%;background:linear-gradient(90deg,#E50914,#ff5555);border-radius:2px'></div>
      </div>
    </div>""", unsafe_allow_html=True)

    _days_left = max(0, plan_duration - done_count)
    st.markdown(
        f"<div style='display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-bottom:14px'>"
        f"<div style='background:rgba(229,9,20,0.10);border:1.5px solid rgba(229,9,20,0.25);border-radius:12px;padding:12px 8px;text-align:center'>"
        f"<div style='font-family:Bebas Neue,sans-serif;font-size:1.6rem;color:#E50914'>{done_count}</div>"
        f"<div style='font-size:0.85rem;color:rgba(255,255,255,0.90);letter-spacing:1.5px;text-transform:uppercase'>Done</div></div>"
        f"<div style='background:rgba(251,191,36,0.08);border:1.5px solid rgba(251,191,36,0.22);border-radius:12px;padding:12px 8px;text-align:center'>"
        f"<div style='font-family:Bebas Neue,sans-serif;font-size:1.6rem;color:#fbbf24'>{skipped_count}</div>"
        f"<div style='font-size:0.85rem;color:rgba(255,255,255,0.90);letter-spacing:1.5px;text-transform:uppercase'>Skipped</div></div>"
        f"<div style='background:rgba(96,165,250,0.08);border:1.5px solid rgba(96,165,250,0.22);border-radius:12px;padding:12px 8px;text-align:center'>"
        f"<div style='font-family:Bebas Neue,sans-serif;font-size:1.6rem;color:#60a5fa'>{_days_left}</div>"
        f"<div style='font-size:0.85rem;color:rgba(255,255,255,0.90);letter-spacing:1.5px;text-transform:uppercase'>Left</div></div>"
        f"</div>", unsafe_allow_html=True)

    st.markdown("<div class='sec-lbl'>Weight Log</div>", unsafe_allow_html=True)
    _wlog_key = f"wlog_loaded_{uname}"
    if not st.session_state.get(_wlog_key):
        try:
            from utils.db import get_weight_log as _gwl
            st.session_state["_wlog_history"] = _gwl(uname, limit=30)
            st.session_state[_wlog_key] = True
        except Exception:
            st.session_state["_wlog_history"] = []
            st.session_state[_wlog_key] = True
    _wlog = st.session_state.get("_wlog_history",[])
    _cw   = float(data.get("weight",70))
    _new_w = st.number_input("Today's weight (kg)", min_value=30.0, max_value=250.0,
                              value=_cw, step=0.1, format="%.1f", key="wlog_input_dash")
    if st.button("\U0001f4c8 Log Weight", use_container_width=True, key="wlog_save"):
        try:
            from utils.db import save_weight_log as _swl, get_weight_log as _gwl2
            _swl(uname, today_str, _new_w)
            st.session_state["_wlog_history"] = _gwl2(uname, limit=30)
            st.session_state.pop(_wlog_key, None)
            st.toast(f"\u2696\ufe0f Weight {_new_w}kg logged!", icon="\U0001f4c8")
            st.rerun()
        except Exception as _we: st.error(str(_we))

    if _wlog and len(_wlog) >= 2:
        _dates   = [e["date"][-5:] for e in _wlog]
        _weights = [e["weight_kg"] for e in _wlog]
        _min_w, _max_w = min(_weights)-1, max(_weights)+1
        _delta   = _weights[-1] - _weights[0]
        _dcol    = "#22c55e" if _delta <= 0 else "#ef4444"
        _dsym    = "\u25bc" if _delta <= 0 else "\u25b2"
        _N       = len(_weights)
        _pts  = " ".join(f"{int(i*(180/max(_N-1,1)))},{int(((_max_w-w)/(_max_w-_min_w))*80)}" for i,w in enumerate(_weights))
        _dots = "".join(f'<circle cx="{int(i*(180/max(_N-1,1)))}" cy="{int(((_max_w-w)/(_max_w-_min_w))*80)}" r="3" fill="#E50914"/>' for i,w in enumerate(_weights))
        st.markdown(f"""
<div style='background:rgba(10,6,4,0.88);border:1px solid rgba(229,9,20,0.18);border-radius:12px;padding:12px 14px;margin-top:8px'>
  <div style='display:flex;justify-content:space-between;margin-bottom:8px'>
    <span style='font-size:0.85rem;color:rgba(255,255,255,0.90);letter-spacing:2px;text-transform:uppercase'>Weight History</span>
    <span style='font-size:1.05rem;font-weight:700;color:{_dcol}'>{_dsym} {abs(_delta):.1f} kg</span>
  </div>
  <svg viewBox="0 0 200 100" style="width:100%">
    <polyline points="{_pts}" fill="none" stroke="#E50914" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    {_dots}
    <text x="0" y="95" fill="rgba(255,255,255,0.90)" font-size="7">{_dates[0]}</text>
    <text x="180" y="95" fill="rgba(255,255,255,0.90)" font-size="7" text-anchor="end">{_dates[-1]}</text>
  </svg>
</div>""", unsafe_allow_html=True)

    missed = [cd for cd in calendar_days if cd["date"] < date.today() and cd["status"] == "pending"]
    if missed:
        st.markdown("<div class='sec-lbl' style='margin-top:14px'>Missed \u2014 Log Anyway</div>", unsafe_allow_html=True)
        for cd in missed[:3]:
            _sd_m = _sdays[cd["day_idx"]] if _sdays and cd["day_idx"] < len(_sdays) else None
            _mg_m = _sd_m.get("muscle_group","Workout") if _sd_m else "Workout"
            _days_ago = (date.today() - cd["date"]).days
            m1, m2, m3 = st.columns([4,1,1])
            with m1:
                st.markdown(f"<div style='font-size:1.05rem;color:rgba(255,255,255,0.90);padding:7px 0;display:flex;align-items:center;gap:8px'>"
                            f"<span style='font-size:0.85rem;color:rgba(239,68,68,0.70);font-weight:700'>{_days_ago}d ago</span>"
                            f"<span style='color:#fff;font-weight:600'>{_mg_m[:18]}</span></div>", unsafe_allow_html=True)
            with m2:
                if st.button("\u2705", key=f"mc_{cd['date'].isoformat()}", use_container_width=True):
                    tracking[cd["date"].isoformat()] = {"day_idx":cd["day_idx"],"status":"done"}
                    st.session_state.tracking = tracking
                    st.toast(f"\u2705 {_mg_m} logged!", icon="\U0001f4aa"); st.rerun()
            with m3:
                if st.button("\u23ed\ufe0f", key=f"ms_{cd['date'].isoformat()}", use_container_width=True):
                    tracking[cd["date"].isoformat()] = {"day_idx":cd["day_idx"],"status":"skipped"}
                    st.session_state.tracking = tracking; st.rerun()

with col_right:
    from prompt_builder import calculate_bmi, bmi_category
    bmi_val = calculate_bmi(data["weight"], data["height"])
    bmi_cat = bmi_category(bmi_val)
    st.markdown(f"""
    <div class='prof-card'>
      <div style='display:flex;align-items:center;gap:12px;margin-bottom:14px'>
        <div class='prof-avatar'>\U0001f4aa</div>
        <div>
          <div class='prof-name'>{uname}</div>
          <div class='prof-sub'>{data.get("goal","Fitness")}</div>
        </div>
      </div>
      <div style='display:grid;grid-template-columns:1fr 1fr;gap:8px'>
        <div class='db-stat-card'><div class='db-stat-lbl'>Weight</div>
          <div style='font-family:Bebas Neue,sans-serif;font-size:1.4rem;color:#fff'>{data.get("weight","\u2013")} kg</div></div>
        <div class='db-stat-card'><div class='db-stat-lbl'>Height</div>
          <div style='font-family:Bebas Neue,sans-serif;font-size:1.4rem;color:#fff'>{data.get("height","\u2013")} cm</div></div>
        <div class='db-stat-card'><div class='db-stat-lbl'>Age</div>
          <div style='font-family:Bebas Neue,sans-serif;font-size:1.4rem;color:#fff'>{data.get("age","\u2013")} yrs</div></div>
        <div class='db-stat-card' style='border-color:rgba(229,9,20,0.22)'><div class='db-stat-lbl'>BMI</div>
          <div style='font-family:Bebas Neue,sans-serif;font-size:1.4rem;color:#E50914'>{bmi_val:.1f}</div></div>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<div class='sec-lbl'>Workout Calendar</div>", unsafe_allow_html=True)
    _plan_end_date = plan_start + timedelta(days=plan_duration - 1)
    _same_month    = plan_start.month == _plan_end_date.month and plan_start.year == _plan_end_date.year
    month_label    = plan_start.strftime("%B %Y") if _same_month else plan_start.strftime("%b %Y") + " \u2013 " + _plan_end_date.strftime("%b %Y")
    st.markdown(f"<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:10px'>"
                f"<span style='font-size:0.80rem;font-weight:700;color:rgba(255,255,255,0.90)'>{month_label}</span>"
                f"<span style='font-size:0.85rem;color:rgba(255,255,255,0.90);letter-spacing:1px'>{done_count} done &middot; {skipped_count} skipped</span></div>",
                unsafe_allow_html=True)
    DOWS = ["MON","TUE","WED","THU","FRI","SAT","SUN"]
    st.markdown("<div class='cal-hdr-row'>"+"".join(f"<div class='cal-dow'>{d}</div>" for d in DOWS)+"</div>", unsafe_allow_html=True)
    _first_day  = plan_start
    _pad        = _first_day.weekday()
    _cal_cells  = [None] * _pad + calendar_days
    while len(_cal_cells) % 7 != 0: _cal_cells.append(None)
    for _wk_start in range(0, len(_cal_cells), 7):
        week_cells = _cal_cells[_wk_start:_wk_start+7]
        html = "<div class='cal-grid-7'>"
        for cd in week_cells:
            if cd is None:
                html += "<div class='cal-cell' style='opacity:0;pointer-events:none'><div class='cal-num'></div><div class='cal-dot d-pending' style='opacity:0'></div></div>"
                continue
            d = cd["date"]; st_ = cd["status"]
            is_today = d == date.today(); is_past = d < date.today()
            cell_cls = "cal-cell"
            if st_ == "done":      cell_cls += " done-cell"
            elif st_ == "skipped": cell_cls += " skipped-cell"
            elif is_today:         cell_cls += " today-cell"
            elif is_past:          cell_cls += " past-cell"
            dot_cls = "cal-dot " + ("d-done" if st_=="done" else "d-skipped" if st_=="skipped" else "d-today" if is_today else "d-pending")
            html += f"<div class='{cell_cls}'><div class='cal-num'>{d.day}</div><div class='{dot_cls}'></div></div>"
        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)

# ── ROW 3: Up Next + Quick Access ─────────────────────────────────────────────
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
row3_left, row3_right = st.columns([7, 5], gap="medium")

with row3_left:
    st.markdown("<div class='sec-lbl'>Up Next</div>", unsafe_allow_html=True)
    W_ICONS = ["\U0001f3cb\ufe0f","\U0001f4aa","\U0001f3c3","\U0001f94a","\U0001f9d7","\U0001f6b4","\U0001f938","\u26a1","\U0001f525","\U0001f3af","\u26a1","\U0001f4a5"]
    MUSCLE_COLORS = {"chest":"#E50914","back":"#3b82f6","legs":"#22c55e","shoulders":"#f97316",
                     "arms":"#a855f7","core":"#fbbf24","cardio":"#06b6d4","full":"#E50914",
                     "rest":"#64748b","push":"#E50914","pull":"#3b82f6","lower":"#22c55e"}
    upcoming = [cd for cd in calendar_days if cd["date"] >= date.today() and cd["status"] == "pending"]
    if upcoming:
        _up_pairs = [upcoming[i:i+2] for i in range(0, min(len(upcoming), 6), 2)]
        for pair in _up_pairs:
            up_c1, up_c2 = st.columns(2, gap="small")
            for _col_widget, cd in zip([up_c1, up_c2], pair):
                with _col_widget:
                    _si    = _sdays[cd["day_idx"]] if _sdays and cd["day_idx"] < len(_sdays) else None
                    _mg2   = _si.get("muscle_group","Workout") if _si else f"Day {cd['day_idx']+1}"
                    _ex_ct = len(_si.get("workout",[])) if _si else 0
                    _ico   = W_ICONS[cd["day_idx"] % len(W_ICONS)]
                    _da    = (cd["date"] - date.today()).days
                    _dl    = "Today" if _da==0 else ("Tomorrow" if _da==1 else cd["date"].strftime("%b %d"))
                    _rest  = _si.get("is_rest_day",False) if _si else False
                    _accent = "#64748b" if _rest else next((v for k,v in MUSCLE_COLORS.items() if k in _mg2.lower()), "#E50914")
                    _sub_txt   = "Recovery \U0001f634" if _rest else f"{_ex_ct} exercises"
                    _title_txt = "Rest & Recovery" if _rest else _mg2
                    _date_style = f"color:#E50914;background:rgba(229,9,20,0.15);border:1px solid rgba(229,9,20,0.35);border-radius:5px;padding:1px 7px;" if _da==0 else "color:rgba(229,9,20,0.75);"
                    st.markdown(
                        f"<div style='background:rgba(10,6,4,0.75);border:1.5px solid {_accent}33;"
                        f"border-left:4px solid {_accent};border-radius:12px;padding:12px 14px;margin-bottom:8px;'>"
                        f"<div style='display:flex;align-items:center;justify-content:space-between;margin-bottom:6px'>"
                        f"<div style='display:flex;align-items:center;gap:8px'>"
                        f"<div style='width:32px;height:32px;border-radius:8px;background:{_accent}22;border:1px solid {_accent}44;"
                        f"display:flex;align-items:center;justify-content:center;font-size:1.1rem'>{_ico}</div>"
                        f"<div><div style='font-size:0.85rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:{_accent};margin-bottom:2px'>"
                        f"{'REST' if _rest else _mg2.split()[0].upper()[:8]}</div>"
                        f"<div style='font-size:1.00rem;font-weight:700;color:#fff;line-height:1.2'>{_title_txt[:20]}</div>"
                        f"</div></div>"
                        f"<div style='text-align:right'><div style='font-size:0.85rem;font-weight:700;{_date_style}'>{_dl}</div>"
                        f"<div style='font-size:0.85rem;color:rgba(255,255,255,0.90);margin-top:2px'>Day {cd['day_idx']+1}</div></div></div>"
                        f"<div style='font-size:0.85rem;color:rgba(255,255,255,0.90)'>{_sub_txt}</div></div>",
                        unsafe_allow_html=True)
    else:
        st.markdown("<div style='background:rgba(34,197,94,0.08);border:1.5px solid rgba(34,197,94,0.25);"
                    "border-radius:14px;padding:24px;text-align:center'>"
                    "<div style='font-size:2rem;margin-bottom:8px'>\U0001f389</div>"
                    "<div style='font-size:1.05rem;font-weight:700;color:#4ade80'>All workouts complete!</div>"
                    "<div style='font-size:0.85rem;color:rgba(255,255,255,0.90);margin-top:4px'>You crushed this plan!</div>"
                    "</div>", unsafe_allow_html=True)

with row3_right:
    st.markdown("<div class='sec-lbl'>Quick Access</div>", unsafe_allow_html=True)
    _nav_items = [
        ("\u270f\ufe0f", "Edit Profile",  "Update your goals & details",  "pages/1_Profile.py",        "ep"),
        ("\U0001f3c6", "Records",       "PRs, measurements & 1RM",       "pages/6_records.py",        "db_rec"),
        ("\U0001f916", "AI Coach",      "Chat with your fitness coach",  "pages/5_ai_coach.py",       "db_ai2"),
        ("\U0001f4c5", "History",       "Past workouts timeline",        "pages/9_history.py",        "go_history"),
        ("\U0001f957", "Diet Plan",     "Today's meals & nutrition",     "pages/4_Diet_Plan.py",      "go_diet"),
        ("\U0001f4f8", "Photos",        "Track your transformation",     "pages/7_progress_photos.py","go_photos"),
    ]
    for _ni_row in [_nav_items[:3], _nav_items[3:]]:
        _nc = st.columns(3, gap="small")
        for _col_w, (_ico, _lbl, _desc, _path, _key) in zip(_nc, _ni_row):
            with _col_w:
                st.markdown(f"<div style='background:rgba(10,6,4,0.75);border:1.5px solid rgba(229,9,20,0.22);"
                            f"border-radius:12px;padding:14px 10px;text-align:center;backdrop-filter:blur(10px);margin-bottom:8px'>"
                            f"<div style='font-size:1.6rem;margin-bottom:6px'>{_ico}</div>"
                            f"<div style='font-size:0.85rem;font-weight:700;color:#fff'>{_lbl}</div>"
                            f"<div style='font-size:0.85rem;color:rgba(255,255,255,0.90);margin-top:3px;line-height:1.3'>{_desc}</div>"
                            f"</div>", unsafe_allow_html=True)
                if st.button(_lbl, key=_key, use_container_width=True):
                    try: st.switch_page(_path)
                    except Exception: pass

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='plan-btn'>", unsafe_allow_html=True)
    if st.button("\u26a1  View Full Workout Plan", key="vfp", use_container_width=True):
        try: st.switch_page("pages/3_Workout_Plan.py")
        except Exception: pass
    st.markdown("</div>", unsafe_allow_html=True) 