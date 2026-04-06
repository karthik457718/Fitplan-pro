# -*- coding: utf-8 -*-
import streamlit as st
import os, sys, json
from datetime import date
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth_token import logout
from bg_utils import apply_bg

st.set_page_config(page_title="Records | FitPlan Pro", page_icon="🏆",
                   layout="wide", initial_sidebar_state="collapsed")

if not st.session_state.get("logged_in"): st.switch_page("app.py")
if "user_data" not in st.session_state:   st.switch_page("pages/1_Profile.py")

uname = st.session_state.get("username", "Athlete")
data  = st.session_state.user_data

st.markdown("""
<style>
[data-testid="stAppViewContainer"]::before{
  content:'';position:fixed;inset:0;z-index:0;
  background:url('https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?fm=jpg&w=1600&q=80&fit=crop') center center/cover no-repeat;
  filter:blur(8px) brightness(0.25) saturate(0.55);transform:scale(1.06);}
[data-testid="stAppViewContainer"]{
  background:linear-gradient(160deg,rgba(3,1,0,0.90) 0%,rgba(4,2,0,0.82) 50%,rgba(3,1,0,0.94) 100%)!important;position:relative;}
[data-testid="stAppViewContainer"]>section>div.block-container{position:relative;z-index:2;}
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow+Condensed:wght@700;800;900&family=DM+Sans:opsz,wght@9..40,400;9..40,600;9..40,700&display=swap');
#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stDecoration"],
[data-testid="stSidebarNav"],[data-testid="collapsedControl"],
section[data-testid="stSidebar"],button[kind="header"]{display:none!important;}
html,body,.stApp{background:#050202!important;color:#fff!important;font-family:'DM Sans',sans-serif!important;}
[data-testid="stAppViewContainer"]>section>div.block-container{
  max-width:1100px!important;margin:0 auto!important;padding:0 24px 80px!important;
  background:rgba(0,0,0,0.35)!important;border-radius:0!important;}

/* ── LABELS ── */
[data-testid="stWidgetLabel"],[data-testid="stWidgetLabel"] p{
  color:#fff!important;font-size:1.00rem!important;font-weight:700!important;
  text-shadow:0 2px 8px rgba(0,0,0,0.99)!important;}

/* ── BUTTONS ── */
[data-testid="stFormSubmitButton"] button,.stFormSubmitButton>button,button[kind="secondaryFormSubmit"]{
  background:linear-gradient(135deg,#E50914,#c0000c)!important;border:none!important;
  color:#fff!important;border-radius:10px!important;font-weight:700!important;
  box-shadow:0 4px 20px rgba(229,9,20,0.45)!important;text-transform:uppercase!important;}
.stButton>button{background:linear-gradient(135deg,rgba(229,9,20,0.85),rgba(160,0,10,0.90))!important;
  border:2px solid rgba(229,9,20,0.65)!important;color:#fff!important;border-radius:10px!important;
  font-family:'DM Sans',sans-serif!important;font-size:1.0rem!important;font-weight:700!important;
  box-shadow:0 0 12px rgba(229,9,20,0.30)!important;transition:all 0.20s!important;}
.stButton>button:hover{transform:translateY(-2px)!important;box-shadow:0 0 24px rgba(229,9,20,0.60)!important;}

/* ── FIX: DARK INPUTS — nuclear override for all Streamlit input types ── */
input, textarea,
input[type="number"], input[type="text"],
.stNumberInput input, .stTextInput input,
.stNumberInput>div>div>input, .stTextInput>div>div>input,
[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea,
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input,
div[data-baseweb="input"],
div[data-baseweb="base-input"]{
  background:#1a0a06!important;
  background-color:#1a0a06!important;
  border:1.5px solid rgba(229,9,20,0.55)!important;
  color:#fff!important;border-radius:10px!important;
  box-shadow:inset 0 0 0 9999px #1a0a06!important;
  -webkit-box-shadow:inset 0 0 0 9999px #1a0a06!important;
  font-family:'DM Sans',sans-serif!important;
  caret-color:#E50914!important;}
input:focus, input[type="number"]:focus, input[type="text"]:focus,
.stNumberInput input:focus, .stTextInput input:focus{
  background:#200c07!important;background-color:#200c07!important;
  border-color:rgba(229,9,20,0.90)!important;
  box-shadow:inset 0 0 0 9999px #200c07, 0 0 0 2px rgba(229,9,20,0.25)!important;
  -webkit-box-shadow:inset 0 0 0 9999px #200c07!important;
  outline:none!important;}
/* Step buttons */
.stNumberInput [data-testid="stNumberInputStepUp"],
.stNumberInput [data-testid="stNumberInputStepDown"],
[data-testid="stNumberInputStepUp"],
[data-testid="stNumberInputStepDown"]{
  background:rgba(229,9,20,0.35)!important;border:none!important;
  color:#fff!important;border-radius:8px!important;}
/* Container wrapper also dark */
[data-baseweb="input"]{
  background:#1a0a06!important;background-color:#1a0a06!important;
  border:1.5px solid rgba(229,9,20,0.55)!important;border-radius:10px!important;}
/* Autofill override */
input:-webkit-autofill,input:-webkit-autofill:hover,
input:-webkit-autofill:focus,input:-webkit-autofill:active{
  -webkit-box-shadow:0 0 0 9999px #1a0a06 inset!important;
  -webkit-text-fill-color:#fff!important;}

/* ── FIX: DARK SELECTBOX ── */
[data-baseweb="select"]>div{background:rgba(8,4,2,0.90)!important;
  border:1.5px solid rgba(229,9,20,0.40)!important;border-radius:12px!important;
  backdrop-filter:blur(28px)!important;color:#fff!important;}
[data-baseweb="select"] span{color:#fff!important;}
[data-baseweb="popover"] [role="option"]{background:rgba(10,6,4,0.96)!important;color:#fff!important;}
[data-baseweb="popover"] [role="option"]:hover{background:rgba(229,9,20,0.25)!important;}

/* ── FIX: TRANSPARENT FORM ── */
[data-testid="stForm"]{background:transparent!important;border:none!important;}

/* ── NAV BUTTONS ── */
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"]>button{
  background:rgba(18,4,4,0.82)!important;border:2px solid rgba(229,9,20,0.65)!important;
  color:rgba(255,255,255,0.92)!important;border-radius:9px!important;
  font-size:0.85rem!important;font-weight:700!important;padding:5px 8px!important;
  height:32px!important;min-height:32px!important;white-space:nowrap!important;}
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"]>button:hover{
  background:rgba(229,9,20,0.28)!important;border-color:rgba(229,9,20,0.85)!important;color:#fff!important;}
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"]:last-child>button{
  background:linear-gradient(135deg,#c0000c,#8b0000)!important;border-color:rgba(229,9,20,0.80)!important;}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"]{background:rgba(8,4,2,0.88)!important;
  border-radius:10px!important;padding:4px!important;border:1px solid rgba(229,9,20,0.18)!important;}
.stTabs [data-baseweb="tab"]{background:transparent!important;color:rgba(255,255,255,0.90)!important;
  border-radius:7px!important;font-size:0.95rem!important;font-weight:700!important;
  border:none!important;padding:9px 16px!important;text-shadow:0 2px 6px rgba(0,0,0,0.95)!important;}
.stTabs [aria-selected="true"]{background:linear-gradient(135deg,#E50914,#c0000c)!important;
  color:#fff!important;box-shadow:0 3px 12px rgba(229,9,20,0.40)!important;}

/* ── EXPANDERS DARK ── */
.stExpander{background:rgba(8,4,2,0.82)!important;
  border:1.5px solid rgba(229,9,20,0.22)!important;border-radius:14px!important;}
.stExpander details summary{color:#fff!important;font-weight:700!important;
  font-size:1.00rem!important;text-shadow:0 2px 6px rgba(0,0,0,0.95)!important;}

.nav-logo{font-family:'Bebas Neue',sans-serif;font-size:1.4rem;letter-spacing:5px;
  color:#E50914;text-shadow:0 0 18px rgba(229,9,20,0.45);line-height:1;}

/* ── GLOBAL VISIBILITY ── */
html,body,.stApp,.stMarkdown,p,div,span,label{text-shadow:0 2px 6px rgba(0,0,0,0.98)!important;}
.stCheckbox>label,.stCheckbox>label p{color:#fff!important;font-weight:700!important;font-size:1.05rem!important;}
.stMarkdown p,.stMarkdown li{color:#fff!important;font-size:1.05rem!important;line-height:1.75!important;}
.g-panel{background:rgba(8,4,2,0.88)!important;backdrop-filter:blur(32px)!important;}
</style>
""", unsafe_allow_html=True)

apply_bg(
    "https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?fm=jpg&w=1600&q=80&fit=crop",
    overlay="rgba(8,5,3,0.78)"
)

# ── NAV ───────────────────────────────────────────────────────────────────────
try:
    from nav_component import render_nav
    render_nav("records", uname)
except Exception as _nav_err:
    st.warning(f"Nav error: {_nav_err}")

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='background:linear-gradient(135deg,rgba(251,191,36,0.15),rgba(217,149,0,0.08) 40%,rgba(6,4,1,0.70));
  border:1px solid rgba(251,191,36,0.30);border-radius:18px;padding:28px 36px;margin-bottom:24px;
  position:relative;overflow:hidden'>
  <div style='position:absolute;top:0;left:0;right:0;height:2px;
    background:linear-gradient(90deg,transparent,#fbbf24,transparent)'></div>
  <div style='font-family:Bebas Neue,sans-serif;font-size:2.4rem;font-weight:900;
    text-transform:uppercase;color:#fff;line-height:1;margin-bottom:6px'>
    Personal <span style='color:#fbbf24'>Records</span></div>
  <div style='font-size:1.00rem;color:rgba(255,255,255,0.70)'>
    Track your PRs, body measurements, and progress over time</div>
</div>
""", unsafe_allow_html=True)

@st.cache_data(ttl=180)
def _load_prs(uname):
    try:
        from utils.db import get_personal_records
        return get_personal_records(uname) or []
    except Exception:
        return []

@st.cache_data(ttl=180)
def _load_measurements(uname):
    try:
        from utils.db import get_body_measurements
        return get_body_measurements(uname) or []
    except Exception:
        return []

tab1, tab2, tab3, tab4 = st.tabs(["🏆 Personal Records","📏 Body Measurements","📐 1RM Calculator","🎖️ Achievements"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1: PERSONAL RECORDS
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    PRESET_EXERCISES = ["Bench Press","Squat","Deadlift","Overhead Press","Pull-ups",
        "Push-ups","Barbell Row","Dumbbell Curl","Tricep Dip","Leg Press",
        "Lat Pulldown","Cable Row","Plank (seconds)","Running 1km (seconds)","Custom"]

    if "personal_records" not in st.session_state: st.session_state.personal_records = {}
    records = st.session_state.personal_records

    if not st.session_state.get("_pr_loaded"):
        try:
            from utils.db import get_personal_records as _gpr
            _db_records = _gpr(uname)
            if _db_records:
                st.session_state.personal_records = _db_records
                records = _db_records
        except Exception: pass
        st.session_state._pr_loaded = True

    st.markdown(
        "<div style='font-size:0.75rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;"
        "color:rgba(229,9,20,0.85);margin-bottom:10px;display:flex;align-items:center;gap:8px'>"
        "<span style='width:16px;height:1.5px;background:#E50914;display:block'></span>"
        "Log New PR</div>", unsafe_allow_html=True)

    with st.form("pr_form"):
        fc1,fc2,fc3,fc4 = st.columns([3,2,2,1])
        with fc1: ex_choice  = st.selectbox("Exercise", PRESET_EXERCISES, key="pr_ex")
        with fc2: custom_name = st.text_input("Custom name", placeholder="e.g. Incline Press", key="pr_custom")
        with fc3: pr_val      = st.number_input("Value (kg/reps/sec)", min_value=0.0, step=0.5, key="pr_val")
        with fc4: pr_unit     = st.selectbox("Unit", ["kg","reps","seconds","lbs"], key="pr_unit")
        if st.form_submit_button("Save PR", use_container_width=True) and pr_val > 0:
            ex_name = custom_name.strip() if ex_choice=="Custom" and custom_name.strip() else ex_choice
            today_s = date.today().isoformat()
            if ex_name not in records: records[ex_name] = []
            records[ex_name].append({"date":today_s,"value":pr_val,"unit":pr_unit})
            records[ex_name] = sorted(records[ex_name], key=lambda x: x["date"])
            st.session_state.personal_records = records
            try:
                from utils.db import save_personal_records as _spr
                _spr(uname, records)
            except Exception: pass
            st.success("PR saved: " + ex_name + " — " + str(pr_val) + " " + pr_unit)
            st.rerun()

    if not records:
        st.markdown(
            "<div style='text-align:center;padding:40px;background:rgba(8,4,2,0.70);"
            "border:1px solid rgba(229,9,20,0.15);border-radius:14px;margin-top:12px'>"
            "<div style='font-size:3rem;margin-bottom:12px'>🏆</div>"
            "<div style='font-family:Barlow Condensed,sans-serif;font-size:1.6rem;font-weight:800;color:#fff;margin-bottom:8px'>No Personal Records Yet</div>"
            "<div style='font-size:0.90rem;color:rgba(255,255,255,0.65);max-width:320px;margin:0 auto;line-height:1.6'>Log your first PR using the form above. Track lifts, runs, time — anything you want to beat!</div>"
            "<div style='margin-top:16px;background:rgba(229,9,20,0.10);border:1px solid rgba(229,9,20,0.25);border-radius:12px;padding:10px 18px;display:inline-block;font-size:0.80rem;color:rgba(229,9,20,0.80);font-weight:700;'>👆 Use the form above to log your first PR</div>"
            "</div>", unsafe_allow_html=True)
    else:
        for ex_name, ex_records in records.items():
            if not ex_records: continue
            best = max(ex_records, key=lambda x: x["value"])
            unit = best["unit"]
            with st.expander("🏅 " + ex_name + " — Best: " + str(best["value"]) + " " + unit, expanded=False):
                if len(ex_records) >= 2:
                    vals  = [r["value"] for r in ex_records[-10:]]
                    dates = [r["date"][-5:] for r in ex_records[-10:]]
                    mn, mx = min(vals)-1, max(vals)+1
                    N = len(vals)
                    pts  = " ".join(str(int(i*(180/max(N-1,1)))) + "," + str(int(((mx-v)/(mx-mn))*60)) for i,v in enumerate(vals))
                    dots = "".join(
                        '<circle cx="' + str(int(i*(180/max(N-1,1)))) + '" cy="' + str(int(((mx-v)/(mx-mn))*60)) +
                        '" r="4" fill="#E50914" stroke="rgba(0,0,0,0.5)" stroke-width="1.5"/>'
                        for i,v in enumerate(vals))
                    st.markdown(
                        "<div style='background:rgba(8,4,2,0.80);border:1px solid rgba(229,9,20,0.22);"
                        "border-radius:12px;padding:14px 16px;margin-bottom:10px'>"
                        "<svg viewBox='0 0 200 80' style='width:100%;height:80px'>"
                        "<polyline points='" + pts + "' fill='none' stroke='#E50914' stroke-width='2' stroke-linecap='round'/>"
                        + dots +
                        "<text x='0' y='77' fill='rgba(255,255,255,0.55)' font-size='7'>" + dates[0] + "</text>"
                        "<text x='200' y='77' fill='rgba(255,255,255,0.55)' font-size='7' text-anchor='end'>" + dates[-1] + "</text>"
                        "</svg></div>", unsafe_allow_html=True)
                for r in reversed(ex_records[-5:]):
                    is_best = r["value"] == best["value"]
                    badge   = " &#127942; PR" if is_best else ""
                    color   = "#fbbf24" if is_best else "#fff"
                    st.markdown(
                        "<div style='display:flex;justify-content:space-between;padding:5px 0;"
                        "border-bottom:1px solid rgba(255,255,255,0.06);font-size:0.90rem'>"
                        "<span style='color:rgba(255,255,255,0.55)'>" + r["date"] + "</span>"
                        "<span style='color:" + color + ";font-weight:700'>"
                        + str(r["value"]) + " " + r["unit"] + badge + "</span></div>",
                        unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2: BODY MEASUREMENTS — dark inputs, no white boxes
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    MEASUREMENTS = ["Chest (cm)","Waist (cm)","Hips (cm)","Left Arm (cm)","Right Arm (cm)",
                    "Left Thigh (cm)","Right Thigh (cm)","Neck (cm)","Shoulders (cm)","Calf (cm)"]

    if "body_measurements" not in st.session_state: st.session_state.body_measurements = []
    meas_list = st.session_state.body_measurements

    if not st.session_state.get("_meas_loaded"):
        try:
            from utils.db import get_body_measurements as _gbm
            _db_meas = _gbm(uname)
            if _db_meas:
                st.session_state.body_measurements = _db_meas
                meas_list = _db_meas
        except Exception: pass
        st.session_state._meas_loaded = True

    st.markdown(
        "<div style='font-size:0.75rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;"
        "color:rgba(229,9,20,0.85);margin-bottom:12px;display:flex;align-items:center;gap:8px'>"
        "<span style='width:16px;height:1.5px;background:#E50914;display:block'></span>"
        "Log Today's Measurements (cm)</div>", unsafe_allow_html=True)

    st.markdown(
        "<div style='background:rgba(8,4,2,0.88);border:1.5px solid rgba(229,9,20,0.25);"
        "border-radius:16px;padding:20px 24px;margin-bottom:12px'>",
        unsafe_allow_html=True)
    with st.form("meas_form"):
        mc1, mc2 = st.columns(2)
        meas_vals = {}
        for i, m in enumerate(MEASUREMENTS[:5]):
            with mc1: meas_vals[m] = st.number_input(m, min_value=0.0, step=0.5, key="meas_"+str(i))
        for i, m in enumerate(MEASUREMENTS[5:]):
            with mc2: meas_vals[m] = st.number_input(m, min_value=0.0, step=0.5, key="meas_"+str(i+5))
        if st.form_submit_button("💾 Save Measurements", use_container_width=True):
            entry = {"date":date.today().isoformat(),"measurements":{k:v for k,v in meas_vals.items() if v>0}}
            if entry["measurements"]:
                meas_list.append(entry)
                st.session_state.body_measurements = meas_list
                try:
                    from utils.db import save_body_measurements as _sbm
                    _sbm(uname, meas_list)
                except Exception: pass
                st.success("✅ Measurements saved!")
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    if meas_list:
        st.markdown(
            "<div style='font-size:0.75rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;"
            "color:rgba(229,9,20,0.85);margin:20px 0 12px;display:flex;align-items:center;gap:8px'>"
            "<span style='width:16px;height:1.5px;background:#E50914;display:block'></span>"
            "Progress Charts</div>", unsafe_allow_html=True)
        key_measures = ["Chest (cm)","Waist (cm)","Hips (cm)","Left Arm (cm)","Left Thigh (cm)"]
        cols = st.columns(3)
        for ci, metric in enumerate(key_measures[:3]):
            vals_m = [(e["date"][-5:], e["measurements"].get(metric,0)) for e in meas_list if e["measurements"].get(metric,0)>0]
            if len(vals_m) < 2: continue
            with cols[ci % 3]:
                _dates_m = [v[0] for v in vals_m[-8:]]
                _vals_m  = [v[1] for v in vals_m[-8:]]
                mn2, mx2 = min(_vals_m)-1, max(_vals_m)+1
                N2 = len(_vals_m)
                pts2  = " ".join(str(int(i*(120/max(N2-1,1)))) + "," + str(int(((mx2-v)/(mx2-mn2))*50)) for i,v in enumerate(_vals_m))
                dots2 = "".join(
                    '<circle cx="' + str(int(i*(120/max(N2-1,1)))) + '" cy="' + str(int(((mx2-v)/(mx2-mn2))*50)) +
                    '" r="3" fill="#E50914" stroke="rgba(0,0,0,0.5)" stroke-width="1"/>'
                    for i,v in enumerate(_vals_m))
                delta = _vals_m[-1] - _vals_m[0]
                dcol  = "#22c55e" if delta<=0 else "#ef4444"
                dsym  = "▼" if delta<=0 else "▲"
                st.markdown(
                    "<div style='background:rgba(8,4,2,0.88);border:1.5px solid rgba(229,9,20,0.22);"
                    "border-radius:12px;padding:12px 14px;margin-bottom:8px'>"
                    "<div style='font-size:0.70rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;"
                    "color:rgba(255,255,255,0.50);margin-bottom:4px'>" + metric.replace(" (cm)","") + "</div>"
                    "<div style='font-size:1.2rem;font-weight:700;color:#fff'>" + str(round(_vals_m[-1],1)) + " cm "
                    "<span style='font-size:0.85rem;color:" + dcol + "'>" + dsym + " " + str(round(abs(delta),1)) + "</span></div>"
                    "<svg viewBox='0 0 130 60' style='width:100%;height:60px;margin-top:6px'>"
                    "<polyline points='" + pts2 + "' fill='none' stroke='#E50914' stroke-width='1.5'/>"
                    + dots2 +
                    "<text x='0' y='58' fill='rgba(255,255,255,0.40)' font-size='6'>" + _dates_m[0] + "</text>"
                    "<text x='120' y='58' fill='rgba(255,255,255,0.40)' font-size='6' text-anchor='end'>" + _dates_m[-1] + "</text>"
                    "</svg></div>", unsafe_allow_html=True)
    else:
        st.markdown(
            "<div style='text-align:center;padding:40px;background:rgba(8,4,2,0.70);"
            "border:1px solid rgba(229,9,20,0.15);border-radius:14px;margin-top:12px'>"
            "<div style='font-size:2.5rem;margin-bottom:10px'>&#128207;</div>"
            "<div style='font-size:3rem;margin-bottom:12px'>📏</div>"
                "<div style='font-family:Barlow Condensed,sans-serif;font-size:1.6rem;font-weight:800;color:#fff;margin-bottom:8px'>No Measurements Logged</div>"
                "<div style='font-size:0.90rem;color:rgba(255,255,255,0.65);max-width:320px;margin:0 auto;line-height:1.6'>Start tracking your body measurements to see your transformation over time. Every centimetre counts!</div>"
                "<div style='margin-top:16px;background:rgba(229,9,20,0.10);border:1px solid rgba(229,9,20,0.25);border-radius:12px;padding:10px 18px;display:inline-block;font-size:0.80rem;color:rgba(229,9,20,0.80);font-weight:700;'>👆 Log your first measurements above</div>"
            "</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3: 1RM CALCULATOR — fixed formula visibility
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown(
        "<div style='font-size:0.75rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;"
        "color:rgba(229,9,20,0.85);margin-bottom:16px;display:flex;align-items:center;gap:8px'>"
        "<span style='width:16px;height:1.5px;background:#E50914;display:block'></span>"
        "One Rep Max Calculator</div>", unsafe_allow_html=True)

    # FIX: Formula card — dark background, bright yellow formula text
    st.markdown(
        "<div style='background:rgba(8,4,2,0.92);border:1.5px solid rgba(251,191,36,0.42);"
        "border-radius:14px;padding:18px 24px;margin-bottom:20px'>"
        "<div style='font-size:0.65rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;"
        "color:rgba(251,191,36,0.85);margin-bottom:10px'>📐 Epley Formula</div>"
        "<div style='background:rgba(0,0,0,0.55);border-radius:10px;padding:12px 18px;margin-bottom:10px'>"
        "<span style='font-family:monospace;font-size:1.15rem;font-weight:700;"
        "color:#fbbf24;letter-spacing:1px'>1RM = weight × (1 + reps ÷ 30)</span>"
        "</div>"
        "<div style='font-size:0.88rem;color:rgba(255,255,255,0.65);line-height:1.6'>"
        "The <b style='color:#fff'>1RM</b> is the maximum weight you can lift for one rep. "
        "We average <b style='color:#E50914'>3 formulas</b> (Epley, Brzycki, Lander) for accuracy.</div>"
        "</div>",
        unsafe_allow_html=True)

    orm_exercises = ["Bench Press","Squat","Deadlift","Overhead Press","Barbell Row",
                     "Pull-ups","Dumbbell Press","Leg Press","Romanian Deadlift","Cable Row","Custom"]
    rc1,rc2,rc3,rc4 = st.columns([3,2,2,2])
    with rc1: orm_ex     = st.selectbox("Exercise", orm_exercises, key="orm_ex")
    with rc2: orm_custom = st.text_input("Custom name", placeholder="e.g. Incline Press", key="orm_custom")
    with rc3: orm_weight = st.number_input("Weight (kg)", min_value=1.0, max_value=500.0, value=60.0, step=2.5, key="orm_weight")
    with rc4: orm_reps   = st.number_input("Reps", min_value=1, max_value=30, value=5, step=1, key="orm_reps")

    w, r    = float(orm_weight), int(orm_reps)
    epley   = w * (1 + r/30)
    brzycki = w * (36/(37-r)) if r < 37 else w
    lander  = (100*w)/(101.3 - 2.67123*r)
    avg_1rm = (epley + brzycki + lander) / 3
    ex_name = orm_custom.strip() if orm_ex=="Custom" and orm_custom.strip() else orm_ex

    pcts = [(95,"1-2 reps","Strength Max"),(85,"4-6 reps","Strength"),
            (75,"8-10 reps","Hypertrophy"),(65,"12-15 reps","Endurance")]
    pct_html = "".join(
        "<div style='background:rgba(8,4,2,0.88);border:1.5px solid rgba(229,9,20,0.28);"
        "border-radius:10px;padding:10px 12px;flex:1;min-width:100px;text-align:center'>"
        "<div style='font-size:0.65rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;"
        "color:rgba(229,9,20,0.80);margin-bottom:4px'>" + str(pct) + "%</div>"
        "<div style='font-family:Bebas Neue,sans-serif;font-size:1.4rem;color:#fff'>"
        + str(round(avg_1rm*pct/100,1)) + "kg</div>"
        "<div style='font-size:0.65rem;color:rgba(255,255,255,0.50);margin-top:2px'>" + rng + "</div>"
        "<div style='font-size:0.60rem;color:rgba(255,255,255,0.35)'>" + zone + "</div></div>"
        for pct, rng, zone in pcts)

    st.markdown(
        "<div style='background:linear-gradient(135deg,rgba(229,9,20,0.18),rgba(160,0,10,0.10) 60%,rgba(8,4,2,0.90));"
        "border:1.5px solid rgba(229,9,20,0.50);border-radius:16px;padding:24px 28px;margin-top:16px;"
        "position:relative;overflow:hidden'>"
        "<div style='position:absolute;top:0;left:0;right:0;height:2px;"
        "background:linear-gradient(90deg,transparent,#E50914,transparent)'></div>"
        "<div style='font-size:0.70rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;"
        "color:rgba(229,9,20,0.80);margin-bottom:8px'>&#128170; " + ex_name + " — Estimated 1RM</div>"
        "<div style='font-family:Bebas Neue,sans-serif;font-size:4.5rem;color:#E50914;"
        "letter-spacing:2px;line-height:1;margin-bottom:4px'>" + str(round(avg_1rm,1)) +
        " <span style='font-size:2rem;color:rgba(255,255,255,0.80)'>kg</span></div>"
        "<div style='font-size:0.75rem;color:rgba(255,255,255,0.50);margin-bottom:20px'>"
        "Average of 3 formulas | " + str(r) + " reps @ " + str(w) + "kg</div>"
        "<div style='display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:20px'>"
        "<div style='background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.10);"
        "border-radius:10px;padding:10px;text-align:center'>"
        "<div style='font-size:0.60rem;letter-spacing:2px;text-transform:uppercase;"
        "color:rgba(255,255,255,0.40);margin-bottom:4px'>EPLEY</div>"
        "<div style='font-family:Bebas Neue,sans-serif;font-size:1.6rem;color:#fff'>" + str(round(epley,1)) + "kg</div></div>"
        "<div style='background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.10);"
        "border-radius:10px;padding:10px;text-align:center'>"
        "<div style='font-size:0.60rem;letter-spacing:2px;text-transform:uppercase;"
        "color:rgba(255,255,255,0.40);margin-bottom:4px'>BRZYCKI</div>"
        "<div style='font-family:Bebas Neue,sans-serif;font-size:1.6rem;color:#fff'>" + str(round(brzycki,1)) + "kg</div></div>"
        "<div style='background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.10);"
        "border-radius:10px;padding:10px;text-align:center'>"
        "<div style='font-size:0.60rem;letter-spacing:2px;text-transform:uppercase;"
        "color:rgba(255,255,255,0.40);margin-bottom:4px'>LANDER</div>"
        "<div style='font-family:Bebas Neue,sans-serif;font-size:1.6rem;color:#fff'>" + str(round(lander,1)) + "kg</div></div>"
        "</div>"
        "<div style='font-size:0.70rem;color:rgba(255,255,255,0.45);margin-bottom:10px;"
        "letter-spacing:1px;text-transform:uppercase'>Training % Targets</div>"
        "<div style='display:flex;gap:8px;flex-wrap:wrap'>" + pct_html + "</div></div>",
        unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4: ACHIEVEMENTS
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown(
        "<div style='font-size:0.75rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;"
        "color:rgba(229,9,20,0.85);margin-bottom:16px;display:flex;align-items:center;gap:8px'>"
        "<span style='width:16px;height:1.5px;background:#E50914;display:block'></span>"
        "Your Achievement Badges</div>", unsafe_allow_html=True)
    try:
        from utils.achievements import compute_stats, get_earned_badges, get_next_badge, render_badges_html, BADGES
        stats  = compute_stats(uname, st.session_state)
        earned = get_earned_badges(stats)
        next_b = get_next_badge(stats)

        st.markdown(
            "<div style='background:rgba(8,4,2,0.88);border:1.5px solid rgba(229,9,20,0.28);"
            "border-radius:14px;padding:16px 20px;margin-bottom:20px;"
            "display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px'>"
            "<div><div style='font-family:Bebas Neue,sans-serif;font-size:2.2rem;color:#E50914;line-height:1'>"
            + str(len(earned)) + " / " + str(len(BADGES)) + "</div>"
            "<div style='font-size:0.80rem;color:rgba(255,255,255,0.60);letter-spacing:2px;text-transform:uppercase'>Badges Earned</div></div>"
            "<div style='text-align:right'>"
            "<div style='font-size:0.75rem;color:rgba(255,255,255,0.50)'>Completion</div>"
            "<div style='height:8px;width:200px;background:rgba(255,255,255,0.08);border-radius:4px;overflow:hidden;margin-top:6px'>"
            "<div style='height:100%;width:" + str(int(len(earned)/max(len(BADGES),1)*100)) + "%;background:#E50914;border-radius:4px'></div>"
            "</div></div></div>", unsafe_allow_html=True)

        if next_b:
            st.markdown(
                "<div style='background:rgba(251,191,36,0.08);border:1.5px solid rgba(251,191,36,0.28);"
                "border-radius:12px;padding:14px 18px;margin-bottom:20px;display:flex;align-items:center;gap:14px'>"
                "<div style='font-size:2.5rem'>" + next_b["icon"] + "</div>"
                "<div><div style='font-size:0.65rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;"
                "color:rgba(251,191,36,0.80);margin-bottom:4px'>&#127919; Next Badge to Unlock</div>"
                "<div style='font-size:0.92rem;font-weight:700;color:#fff'>" + next_b["title"] + "</div>"
                "<div style='font-size:0.75rem;color:rgba(255,255,255,0.60);margin-top:2px'>" + next_b["desc"] + "</div>"
                "</div></div>", unsafe_allow_html=True)

        if earned:
            st.markdown("<div style='font-size:0.80rem;color:rgba(255,255,255,0.60);margin-bottom:12px'>&#127942; Earned Badges</div>", unsafe_allow_html=True)
            st.markdown(render_badges_html(earned), unsafe_allow_html=True)

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        with st.expander("&#128274; Locked Badges — " + str(len(BADGES)-len(earned)) + " remaining", expanded=False):
            earned_ids  = {b["id"] for b in earned}
            locked_html = "<div style='display:flex;flex-wrap:wrap;gap:10px'>"
            for bid, icon, title, desc, _ in BADGES:
                if bid not in earned_ids:
                    locked_html += (
                        "<div style='background:rgba(8,4,2,0.75);border:1.5px solid rgba(255,255,255,0.08);"
                        "border-radius:12px;padding:14px 16px;text-align:center;min-width:120px;flex:1;max-width:150px;opacity:0.55'>"
                        "<div style='font-size:2rem;margin-bottom:6px;filter:grayscale(100%)'>" + icon + "</div>"
                        "<div style='font-size:0.80rem;font-weight:700;color:rgba(255,255,255,0.70);margin-bottom:3px'>" + title + "</div>"
                        "<div style='font-size:0.65rem;color:rgba(255,255,255,0.40);line-height:1.4'>" + desc + "</div></div>")
            st.markdown(locked_html + "</div>", unsafe_allow_html=True)
    except Exception as e:
        st.error("Achievements error: " + str(e)) 