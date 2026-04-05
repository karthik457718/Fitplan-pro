# -*- coding: utf-8 -*-
import streamlit as st
import os, sys, json
from datetime import date
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth_token import logout

st.set_page_config(page_title="Tools | FitPlan Pro", page_icon="🧮",
                   layout="wide", initial_sidebar_state="collapsed")
if not st.session_state.get("logged_in"): st.switch_page("app.py")
if "user_data" not in st.session_state:   st.switch_page("pages/1_Profile.py")

uname = st.session_state.get("username", "Athlete")
data  = st.session_state.user_data

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:opsz,wght@9..40,400;9..40,600;9..40,700&display=swap');
[data-testid="stAppViewContainer"]::before{
  content:'';position:fixed;inset:0;z-index:0;
  background:url('https://images.unsplash.com/photo-1534438327276-14e5300c3a48?fm=jpg&w=1600&q=80&fit=crop') center/cover no-repeat;
  filter:blur(8px) brightness(0.20) saturate(0.40);transform:scale(1.06);}
[data-testid="stAppViewContainer"]{
  background:linear-gradient(160deg,rgba(3,1,0,0.92) 0%,rgba(4,2,0,0.85) 100%)!important;position:relative;}
[data-testid="stAppViewContainer"]>section>div.block-container{
  position:relative;z-index:2;max-width:1100px!important;margin:0 auto!important;padding:0 24px 80px!important;}
#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stDecoration"],
[data-testid="stSidebarNav"],section[data-testid="stSidebar"]{display:none!important;}
html,body,.stApp{background:#050202!important;color:#fff!important;font-family:'DM Sans',sans-serif!important;}

/* Dark inputs */
input,textarea,.stNumberInput>div>div>input,.stTextInput>div>div>input{
  background:#0e0408!important;background-color:#0e0408!important;
  border:1.5px solid rgba(229,9,20,0.40)!important;color:#fff!important;
  border-radius:10px!important;
  box-shadow:inset 0 0 0 9999px #0e0408!important;
  -webkit-box-shadow:inset 0 0 0 9999px #0e0408!important;
  caret-color:#E50914!important;}
[data-baseweb="select"]>div{
  background:#0e0408!important;border:1.5px solid rgba(229,9,20,0.38)!important;
  border-radius:10px!important;color:#fff!important;}
[data-baseweb="select"] span,[data-baseweb="select"] div{color:#fff!important;}
[data-baseweb="popover"] [role="option"]{background:#0e0408!important;color:#fff!important;}
[data-baseweb="popover"] [role="option"]:hover{background:rgba(229,9,20,0.20)!important;}
.stNumberInput [data-testid="stNumberInputStepUp"],
.stNumberInput [data-testid="stNumberInputStepDown"]{
  background:rgba(229,9,20,0.25)!important;border:none!important;color:#fff!important;border-radius:6px!important;}
[data-testid="stForm"]{background:transparent!important;border:none!important;}
[data-testid="stWidgetLabel"],[data-testid="stWidgetLabel"] p{
  color:#fff!important;font-weight:700!important;text-shadow:0 2px 6px rgba(0,0,0,0.99)!important;}

/* Buttons */
.stButton>button{
  background:linear-gradient(135deg,#E50914,#c0000c)!important;border:none!important;
  color:#fff!important;border-radius:10px!important;font-weight:700!important;
  box-shadow:0 4px 16px rgba(229,9,20,0.40)!important;transition:all 0.20s!important;}
.stButton>button:hover{transform:translateY(-2px)!important;box-shadow:0 6px 24px rgba(229,9,20,0.60)!important;}
[data-testid="stFormSubmitButton"] button{
  background:linear-gradient(135deg,#E50914,#b0000a)!important;border:none!important;
  color:#fff!important;border-radius:10px!important;font-weight:700!important;width:100%!important;}

/* Tabs */
.stTabs [data-baseweb="tab-list"]{
  background:rgba(8,4,2,0.88)!important;border-radius:10px!important;
  padding:4px!important;border:1px solid rgba(229,9,20,0.18)!important;}
.stTabs [data-baseweb="tab"]{
  background:transparent!important;color:rgba(255,255,255,0.88)!important;
  border-radius:7px!important;font-size:0.95rem!important;font-weight:700!important;}
.stTabs [aria-selected="true"]{
  background:linear-gradient(135deg,#E50914,#c0000c)!important;color:#fff!important;}

/* Nav */
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"]>button{
  background:rgba(10,4,2,0.82)!important;border:1.5px solid rgba(229,9,20,0.38)!important;
  color:rgba(255,255,255,0.80)!important;border-radius:8px!important;
  font-size:0.82rem!important;font-weight:600!important;height:30px!important;min-height:30px!important;}
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"]>button:hover{
  background:rgba(229,9,20,0.20)!important;color:#fff!important;}
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"]:last-child>button{
  background:rgba(229,9,20,0.25)!important;}

html,body,.stApp,.stMarkdown,p,div,span,label{text-shadow:0 1px 4px rgba(0,0,0,0.95)!important;}
.stMarkdown p,.stMarkdown li{color:#fff!important;line-height:1.75!important;}
.nav-logo{font-family:'Bebas Neue',sans-serif;font-size:1.4rem;letter-spacing:5px;
  color:#E50914;text-shadow:0 0 18px rgba(229,9,20,0.50);}
</style>
""", unsafe_allow_html=True)

# ── NAV ───────────────────────────────────────────────────────────────────────
# ── NAV ─────────────────────────────────────────────────────────────────────
try:
    from nav_component import render_nav
    render_nav("tools", uname)
except Exception as _nav_err:
    st.warning(f"Nav error: {_nav_err}")

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='background:linear-gradient(135deg,rgba(229,9,20,0.12),rgba(8,4,2,0.80));
  border:1.5px solid rgba(229,9,20,0.28);border-radius:18px;padding:24px 32px;margin-bottom:22px;
  position:relative;overflow:hidden'>
  <div style='position:absolute;top:0;left:0;right:0;height:2px;
    background:linear-gradient(90deg,transparent,#E50914,transparent)'></div>
  <div style='font-family:Bebas Neue,sans-serif;font-size:2.2rem;color:#fff;
    letter-spacing:2px;margin-bottom:4px'>🧮 Fitness <span style='color:#E50914'>Tools</span></div>
  <div style='font-size:0.90rem;color:rgba(255,255,255,0.55)'>
    BMI &amp; Body Fat Calculator · Meal Calorie Logger · More</div>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📊 BMI & Body Fat Calculator", "🍽️ Meal Calorie Logger"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1: BMI & BODY FAT CALCULATOR
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown(
        "<div style='font-size:0.75rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;"
        "color:rgba(229,9,20,0.80);margin-bottom:16px;display:flex;align-items:center;gap:8px'>"
        "<span style='width:14px;height:1.5px;background:#E50914;display:block'></span>"
        "Your Body Metrics</div>",
        unsafe_allow_html=True
    )

    bc1, bc2 = st.columns(2)
    with bc1:
        b_weight = st.number_input("Weight (kg)", min_value=30.0, max_value=300.0,
                                    value=float(data.get("weight", 70)), step=0.1, key="bmi_weight")
        b_height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0,
                                    value=float(data.get("height", 170)), step=0.5, key="bmi_height")
    with bc2:
        b_age    = st.number_input("Age", min_value=10, max_value=100,
                                    value=int(data.get("age", 25)), key="bmi_age")
        b_gender = st.selectbox("Gender", ["Male", "Female"],
                                 index=0 if data.get("gender","Male")=="Male" else 1,
                                 key="bmi_gender")
        b_neck   = st.number_input("Neck circumference (cm)", min_value=20.0, max_value=80.0,
                                    value=38.0, step=0.5, key="bmi_neck",
                                    help="Measure around the middle of your neck")
        b_waist  = st.number_input("Waist circumference (cm)", min_value=40.0, max_value=200.0,
                                    value=85.0, step=0.5, key="bmi_waist",
                                    help="Measure at navel level")
        b_hip    = 0.0
        if b_gender == "Female":
            b_hip = st.number_input("Hip circumference (cm)", min_value=40.0, max_value=200.0,
                                     value=95.0, step=0.5, key="bmi_hip")

    # ── CALCULATIONS ─────────────────────────────────────────────────────────
    import math
    h_m  = b_height / 100
    bmi  = b_weight / (h_m ** 2)

    # BMI category
    if bmi < 18.5:
        bmi_cat, bmi_col = "Underweight", "#60a5fa"
    elif bmi < 25:
        bmi_cat, bmi_col = "Normal weight", "#22c55e"
    elif bmi < 30:
        bmi_cat, bmi_col = "Overweight", "#fbbf24"
    else:
        bmi_cat, bmi_col = "Obese", "#ef4444"

    # Body fat % — US Navy Formula
    try:
        if b_gender == "Male":
            bf = 495 / (1.0324 - 0.19077 * math.log10(b_waist - b_neck) + 0.15456 * math.log10(b_height)) - 450
        else:
            bf = 495 / (1.29579 - 0.35004 * math.log10(b_waist + b_hip - b_neck) + 0.22100 * math.log10(b_height)) - 450
        bf = max(3.0, min(bf, 60.0))
    except Exception:
        bf = 20.0

    # BF category
    if b_gender == "Male":
        if bf < 6:    bf_cat, bf_col = "Essential Fat", "#60a5fa"
        elif bf < 14: bf_cat, bf_col = "Athletic",      "#22c55e"
        elif bf < 18: bf_cat, bf_col = "Fitness",       "#22c55e"
        elif bf < 25: bf_cat, bf_col = "Average",       "#fbbf24"
        else:         bf_cat, bf_col = "Obese",         "#ef4444"
    else:
        if bf < 14:   bf_cat, bf_col = "Essential Fat", "#60a5fa"
        elif bf < 21: bf_cat, bf_col = "Athletic",      "#22c55e"
        elif bf < 25: bf_cat, bf_col = "Fitness",       "#22c55e"
        elif bf < 32: bf_cat, bf_col = "Average",       "#fbbf24"
        else:         bf_cat, bf_col = "Obese",         "#ef4444"

    # Lean mass & fat mass
    fat_mass  = round(b_weight * bf / 100, 1)
    lean_mass = round(b_weight - fat_mass, 1)

    # Ideal weight range (BMI 18.5–24.9)
    ideal_low  = round(18.5 * h_m**2, 1)
    ideal_high = round(24.9 * h_m**2, 1)

    # BMR (Mifflin-St Jeor)
    if b_gender == "Male":
        bmr = 10*b_weight + 6.25*b_height - 5*b_age + 5
    else:
        bmr = 10*b_weight + 6.25*b_height - 5*b_age - 161

    # TDEE
    activity_map = {
        "Sedentary (desk job, no exercise)": 1.2,
        "Lightly active (1-3 days/week)":    1.375,
        "Moderately active (3-5 days/week)": 1.55,
        "Very active (6-7 days/week)":       1.725,
        "Athlete (2x/day training)":         1.9,
    }
    act_level = st.selectbox("Activity Level", list(activity_map.keys()),
                              index=2, key="bmi_activity")
    tdee = round(bmr * activity_map[act_level])

    # ── AUTO-SAVE BMI TO DB ───────────────────────────────────────────────────
    try:
        from utils.db import save_user_setting, get_user_setting
        import json as _jbmi
        from datetime import date as _dbmi
        _bmi_record = {
            "date": _dbmi.today().isoformat(),
            "bmi": round(bmi, 1), "bmi_cat": bmi_cat,
            "body_fat": round(bf, 1), "bf_cat": bf_cat,
            "lean_mass": lean_mass, "fat_mass": fat_mass,
            "bmr": int(bmr), "tdee": tdee,
            "weight": b_weight, "height": b_height,
        }
        # Load existing BMI log and prepend
        _existing = get_user_setting(uname, "bmi_log")
        _bmi_log  = _jbmi.loads(_existing) if _existing else []
        # Only save if different from last entry
        if not _bmi_log or _bmi_log[0].get("date") != _bmi_record["date"]:
            _bmi_log.insert(0, _bmi_record)
            _bmi_log = _bmi_log[:30]  # keep last 30 entries
            save_user_setting(uname, "bmi_log", _jbmi.dumps(_bmi_log))
    except Exception:
        pass

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ── RESULTS GRID ─────────────────────────────────────────────────────────
    r1, r2, r3, r4 = st.columns(4)
    for col, val, lbl, color, sub in [
        (r1, f"{bmi:.1f}",     "BMI",          bmi_col,  bmi_cat),
        (r2, f"{bf:.1f}%",     "Body Fat",     bf_col,   bf_cat),
        (r3, f"{lean_mass}kg", "Lean Mass",    "#60a5fa","Fat-free"),
        (r4, f"{fat_mass}kg",  "Fat Mass",     "#fbbf24","Body fat"),
    ]:
        with col:
            st.markdown(
                f"<div style='background:rgba(8,4,2,0.85);border:1.5px solid rgba(229,9,20,0.22);"
                f"border-radius:14px;padding:16px;text-align:center'>"
                f"<div style='font-family:Bebas Neue,sans-serif;font-size:2.2rem;color:{color};line-height:1'>{val}</div>"
                f"<div style='font-size:0.70rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;"
                f"color:rgba(255,255,255,0.55);margin-top:4px'>{lbl}</div>"
                f"<div style='font-size:0.72rem;color:{color};margin-top:3px;font-weight:600'>{sub}</div>"
                f"</div>",
                unsafe_allow_html=True
            )

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    # ── BMI GAUGE ────────────────────────────────────────────────────────────
    bmi_pct = min(max((bmi - 10) / (45 - 10) * 100, 0), 100)
    st.markdown(
        "<div style='background:rgba(8,4,2,0.85);border:1.5px solid rgba(229,9,20,0.20);"
        "border-radius:14px;padding:18px 22px;margin-bottom:14px'>"
        "<div style='font-size:0.72rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;"
        "color:rgba(229,9,20,0.70);margin-bottom:12px'>BMI Scale</div>"
        "<div style='position:relative;height:14px;border-radius:7px;overflow:hidden;"
        "background:linear-gradient(90deg,#60a5fa 0%,#22c55e 25%,#fbbf24 55%,#ef4444 85%)'>"
        f"<div style='position:absolute;top:-3px;left:{bmi_pct}%;transform:translateX(-50%);"
        f"width:20px;height:20px;border-radius:50%;background:#fff;"
        f"border:3px solid {bmi_col};box-shadow:0 2px 8px rgba(0,0,0,0.60)'></div>"
        "</div>"
        "<div style='display:flex;justify-content:space-between;margin-top:8px;font-size:0.68rem;color:rgba(255,255,255,0.40)'>"
        "<span>10 · Underweight</span><span>18.5</span><span>25</span><span>30</span><span>45 · Obese</span>"
        "</div>"
        f"<div style='margin-top:10px;font-size:0.88rem;font-weight:600;color:{bmi_col}'>"
        f"Your BMI: {bmi:.1f} — {bmi_cat} &nbsp;·&nbsp; Ideal weight: {ideal_low}–{ideal_high} kg</div>"
        "</div>",
        unsafe_allow_html=True
    )

    # ── CALORIE TARGETS ───────────────────────────────────────────────────────
    goal = data.get("goal", "General Fitness")
    if "Loss" in goal:
        target_cal = tdee - 500
        goal_label = "Weight Loss (–500 cal deficit)"
        goal_col   = "#22c55e"
    elif "Muscle" in goal:
        target_cal = tdee + 300
        goal_label = "Muscle Gain (+300 cal surplus)"
        goal_col   = "#60a5fa"
    else:
        target_cal = tdee
        goal_label = "Maintain weight"
        goal_col   = "#fbbf24"

    protein_g = round(b_weight * 2.0)
    carbs_g   = round((target_cal * 0.45) / 4)
    fat_g     = round((target_cal * 0.25) / 9)

    st.markdown(
        "<div style='background:rgba(8,4,2,0.85);border:1.5px solid rgba(229,9,20,0.20);"
        "border-radius:14px;padding:18px 22px'>"
        "<div style='font-size:0.72rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;"
        "color:rgba(229,9,20,0.70);margin-bottom:14px'>Daily Calorie & Macro Targets</div>"
        "<div style='display:grid;grid-template-columns:repeat(2,1fr);gap:12px'>"
        f"<div style='background:rgba(229,9,20,0.10);border:1px solid rgba(229,9,20,0.25);"
        f"border-radius:10px;padding:12px;text-align:center'>"
        f"<div style='font-family:Bebas Neue,sans-serif;font-size:2rem;color:#E50914'>{tdee}</div>"
        f"<div style='font-size:0.68rem;text-transform:uppercase;letter-spacing:2px;color:rgba(255,255,255,0.50)'>TDEE (Maintenance)</div></div>"
        f"<div style='background:rgba(0,0,0,0.50);border:1px solid rgba({goal_col.replace('#','')},0.30);"
        f"border-radius:10px;padding:12px;text-align:center'>"
        f"<div style='font-family:Bebas Neue,sans-serif;font-size:2rem;color:{goal_col}'>{target_cal}</div>"
        f"<div style='font-size:0.68rem;text-transform:uppercase;letter-spacing:2px;color:rgba(255,255,255,0.50)'>{goal_label}</div></div>"
        "</div>"
        "<div style='display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:12px'>"
        f"<div style='background:rgba(96,165,250,0.10);border:1px solid rgba(96,165,250,0.25);border-radius:10px;padding:10px;text-align:center'>"
        f"<div style='font-family:Bebas Neue,sans-serif;font-size:1.6rem;color:#60a5fa'>{protein_g}g</div>"
        f"<div style='font-size:0.65rem;text-transform:uppercase;letter-spacing:2px;color:rgba(255,255,255,0.45)'>Protein</div></div>"
        f"<div style='background:rgba(251,191,36,0.10);border:1px solid rgba(251,191,36,0.25);border-radius:10px;padding:10px;text-align:center'>"
        f"<div style='font-family:Bebas Neue,sans-serif;font-size:1.6rem;color:#fbbf24'>{carbs_g}g</div>"
        f"<div style='font-size:0.65rem;text-transform:uppercase;letter-spacing:2px;color:rgba(255,255,255,0.45)'>Carbs</div></div>"
        f"<div style='background:rgba(249,115,22,0.10);border:1px solid rgba(249,115,22,0.25);border-radius:10px;padding:10px;text-align:center'>"
        f"<div style='font-family:Bebas Neue,sans-serif;font-size:1.6rem;color:#f97316'>{fat_g}g</div>"
        f"<div style='font-size:0.65rem;text-transform:uppercase;letter-spacing:2px;color:rgba(255,255,255,0.45)'>Fat</div></div>"
        "</div></div>",
        unsafe_allow_html=True
    )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2: MEAL CALORIE LOGGER
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    today_str = date.today().isoformat()
    log_key   = f"meal_log_{uname}_{today_str}"

    if log_key not in st.session_state:
        try:
            from utils.db import get_user_setting
            _saved = get_user_setting(uname, f"meal_log_{today_str}")
            st.session_state[log_key] = json.loads(_saved) if _saved else []
        except Exception:
            st.session_state[log_key] = []

    meal_log = st.session_state[log_key]

    st.markdown(
        "<div style='font-size:0.75rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;"
        "color:rgba(229,9,20,0.80);margin-bottom:16px;display:flex;align-items:center;gap:8px'>"
        "<span style='width:14px;height:1.5px;background:#E50914;display:block'></span>"
        f"🍽️ Meal Log — {today_str}</div>",
        unsafe_allow_html=True
    )

    # ── QUICK ADD COMMON FOODS ────────────────────────────────────────────────
    COMMON_FOODS = {
        "🥚 Boiled Egg (1)":          {"cal":78,  "protein":6,  "carbs":0,  "fat":5},
        "🍗 Chicken Breast (150g)":   {"cal":165, "protein":31, "carbs":0,  "fat":4},
        "🍚 Brown Rice (1 cup)":      {"cal":216, "protein":5,  "carbs":45, "fat":2},
        "🥛 Greek Yogurt (100g)":     {"cal":59,  "protein":10, "carbs":4,  "fat":1},
        "🍌 Banana (1 medium)":       {"cal":105, "protein":1,  "carbs":27, "fat":0},
        "🥦 Broccoli (100g)":         {"cal":34,  "protein":3,  "carbs":7,  "fat":0},
        "🌾 Oats (50g dry)":          {"cal":190, "protein":7,  "carbs":34, "fat":4},
        "🥜 Peanut Butter (2 tbsp)":  {"cal":190, "protein":8,  "carbs":6,  "fat":16},
        "🐟 Salmon (150g)":           {"cal":280, "protein":39, "carbs":0,  "fat":13},
        "🫘 Dal (1 cup cooked)":      {"cal":230, "protein":18, "carbs":40, "fat":1},
        "🧀 Paneer (100g)":           {"cal":265, "protein":18, "carbs":4,  "fat":20},
        "🥑 Avocado (half)":          {"cal":120, "protein":2,  "carbs":6,  "fat":11},
    }

    st.markdown(
        "<div style='font-size:0.72rem;color:rgba(255,255,255,0.50);margin-bottom:8px'>"
        "Quick-add common foods or enter custom below</div>",
        unsafe_allow_html=True
    )

    qf_cols = st.columns(4)
    for qi, (fname, fdata) in enumerate(COMMON_FOODS.items()):
        with qf_cols[qi % 4]:
            if st.button(fname, key=f"qadd_{qi}", use_container_width=True):
                meal_log.append({
                    "name":    fname,
                    "cal":     fdata["cal"],
                    "protein": fdata["protein"],
                    "carbs":   fdata["carbs"],
                    "fat":     fdata["fat"],
                    "meal":    "Snack",
                    "time":    str(date.today()),
                })
                st.session_state[log_key] = meal_log
                try:
                    from utils.db import save_user_setting
                    save_user_setting(uname, f"meal_log_{today_str}", json.dumps(meal_log))
                except Exception: pass
                st.toast(f"Added {fname}!", icon="✅")
                st.rerun()

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # ── CUSTOM FOOD ENTRY ─────────────────────────────────────────────────────
    with st.expander("➕ Add Custom Food", expanded=False):
        with st.form("custom_food_form", clear_on_submit=True):
            cf1, cf2, cf3 = st.columns(3)
            with cf1:
                cf_name  = st.text_input("Food name", placeholder="e.g. Idli (2 pieces)")
                cf_meal  = st.selectbox("Meal type", ["Breakfast","Lunch","Dinner","Snack"])
            with cf2:
                cf_cal   = st.number_input("Calories (kcal)", min_value=0, max_value=5000, value=100)
                cf_prot  = st.number_input("Protein (g)", min_value=0.0, max_value=200.0, value=0.0, step=0.5)
            with cf3:
                cf_carbs = st.number_input("Carbs (g)", min_value=0.0, max_value=500.0, value=0.0, step=0.5)
                cf_fat   = st.number_input("Fat (g)", min_value=0.0, max_value=200.0, value=0.0, step=0.5)
            if st.form_submit_button("Add to Log", use_container_width=True) and cf_name.strip():
                meal_log.append({
                    "name":    cf_name.strip(),
                    "cal":     cf_cal,
                    "protein": cf_prot,
                    "carbs":   cf_carbs,
                    "fat":     cf_fat,
                    "meal":    cf_meal,
                    "time":    today_str,
                })
                st.session_state[log_key] = meal_log
                try:
                    from utils.db import save_user_setting
                    save_user_setting(uname, f"meal_log_{today_str}", json.dumps(meal_log))
                except Exception: pass
                st.toast(f"Added {cf_name}!", icon="✅")
                st.rerun()

    # ── AI FOOD LOOKUP ────────────────────────────────────────────────────────
    with st.expander("🤖 AI Calorie Lookup", expanded=False):
        ai_food_q = st.text_input("Describe what you ate", placeholder="e.g. 2 chapati with 1 cup dal fry",
                                   key="ai_food_q")
        if st.button("🔍 Look Up Calories", key="ai_food_btn"):
            if ai_food_q.strip():
                with st.spinner("Calculating..."):
                    try:
                        from model_api import query_model
                        _fp = (
                            f"Estimate calories and macros for: '{ai_food_q}'. "
                            "Reply in this exact format:\n"
                            "FOOD: [name]\nCAL: [number]\nPROTEIN: [g]\nCARBS: [g]\nFAT: [g]\n"
                            "Nothing else. Numbers only, no units in values."
                        )
                        _res = query_model(_fp, max_tokens=100).strip()
                        _parsed = {}
                        for line in _res.splitlines():
                            if ":" in line:
                                k,v = line.split(":",1)
                                _parsed[k.strip().upper()] = v.strip()
                        if "CAL" in _parsed:
                            _entry = {
                                "name":    _parsed.get("FOOD", ai_food_q),
                                "cal":     int(float(_parsed.get("CAL",0))),
                                "protein": float(_parsed.get("PROTEIN",0)),
                                "carbs":   float(_parsed.get("CARBS",0)),
                                "fat":     float(_parsed.get("FAT",0)),
                                "meal":    "Custom",
                                "time":    today_str,
                            }
                            meal_log.append(_entry)
                            st.session_state[log_key] = meal_log
                            try:
                                from utils.db import save_user_setting
                                save_user_setting(uname, f"meal_log_{today_str}", json.dumps(meal_log))
                            except Exception: pass
                            st.success(f"Added: {_entry['name']} — {_entry['cal']} kcal | "
                                       f"P:{_entry['protein']}g C:{_entry['carbs']}g F:{_entry['fat']}g")
                            st.rerun()
                        else:
                            st.error("Could not parse. Try a more specific description.")
                    except Exception as e:
                        st.error("AI error: " + str(e))

    # ── TODAY'S LOG ───────────────────────────────────────────────────────────
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    if not meal_log:
        st.markdown(
            "<div style='text-align:center;padding:40px;background:rgba(8,4,2,0.70);"
            "border:1px solid rgba(229,9,20,0.15);border-radius:14px'>"
            "<div style='font-size:2.5rem;margin-bottom:8px'>🍽️</div>"
            "<div style='color:rgba(255,255,255,0.50);font-size:0.90rem'>Nothing logged yet today.<br>"
            "Use quick-add buttons or add a custom food above.</div></div>",
            unsafe_allow_html=True
        )
    else:
        # Totals
        total_cal  = sum(e.get("cal",0)     for e in meal_log)
        total_prot = sum(e.get("protein",0) for e in meal_log)
        total_carb = sum(e.get("carbs",0)   for e in meal_log)
        total_fat  = sum(e.get("fat",0)     for e in meal_log)

        # Compare against plan target
        _wt = float(data.get("weight", 70))
        _ht = float(data.get("height", 170))
        _ag = int(data.get("age", 25))
        _gn = data.get("gender", "Male")
        _bmr2 = 10*_wt + 6.25*_ht - 5*_ag + (5 if _gn=="Male" else -161)
        _tdee2 = round(_bmr2 * 1.55)
        _goal2 = data.get("goal","")
        _target2 = _tdee2 - 500 if "Loss" in _goal2 else (_tdee2 + 300 if "Muscle" in _goal2 else _tdee2)
        _cal_pct = min(int(total_cal / max(_target2,1) * 100), 150)
        _cal_col = "#22c55e" if _cal_pct <= 105 else "#ef4444"

        # Summary bar
        st.markdown(
            f"<div style='background:rgba(8,4,2,0.88);border:1.5px solid rgba(229,9,20,0.22);"
            f"border-radius:14px;padding:16px 20px;margin-bottom:14px'>"
            f"<div style='font-size:0.72rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;"
            f"color:rgba(229,9,20,0.70);margin-bottom:12px'>Today's Totals</div>"
            f"<div style='display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:14px'>"
            + "".join([
                f"<div style='text-align:center'>"
                f"<div style='font-family:Bebas Neue,sans-serif;font-size:1.8rem;color:{c}'>{v}</div>"
                f"<div style='font-size:0.65rem;letter-spacing:2px;text-transform:uppercase;"
                f"color:rgba(255,255,255,0.45)'>{l}</div></div>"
                for v,l,c in [
                    (f"{total_cal} kcal", "Calories",   _cal_col),
                    (f"{round(total_prot)}g",  "Protein",    "#60a5fa"),
                    (f"{round(total_carb)}g",  "Carbs",      "#fbbf24"),
                    (f"{round(total_fat)}g",   "Fat",        "#f97316"),
                ]
            ]) +
            f"</div>"
            f"<div style='font-size:0.75rem;color:rgba(255,255,255,0.45);margin-bottom:6px'>"
            f"Target: {_target2} kcal &nbsp;·&nbsp; {_cal_pct}% of daily goal</div>"
            f"<div style='height:8px;background:rgba(255,255,255,0.08);border-radius:4px;overflow:hidden'>"
            f"<div style='height:100%;width:{min(_cal_pct,100)}%;background:{_cal_col};border-radius:4px'></div>"
            f"</div></div>",
            unsafe_allow_html=True
        )

        # Food entries
        for i, entry in enumerate(reversed(meal_log)):
            ri = len(meal_log) - 1 - i
            ec1, ec2 = st.columns([5, 1])
            with ec1:
                st.markdown(
                    f"<div style='background:rgba(8,4,2,0.75);border:1px solid rgba(229,9,20,0.15);"
                    f"border-radius:10px;padding:10px 14px;margin-bottom:6px;"
                    f"display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px'>"
                    f"<div>"
                    f"<div style='font-size:0.90rem;font-weight:600;color:#fff'>{entry.get('name','Food')}</div>"
                    f"<div style='font-size:0.72rem;color:rgba(255,255,255,0.40);margin-top:2px'>"
                    f"{entry.get('meal','')}</div></div>"
                    f"<div style='display:flex;gap:12px;font-size:0.80rem'>"
                    f"<span style='color:#E50914;font-weight:700'>{entry.get('cal',0)} kcal</span>"
                    f"<span style='color:#60a5fa'>P:{entry.get('protein',0)}g</span>"
                    f"<span style='color:#fbbf24'>C:{entry.get('carbs',0)}g</span>"
                    f"<span style='color:#f97316'>F:{entry.get('fat',0)}g</span>"
                    f"</div></div>",
                    unsafe_allow_html=True
                )
            with ec2:
                if st.button("🗑", key=f"del_meal_{ri}", use_container_width=True):
                    meal_log.pop(ri)
                    st.session_state[log_key] = meal_log
                    try:
                        from utils.db import save_user_setting
                        save_user_setting(uname, f"meal_log_{today_str}", json.dumps(meal_log))
                    except Exception: pass
                    st.rerun()

        if st.button("🗑 Clear All Today's Log", key="clear_log"):
            st.session_state[log_key] = []
            try:
                from utils.db import save_user_setting
                save_user_setting(uname, f"meal_log_{today_str}", "[]")
            except Exception: pass
            st.rerun()