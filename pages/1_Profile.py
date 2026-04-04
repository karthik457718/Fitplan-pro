import streamlit as st
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth_token import logout

st.set_page_config(page_title="FitPlan Pro – Profile", page_icon="⚡", layout="wide")

if not st.session_state.get("logged_in"):
    st.switch_page("app.py")

uname = st.session_state.get("username", "Athlete")

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow+Condensed:wght@700;800;900&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700&display=swap');
::-webkit-scrollbar{width:5px;}
::-webkit-scrollbar-track{background:rgba(255,255,255,0.04);}
::-webkit-scrollbar-thumb{background:rgba(229,9,20,0.40);border-radius:3px;}
#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stDecoration"],
[data-testid="stSidebarNav"],section[data-testid="stSidebar"]{display:none!important;}
:root{--red:#E50914;--ease:cubic-bezier(0.22,1,0.36,1);}
html,body,.stApp,[data-testid="stAppViewContainer"]{font-family:'DM Sans',sans-serif!important;color:#fff!important;}
[data-testid="stAppViewContainer"]::before{
  content:'';position:fixed;inset:0;z-index:0;
  background:url('https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=1920&q=85&auto=format&fit=crop&crop=focalpoint&fp-x=0.5&fp-y=0.4')
  center 40% / cover no-repeat;
  filter:blur(8px) brightness(0.28) saturate(0.6);transform:scale(1.06);}
[data-testid="stAppViewContainer"]{
  background:linear-gradient(160deg,rgba(2,1,8,0.82) 0%,rgba(4,2,10,0.70) 40%,rgba(2,1,8,0.85) 100%)!important;
  position:relative;}
[data-testid="stAppViewContainer"]>section>div.block-container{
  max-width:900px!important;margin:0 auto!important;padding:0 28px 100px!important;position:relative;z-index:2;}
.nav-logo{font-family:'Bebas Neue',sans-serif;font-size:1.9rem;letter-spacing:5px;color:var(--red);text-shadow:0 0 28px rgba(229,9,20,0.5);}
[data-testid="stVerticalBlockBorderWrapper"]{
  background:rgba(8,4,18,0.82)!important;border:2px solid rgba(229,9,20,0.45)!important;
  border-radius:20px!important;backdrop-filter:blur(40px) saturate(1.6) brightness(1.05)!important;
  -webkit-backdrop-filter:blur(40px) saturate(1.6) brightness(1.05)!important;
  box-shadow:inset 0 1px 0 rgba(255,255,255,0.10),inset 0 0 40px rgba(0,0,0,0.40),0 0 0 1px rgba(229,9,20,0.12),0 24px 70px rgba(0,0,0,0.75)!important;
  padding:32px 36px 28px!important;margin-bottom:16px!important;position:relative;overflow:hidden;
  animation:breathe 5s ease-in-out infinite;}
[data-testid="stVerticalBlockBorderWrapper"]::before{
  content:'';position:absolute;top:0;left:0;right:0;height:1.5px;
  background:linear-gradient(90deg,transparent,rgba(229,9,20,0.45) 30%,rgba(255,80,80,0.25) 50%,rgba(229,9,20,0.45) 70%,transparent);z-index:1;}
@keyframes breathe{
  0%,100%{box-shadow:inset 0 1px 0 rgba(255,255,255,0.10),inset 0 0 40px rgba(0,0,0,0.40),0 0 0 1px rgba(229,9,20,0.12),0 24px 70px rgba(0,0,0,0.75);}
  50%{box-shadow:inset 0 1px 0 rgba(255,255,255,0.12),inset 0 0 40px rgba(0,0,0,0.40),0 0 0 1px rgba(229,9,20,0.25),0 28px 80px rgba(0,0,0,0.82),0 0 50px rgba(229,9,20,0.08);}}
[data-testid="stWidgetLabel"],[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] span,.stTextInput>label,.stNumberInput>label,
.stSelectbox>label,.stMultiSelect>label,.stCheckbox>label,.stRadio>label{
  color:#fff!important;font-size:1.05rem!important;font-weight:700!important;
  letter-spacing:2px!important;text-transform:uppercase!important;
  text-shadow:0 1px 12px rgba(0,0,0,0.99)!important;opacity:1!important;}
input,textarea,.stTextInput input,.stNumberInput input,
[data-testid="stTextInput"] input,[data-testid="stNumberInput"] input{
  background:rgba(8,5,20,0.55)!important;border:2px solid rgba(229,9,20,0.45)!important;
  color:#fff!important;border-radius:10px!important;font-family:'DM Sans',sans-serif!important;
  font-size:0.95rem!important;backdrop-filter:blur(32px)!important;-webkit-backdrop-filter:blur(32px)!important;
  box-shadow:0 0 0 1px rgba(229,9,20,0.08),inset 0 1px 0 rgba(255,255,255,0.06),0 4px 16px rgba(0,0,0,0.40)!important;
  transition:all 0.25s!important;}
input:focus,.stTextInput input:focus,.stNumberInput input:focus{
  background:rgba(14,6,26,0.80)!important;border-color:rgba(229,9,20,0.90)!important;
  box-shadow:0 0 24px rgba(229,9,20,0.40),0 0 8px rgba(229,9,20,0.20),0 0 0 3px rgba(229,9,20,0.12),inset 0 1px 0 rgba(255,255,255,0.10),0 4px 24px rgba(0,0,0,0.55)!important;
  outline:none!important;}
.stSelectbox>div>div,.stMultiSelect>div>div,[data-testid="stSelectbox"]>div>div,[data-baseweb="select"]>div{
  background:rgba(8,5,20,0.55)!important;border:2px solid rgba(229,9,20,0.45)!important;
  color:#fff!important;border-radius:10px!important;backdrop-filter:blur(32px)!important;
  -webkit-backdrop-filter:blur(32px)!important;}
.stNumberInput [data-testid="stNumberInputStepDown"],.stNumberInput [data-testid="stNumberInputStepUp"],
[data-testid="stNumberInputStepDown"],[data-testid="stNumberInputStepUp"]{
  background:rgba(229,9,20,0.20)!important;border:2px solid rgba(229,9,20,0.55)!important;
  color:#fff!important;border-radius:6px!important;}
[data-testid="stForm"]{background:transparent!important;border:none!important;}
section[data-testid="stFormSubmitButton"] button,[data-testid="baseButton-secondaryFormSubmit"]{width:100%!important;}
.stButton>button{
  background:linear-gradient(135deg,rgba(229,9,20,0.85),rgba(160,0,10,0.90))!important;
  border:2px solid rgba(229,9,20,0.65)!important;color:#fff!important;border-radius:10px!important;
  font-family:'Barlow Condensed',sans-serif!important;font-size:1.05rem!important;font-weight:700!important;
  letter-spacing:2px!important;text-transform:uppercase!important;
  box-shadow:0 0 18px rgba(229,9,20,0.40),0 4px 16px rgba(229,9,20,0.20)!important;
  transition:all 0.22s cubic-bezier(0.34,1.56,0.64,1)!important;min-height:52px!important;}
.stButton>button:hover{
  background:linear-gradient(135deg,#E50914,#c0000c)!important;
  transform:translateY(-2px) scale(1.02)!important;
  box-shadow:0 0 32px rgba(229,9,20,0.65),0 8px 28px rgba(229,9,20,0.35)!important;}
[data-testid="baseButton-secondaryFormSubmit"],.stFormSubmitButton>button,
section[data-testid="stFormSubmitButton"]>div>button{
  background:linear-gradient(135deg,#E50914,#b0000a)!important;
  border:2px solid rgba(229,9,20,0.65)!important;color:#fff!important;border-radius:10px!important;
  font-family:'Barlow Condensed',sans-serif!important;font-size:1.1rem!important;font-weight:800!important;
  letter-spacing:3px!important;text-transform:uppercase!important;min-height:56px!important;width:100%!important;
  animation:btn-pulse 2.5s ease-in-out infinite!important;}
@keyframes btn-pulse{
  0%,100%{box-shadow:0 0 18px rgba(229,9,20,0.45),0 4px 18px rgba(229,9,20,0.25);}
  50%{box-shadow:0 0 36px rgba(229,9,20,0.80),0 6px 30px rgba(229,9,20,0.50);}}
.gen-btn .stButton>button{
  background:linear-gradient(135deg,#E50914,#c0000c)!important;
  border-color:rgba(229,9,20,0.5)!important;color:#fff!important;
  animation:glow-pulse 2.4s ease-in-out infinite!important;}
@keyframes glow-pulse{
  0%,100%{box-shadow:0 0 18px rgba(229,9,20,0.45),0 4px 18px rgba(229,9,20,0.25);}
  50%{box-shadow:0 0 32px rgba(229,9,20,0.75),0 6px 28px rgba(229,9,20,0.45);}}
.stCheckbox [data-testid="stCheckbox"] span{border-color:rgba(229,9,20,0.50)!important;}
hr{border-color:rgba(255,255,255,0.90)!important;margin:20px 0!important;}
div[data-testid="stHorizontalBlock"]{gap:12px!important;}
html,body,.stApp,.stMarkdown,p,div,span,label{text-shadow:0 2px 6px rgba(0,0,0,0.98)!important;}
[data-testid="stWidgetLabel"],[data-testid="stWidgetLabel"] p{color:#fff!important;font-size:1.05rem!important;font-weight:700!important;text-shadow:0 2px 8px rgba(0,0,0,0.99)!important;}
.stCheckbox>label,.stCheckbox>label p{color:#fff!important;font-weight:700!important;font-size:1.05rem!important;text-shadow:0 2px 8px rgba(0,0,0,0.99)!important;}
.stTabs [data-baseweb="tab"]{color:rgba(255,255,255,0.92)!important;font-size:0.95rem!important;font-weight:700!important;text-shadow:0 2px 6px rgba(0,0,0,0.95)!important;}
.stExpander details summary{color:#fff!important;font-size:1.05rem!important;font-weight:700!important;text-shadow:0 2px 6px rgba(0,0,0,0.95)!important;}
.stMarkdown p,.stMarkdown li{color:#fff!important;font-size:1.05rem!important;line-height:1.75!important;text-shadow:0 2px 8px rgba(0,0,0,0.99)!important;}
</style>
""", unsafe_allow_html=True)

# ── Popover dark fix ──────────────────────────────────────────────────────────
st.markdown("""
<style>
[data-baseweb="popover"],[data-baseweb="popover"] *{background-color:#0d0818!important;color:#fff!important;}
[data-baseweb="popover"]{border:2px solid rgba(229,9,20,0.37)!important;border-radius:14px!important;box-shadow:0 20px 60px rgba(0,0,0,0.92)!important;}
[data-baseweb="menu"]{background:#0d0818!important;}
[data-baseweb="menu"] ul,[data-baseweb="menu"] li{background:#0d0818!important;color:rgba(255,255,255,0.80)!important;}
li[role="option"]{background:#0d0818!important;color:rgba(255,255,255,0.78)!important;font-family:'DM Sans',sans-serif!important;padding:10px 14px!important;margin:1px 6px!important;border-radius:8px!important;cursor:pointer!important;}
li[role="option"]:hover{background:rgba(229,9,20,0.18)!important;color:#fff!important;}
li[aria-selected="true"]{background:rgba(229,9,20,0.25)!important;color:#fff!important;}
[data-baseweb="tag"]{background:rgba(229,9,20,0.18)!important;border:2px solid rgba(229,9,20,0.47)!important;border-radius:6px!important;margin:2px!important;}
[data-baseweb="tag"] span{color:#fff!important;}
div[data-baseweb="multi-select"]{background:rgba(255,255,255,0.06)!important;}
div[data-baseweb="multi-select"]>div{background:rgba(255,255,255,0.06)!important;color:#fff!important;}
div[data-baseweb="multi-select"] input{background:transparent!important;color:#fff!important;}
div[data-baseweb="select"] div div{background:transparent!important;color:#fff!important;}
</style>
""", unsafe_allow_html=True)

# ── NAV ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"] > button{
  background:rgba(18,4,4,0.82)!important;border:1.5px solid rgba(229,9,20,0.55)!important;
  color:rgba(255,255,255,0.92)!important;border-radius:8px!important;
  font-family:'DM Sans',sans-serif!important;font-size:0.75rem!important;font-weight:700!important;
  padding:4px 4px!important;height:30px!important;min-height:30px!important;
  white-space:nowrap!important;overflow:hidden!important;text-overflow:ellipsis!important;
  letter-spacing:0.5px!important;text-transform:none!important;
  box-shadow:none!important;transition:all 0.15s!important;}
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"] > button:hover{
  background:rgba(229,9,20,0.22)!important;border-color:rgba(229,9,20,0.85)!important;
  color:#fff!important;transform:none!important;}
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"]:last-child > button{
  background:linear-gradient(135deg,#c0000c,#8b0000)!important;border-color:rgba(229,9,20,0.80)!important;}
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"] > button[disabled]{
  opacity:0.35!important;cursor:not-allowed!important;}
</style>
""", unsafe_allow_html=True)

_has_plan = bool(st.session_state.get("structured_days"))
_pn = st.columns([1.6, 0.8, 0.8, 0.8, 0.8, 0.9, 0.9, 0.8, 0.85, 0.95])
with _pn[0]:
    st.markdown("<div class='nav-logo' style='font-size:1.1rem;letter-spacing:3px;'>⚡ FITPLAN PRO</div>", unsafe_allow_html=True)
with _pn[1]:
    if st.button("🏠 Home",    key="pn_db", use_container_width=True, disabled=not _has_plan):
        st.switch_page("pages/2_Dashboard.py")
with _pn[2]:
    if st.button("⚡ Workout", key="pn_wp", use_container_width=True, disabled=not _has_plan):
        st.switch_page("pages/3_Workout_Plan.py")
with _pn[3]:
    if st.button("🥗 Diet",    key="pn_dp", use_container_width=True, disabled=not _has_plan):
        try: st.switch_page("pages/4_Diet_Plan.py")
        except Exception: pass
with _pn[4]:
    if st.button("🍽️ Meals",  key="pn_mp", use_container_width=True):
        try: st.switch_page("pages/11_meal_planner.py")
        except Exception: pass
with _pn[5]:
    if st.button("🤖 AI Coach",key="pn_ai", use_container_width=True):
        try: st.switch_page("pages/5_ai_coach.py")
        except Exception: pass
with _pn[6]:
    if st.button("🏆 Records", key="pn_rc", use_container_width=True):
        try: st.switch_page("pages/6_records.py")
        except Exception: pass
with _pn[7]:
    if st.button("📸 Photos",  key="pn_ph", use_container_width=True):
        try: st.switch_page("pages/7_progress_photos.py")
        except Exception: pass
with _pn[8]:
    if st.button("● Profile",  key="pn_pr", use_container_width=True):
        st.rerun()
with _pn[9]:
    if st.button("🚪 Sign Out",key="pn_so", use_container_width=True):
        logout(uname)
        for k in ["logged_in","username","auth_token","user_data","workout_plan","structured_days",
                  "dietary_type","full_plan_data","plan_id","plan_start","plan_duration","plan_for",
                  "force_regen","tracking","_plan_checked","_db_loaded_dash","_auto_redirect",
                  "_diet_chosen","_needs_rerun","_db_streak","edit_profile_mode","_login_db_err"]:
            st.session_state.pop(k, None)
        st.switch_page("app.py")
        st.switch_page("app.py")

st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

# ── On login: load profile + plan from DB ────────────────────────────────────
if not st.session_state.get("_plan_checked"):
    st.session_state._plan_checked = True
    try:
        from utils.db import get_user_profile
        saved_profile = get_user_profile(uname)
        if saved_profile:
            st.session_state.user_data = saved_profile
    except Exception:
        import traceback; traceback.print_exc()
    try:
        from utils.db import get_active_plan
        existing = get_active_plan(uname)
        if existing and existing.get("days") and len(existing["days"]) > 0:
            for _k in ["structured_days","full_plan_data","workout_plan","plan_id","dietary_type","plan_start"]:
                st.session_state.pop(_k, None)
        if existing and existing.get("days"):
            days = existing["days"]
            structured = []
            for d in days:
                day_obj = {
                    "day":          d.get("day_number", 1),
                    "is_rest_day":  d.get("is_rest_day", False),
                    "muscle_group": d.get("muscle_group", "Full Body"),
                    "workout":      d.get("workout_json", []),
                    "dietary":      d.get("dietary_json", {}),
                    "pre_stretch":  d.get("pre_stretch_json", []),
                    "post_stretch": d.get("post_stretch_json", []),
                }
                structured.append(day_obj)
            structured.sort(key=lambda x: x["day"])
            st.session_state.structured_days = structured
            st.session_state.full_plan_data  = structured
            st.session_state.dietary_type    = existing.get("dietary_type", "veg")
            st.session_state.plan_id         = existing.get("plan_id", "")
            st.session_state.workout_plan    = "\n".join([f"## Day {d['day']} - {d['muscle_group']}" for d in structured])
            st.session_state.plan_for        = uname
            st.session_state._auto_redirect  = True
    except Exception:
        pass
    if not st.session_state.get("_auto_redirect") and st.session_state.get("user_data"):
        st.session_state._auto_redirect = True

if st.session_state.get("_auto_redirect"):
    st.session_state.pop("_auto_redirect", None)
    st.switch_page("pages/2_Dashboard.py")

ud        = st.session_state.get("user_data", {})
edit_mode = st.session_state.get("edit_profile_mode", False)
has_plan  = bool(st.session_state.get("structured_days"))

INJURY_OPTIONS = [
    "knee", "shoulder", "back", "wrist", "ankle", "elbow",
    "hip", "neck", "hamstring", "calf", "rotator cuff", "achilles"
]

# ══════════════════════════════════════════════════════════════════════════════
# PROFILE FORM
# ══════════════════════════════════════════════════════════════════════════════
if not ud or edit_mode:
    st.markdown(
        f"<div style='background:linear-gradient(135deg,rgba(229,9,20,0.10),rgba(229,9,20,0.04));"
        f"border:2px solid rgba(229,9,20,0.35);border-radius:18px;padding:24px 32px;margin-bottom:22px;"
        f"position:relative;overflow:hidden'>"
        f"<div style='position:absolute;top:0;left:0;right:0;height:2px;"
        f"background:linear-gradient(90deg,transparent,#E50914,transparent)'></div>"
        f"<div style='font-size:0.85rem;font-weight:700;letter-spacing:4px;text-transform:uppercase;"
        f"color:rgba(229,9,20,0.80);margin-bottom:6px'>Welcome Back</div>"
        f"<div style='font-family:Bebas Neue,sans-serif;font-size:2.6rem;letter-spacing:3px;"
        f"color:#fff;line-height:1;text-shadow:0 0 30px rgba(229,9,20,0.30)'>"
        f"WELCOME, <span style='color:#E50914'>{uname.upper()}!</span></div>"
        f"<div style='font-size:1.00rem;color:rgba(255,255,255,0.90);margin-top:8px'>"
        f"Fill in your body details to generate your personalised AI fitness plan.</div></div>",
        unsafe_allow_html=True
    )

    with st.form("profile_form"):
        c1, c2 = st.columns(2)
        with c1:
            age    = st.number_input("Age", min_value=10, max_value=100, value=int(ud.get("age", 25)))
            height = st.number_input("Height (cm)", min_value=100, max_value=250, value=int(ud.get("height", 170)))
        with c2:
            saved_gen = ud.get("gender", "Male")
            gender = st.selectbox("Gender", ["Male","Female"],
                                  index=["Male","Female"].index(saved_gen if saved_gen in ["Male","Female"] else "Male"))
            weight = st.number_input("Weight (kg)", min_value=30, max_value=250, value=int(ud.get("weight", 70)))
        c3, c4 = st.columns(2)
        with c3:
            level = st.selectbox("Fitness Level", ["Beginner","Intermediate","Advanced"],
                                 index=["Beginner","Intermediate","Advanced"].index(ud.get("level","Beginner")))
        with c4:
            goal = st.selectbox("Fitness Goal", ["Weight Loss","Build Muscle","General Fitness"],
                                index=["Weight Loss","Build Muscle","General Fitness"].index(ud.get("goal","Weight Loss")))
        c5, c6 = st.columns(2)
        with c5:
            dpw = st.selectbox("Training Days/Week", [3,4,5,6,7],
                               index=[3,4,5,6,7].index(int(ud.get("days_per_week", 5))))
        with c6:
            months = st.selectbox("Program Length", [1,2,3],
                                  index=[1,2,3].index(int(ud.get("months", 1))),
                                  format_func=lambda x: f"{x} month{'s' if x>1 else ''}")

        home_eq = st.multiselect("🏠 Home & Basic Equipment", [
            "Dumbbells","Adjustable Dumbbells","Resistance Bands","Pull-up Bar",
            "Dip Station","Bench","Kettlebell","Jump Rope","Push-up Handles",
            "Ab Roller","Yoga Mat","Foam Roller","TRX / Suspension Bands",
            "Battle Ropes","Medicine Ball"
        ], default=ud.get("home_eq", []))

        gym_eq = st.multiselect("🏋️ Commercial Gym Equipment", [
            "Barbell + Rack","EZ Curl Bar","Cable Machine","Smith Machine",
            "Lat Pulldown","Seated Cable Row","Leg Press","Leg Curl Machine",
            "Leg Extension Machine","Chest Fly Machine","Pec Deck",
            "Incline / Decline Bench","Preacher Curl Bench","Dip Machine",
            "Treadmill","Elliptical","Rowing Machine","Stationary Bike",
            "Stair Climber","Assisted Pull-up Machine"
        ], default=ud.get("gym_eq", []))

        no_eq = st.checkbox("🤸 Bodyweight Only — no equipment needed", value=ud.get("no_eq", False))

        # ── INJURY / LIMITATIONS SECTION ─────────────────────────────────
        st.markdown("""
        <div style='margin-top:24px;margin-bottom:6px'>
          <div style='display:flex;align-items:center;gap:10px;font-size:0.85rem;font-weight:700;
               letter-spacing:3.5px;text-transform:uppercase;color:rgba(255,255,255,0.90);margin-bottom:4px'>
            <span style='width:20px;height:1.5px;background:#E50914;display:inline-block;border-radius:1px'></span>
            ⚠️ Any Injuries or Limitations? (We'll Adjust Exercises)
          </div>
          <div style='font-size:0.78rem;color:rgba(255,255,255,0.55);margin-bottom:12px;padding-left:30px'>
            Select any injured or sensitive areas. Exercises targeting these will be replaced with safe alternatives.
          </div>
        </div>
        """, unsafe_allow_html=True)

        injuries = st.multiselect(
            "Injuries or Limitations",
            options=INJURY_OPTIONS,
            default=ud.get("injuries", []),
            key="injuries_select",
            label_visibility="collapsed"
        )

        submitted = st.form_submit_button("💾 SAVE PROFILE & CONTINUE →", use_container_width=True)

    # ── Regenerate button ─────────────────────────────────────────────────────
    has_plan = bool(st.session_state.get("structured_days"))
    if has_plan:
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        regen_col1, regen_col2 = st.columns([1,1])
        with regen_col1:
            st.markdown("""
            <div style='background:rgba(229,9,20,0.06);border:1px solid rgba(229,9,20,0.25);
            border-radius:12px;padding:12px 16px;font-size:0.80rem;color:rgba(255,255,255,0.90);line-height:1.5'>
            <b style='color:rgba(229,9,20,0.80)'>&#128260; Regenerate Plan</b><br>
            Clears your current plan and generates a brand new one with your updated profile settings.
            </div>
            """, unsafe_allow_html=True)
        with regen_col2:
            st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
            if st.button("🔄 REGENERATE PLAN", use_container_width=True, key="regen_form_btn_profile"):
                for _k in ["workout_plan","structured_days","dietary_type","full_plan_data",
                           "plan_id","_diet_chosen","force_regen","_db_loaded_dash",
                           "_notes_loaded","_plan_checked","_diet_step",
                           "_selected_cuisine_id","_selected_cuisine_label","_selected_cuisine_icon"]:
                    st.session_state.pop(_k, None)
                st.session_state.force_regen = True
                try:
                    from utils.db import delete_active_plan
                    delete_active_plan(uname)
                except Exception:
                    pass
                st.success("Plan cleared! Redirecting to generate your new plan...")
                st.switch_page("pages/3_Workout_Plan.py")
    else:
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style='background:rgba(229,9,20,0.06);border:1px solid rgba(229,9,20,0.15);
        border-radius:10px;padding:10px 14px;font-size:0.75rem;color:rgba(255,255,255,0.90);text-align:center'>
        &#128221; Fill in your profile above and click Save to generate your personalised plan
        </div>
        """, unsafe_allow_html=True)

    if submitted:
        total_days = dpw * 4 * months
        equipment  = [] if no_eq else list(set(home_eq + gym_eq))
        profile = {
            "name":         uname,
            "age":          age,
            "gender":       gender,
            "height":       height,
            "weight":       weight,
            "level":        level,
            "goal":         goal,
            "days_per_week": dpw,
            "months":       months,
            "total_days":   total_days,
            "equipment":    equipment,
            "home_eq":      home_eq,
            "gym_eq":       gym_eq,
            "no_eq":        no_eq,
            "injuries":     injuries,
        }
        st.session_state.user_data = profile
        try:
            from utils.db import save_user_profile
            save_user_profile(uname, profile)
        except Exception:
            pass
        st.session_state.edit_profile_mode = False
        st.toast("✅ Profile saved!", icon="👤")
        if st.session_state.get("force_regen"):
            try:
                from utils.db import delete_active_plan
                delete_active_plan(uname)
                for _k in ["structured_days","dietary_type","full_plan_data","plan_id","_diet_chosen","workout_plan"]:
                    st.session_state.pop(_k, None)
            except Exception:
                pass
        st.switch_page("pages/3_Workout_Plan.py")

    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PROFILE DISPLAY
# ══════════════════════════════════════════════════════════════════════════════
else:
    from prompt_builder import calculate_bmi, bmi_category
    bmi     = calculate_bmi(ud["weight"], ud["height"])
    bmi_cat = bmi_category(bmi)

    st.markdown(
        f"<div style='background:linear-gradient(135deg,rgba(229,9,20,0.10),rgba(229,9,20,0.04));"
        f"border:2px solid rgba(229,9,20,0.35);border-radius:18px;padding:24px 32px;margin-bottom:22px;"
        f"position:relative;overflow:hidden'>"
        f"<div style='position:absolute;top:0;left:0;right:0;height:2px;"
        f"background:linear-gradient(90deg,transparent,#E50914,transparent)'></div>"
        f"<div style='font-size:0.85rem;font-weight:700;letter-spacing:4px;text-transform:uppercase;"
        f"color:rgba(229,9,20,0.80);margin-bottom:6px'>Your Profile</div>"
        f"<div style='font-family:Bebas Neue,sans-serif;font-size:2.6rem;letter-spacing:3px;"
        f"color:#fff;line-height:1;text-shadow:0 0 30px rgba(229,9,20,0.30)'>"
        f"WELCOME, <span style='color:#E50914'>{uname.upper()}!</span></div>"
        f"<div style='font-size:1.00rem;color:rgba(255,255,255,0.90);margin-top:8px'>"
        f"Here's your body stats and active plan summary.</div></div>",
        unsafe_allow_html=True
    )

    # ── Body Stats ────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div style='display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:16px'>
    {"".join([
        f"<div style='background:rgba(12,6,24,0.82);border:1.5px solid rgba(229,9,20,0.35);border-radius:14px;padding:18px;text-align:center;backdrop-filter:blur(20px)'>"
        f"<div style='font-size:0.85rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.90);margin-bottom:6px'>{lbl}</div>"
        f"<div style='font-family:Bebas Neue,sans-serif;font-size:1.8rem;color:#fff;letter-spacing:1px'>{val}</div>"
        f"<div style='font-size:1.00rem;color:rgba(255,255,255,0.90)'>{unit}</div></div>"
        for lbl,val,unit in [
            ("Age",    ud['age'],          "years"),
            ("Height", ud['height'],       "cm"),
            ("Weight", ud['weight'],       "kg"),
            ("BMI",    f"{bmi:.1f}",       bmi_cat),
            ("Level",  ud['level'],        "fitness"),
            ("Goal",   ud['goal'].replace(' ','<br>'), ""),
        ]
    ])}
    </div>
    <div style='font-size:0.80rem;color:rgba(255,255,255,0.90);margin-bottom:16px'>
      📅 {ud['days_per_week']} days/week · {ud['months']} month{'s' if ud['months']>1 else ''} · {ud['total_days']} total days
    </div>
    """, unsafe_allow_html=True)

    # ── Injuries ──────────────────────────────────────────────────────────────
    saved_injuries = ud.get("injuries", [])
    if saved_injuries:
        injury_tags = "".join([
            f"<span style='display:inline-flex;align-items:center;gap:4px;"
            f"background:rgba(251,191,36,0.10);border:1px solid rgba(251,191,36,0.35);"
            f"border-radius:100px;padding:4px 12px;font-size:0.75rem;font-weight:700;"
            f"letter-spacing:1px;text-transform:uppercase;color:rgba(251,191,36,0.90);margin:3px'>⚠️ {inj}</span>"
            for inj in saved_injuries
        ])
        st.markdown(
            f"<div style='background:rgba(251,191,36,0.06);border:1.5px solid rgba(251,191,36,0.25);"
            f"border-radius:14px;padding:14px 20px;margin-bottom:14px'>"
            f"<div style='font-size:0.75rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;"
            f"color:rgba(251,191,36,0.75);margin-bottom:8px'>⚠️ Injury Adaptations Active</div>"
            f"<div style='display:flex;flex-wrap:wrap;gap:4px'>{injury_tags}</div>"
            f"<div style='font-size:0.75rem;color:rgba(255,255,255,0.55);margin-top:8px'>"
            f"Exercises targeting these areas have been replaced with safe alternatives.</div></div>",
            unsafe_allow_html=True
        )

    # ── Plan status ───────────────────────────────────────────────────────────
    if has_plan:
        plan_days = len(st.session_state.structured_days)
        diet_str  = ("🌿 Vegetarian" if st.session_state.get("dietary_type")=="veg"
                     else ("🍗 Non-Vegetarian" if st.session_state.get("dietary_type")=="nonveg"
                           else "🍽️ Flexible"))
        # Show selected cuisine if available
        _c_icon  = st.session_state.get("cuisine_icon", "")
        _c_label = st.session_state.get("cuisine_label", "")
        cuisine_str = f" · {_c_icon} {_c_label}" if _c_label else ""

        st.markdown(
            "<div style='background:rgba(34,197,94,0.08);border:1.5px solid rgba(34,197,94,0.30);"
            "border-radius:14px;padding:16px 22px;margin-bottom:14px;display:flex;"
            "align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px'>"
            "<div><div style='font-size:0.85rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;"
            "color:rgba(34,197,94,0.75);margin-bottom:4px'>&#10003; Active Plan</div>"
            "<div style='font-size:1.05rem;font-weight:600;color:#fff'>"
            + str(plan_days) + "-day plan &middot; " + diet_str + cuisine_str + "</div></div>"
            "<div style='font-size:0.75rem;color:rgba(255,255,255,0.90)'>"
            + str(ud.get("days_per_week",5)) + " days/week &middot; "
            + str(ud.get("months",1)) + " month(s)</div></div>",
            unsafe_allow_html=True
        )

        b1, b2, b3, b4 = st.columns(4)
        with b1:
            if st.button("🏠 Dashboard",   use_container_width=True, key="pdisp_dash"):
                st.switch_page("pages/2_Dashboard.py")
        with b2:
            if st.button("⚡ Workout Plan", use_container_width=True, key="pdisp_wp"):
                st.switch_page("pages/3_Workout_Plan.py")
        with b3:
            if st.button("🥗 Diet Plan",    use_container_width=True, key="pdisp_diet"):
                st.switch_page("pages/4_Diet_Plan.py")
        with b4:
            if st.button("✏️ Edit Profile", use_container_width=True, key="pdisp_edit"):
                st.session_state.edit_profile_mode = True
                st.rerun()

        # Regenerate
        st.markdown(
            "<div style='background:rgba(229,9,20,0.07);border:1.5px solid rgba(229,9,20,0.28);"
            "border-radius:16px;padding:20px 24px;margin-top:16px;position:relative;overflow:hidden'>"
            "<div style='position:absolute;top:0;left:0;right:0;height:2px;"
            "background:linear-gradient(90deg,transparent,#E50914,transparent)'></div>"
            "<div style='font-size:0.85rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;"
            "color:rgba(229,9,20,0.80);margin-bottom:6px'>&#128260; Don&#39;t Like Your Plan?</div>"
            "<div style='font-family:Bebas Neue,sans-serif;font-size:1.4rem;letter-spacing:2px;"
            "color:#fff;margin-bottom:8px'>Regenerate Your Plan</div>"
            "<div style='font-size:0.80rem;color:rgba(255,255,255,0.90);line-height:1.55;margin-bottom:16px'>"
            "Not satisfied? Get a completely new AI-generated plan. Your tracking history is preserved.</div></div>",
            unsafe_allow_html=True
        )
        rc1, rc2 = st.columns([1,1])
        with rc1:
            st.markdown(
                "<div style='background:rgba(12,6,24,0.82);border:1.5px solid rgba(229,9,20,0.30);"
                "border-radius:10px;padding:12px 14px;font-size:1.05rem;color:rgba(255,255,255,0.95);line-height:1.6;"
                "backdrop-filter:blur(20px)'>"
                "&#9888;&#65039; This <b style='color:rgba(229,9,20,0.80)'>permanently deletes</b> your "
                "current plan and AI generates a fresh one.</div>",
                unsafe_allow_html=True
            )
        with rc2:
            if not st.session_state.get("_regen_confirm"):
                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                if st.button("🔄 REGENERATE PLAN", use_container_width=True, key="regen_show_confirm"):
                    st.session_state._regen_confirm = True
                    st.rerun()
            else:
                st.markdown(
                    "<div style='font-size:1.00rem;font-weight:700;color:rgba(229,9,20,0.90);"
                    "text-align:center;margin-bottom:8px;padding-top:4px'>"
                    "&#9888;&#65039; Are you sure? This cannot be undone.</div>",
                    unsafe_allow_html=True
                )
                yc, nc = st.columns(2)
                with yc:
                    if st.button("✅ Yes, Regenerate!", use_container_width=True, key="regen_yes"):
                        for _k in ["workout_plan","structured_days","dietary_type","full_plan_data",
                                   "plan_id","_diet_chosen","force_regen","_db_loaded_dash",
                                   "_notes_loaded","_plan_checked","_regen_confirm",
                                   "_diet_step","_selected_cuisine_id",
                                   "_selected_cuisine_label","_selected_cuisine_icon",
                                   "cuisine_id","cuisine_label","cuisine_icon"]:
                            st.session_state.pop(_k, None)
                        st.session_state.force_regen = True
                        try:
                            from utils.db import delete_active_plan
                            delete_active_plan(uname)
                        except Exception: pass
                        st.toast("🔄 Generating your new plan...", icon="⚡")
                        st.switch_page("pages/3_Workout_Plan.py")
                with nc:
                    if st.button("❌ Cancel", use_container_width=True, key="regen_no"):
                        st.session_state._regen_confirm = False
                        st.rerun()

# ── DAILY REMINDER SETTINGS ──────────────────────────────────────────────────
_show_reminder_section = True
if _show_reminder_section:
    from datetime import datetime as _dt
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    st.markdown(
        "<div style='background:rgba(8,4,2,0.85);border:1.5px solid rgba(229,9,20,0.22);"
        "border-radius:18px;padding:22px 26px;margin-bottom:16px;position:relative;overflow:hidden'>"
        "<div style='position:absolute;top:0;left:0;right:0;height:2px;"
        "background:linear-gradient(90deg,transparent,#E50914,transparent)'></div>"
        "<div style='font-size:0.75rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;"
        "color:rgba(229,9,20,0.75);margin-bottom:8px;display:flex;align-items:center;gap:8px'>"
        "<span style='width:14px;height:1.5px;background:#E50914;display:block'></span>"
        "⏰ Daily Reminder Email</div>"
        "<div style='font-size:0.82rem;color:rgba(255,255,255,0.45);margin-bottom:16px'>"
        "Get a motivational workout reminder email at your chosen time every day via Brevo.</div>",
        unsafe_allow_html=True
    )
    try:
        from utils.db import get_user_setting as _gus, save_user_setting as _sus
        _rem_enabled = _gus(uname, "reminder_enabled") or "0"
        _rem_time_str = _gus(uname, "reminder_time") or "08:00"
        _rem_last_sent = _gus(uname, "reminder_last_sent") or "Never"
    except Exception:
        _rem_enabled   = "0"
        _rem_time_str  = "08:00"
        _rem_last_sent = "Never"

    try:
        _rem_time_val = _dt.strptime(_rem_time_str, "%H:%M").time()
    except Exception:
        import datetime as _dtt
        _rem_time_val = _dtt.time(8, 0)

    rc1, rc2, rc3 = st.columns([2, 3, 2])
    with rc1:
        rem_on = st.toggle(
            "Enable Reminders",
            value=(_rem_enabled == "1"),
            key="rem_toggle",
            help="Sends a daily email to remind you to work out"
        )
    with rc2:
        import datetime as _dtt2
        rem_time = st.time_input(
            "Reminder Time",
            value=_rem_time_val,
            key="rem_time_inp",
            help="What time to send your daily reminder (server time, UTC on HuggingFace)"
        )
    with rc3:
        st.markdown("<div style='padding-top:26px'>", unsafe_allow_html=True)
        if st.button("💾 Save", key="save_reminder", use_container_width=True):
            try:
                _sus(uname, "reminder_enabled", "1" if rem_on else "0")
                _sus(uname, "reminder_time", rem_time.strftime("%H:%M"))
                st.toast("✅ Reminder settings saved!", icon="⏰")
                st.rerun()
            except Exception as _e:
                st.error("Save failed: " + str(_e))
        st.markdown("</div>", unsafe_allow_html=True)

    # Status + test send
    if _rem_enabled == "1":
        st.markdown(
            f"<div style='background:rgba(34,197,94,0.06);border:1px solid rgba(34,197,94,0.22);"
            f"border-radius:10px;padding:10px 14px;margin-top:8px;"
            f"display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px'>"
            f"<div style='font-size:0.80rem;color:rgba(255,255,255,0.55)'>"
            f"📧 Active · Sends at <b style='color:rgba(34,197,94,0.80)'>{_rem_time_str}</b> daily"
            f" &nbsp;·&nbsp; Last sent: <b>{_rem_last_sent}</b></div>"
            f"</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            "<div style='font-size:0.78rem;color:rgba(255,255,255,0.30);margin-top:8px'>"
            "⭕ Reminders disabled — toggle on to activate.</div>",
            unsafe_allow_html=True
        )

    # Manual test button
    tc1, tc2 = st.columns([3, 2])
    with tc2:
        if st.button("📧 Send Test Reminder", key="test_reminder", use_container_width=True):
            try:
                from daily_reminder import send_daily_reminder
                _user_email = ""
                try:
                    from utils.db import get_user_setting as _g2
                    from auth_token import _get_user_by_username
                    _u = _get_user_by_username(uname)
                    _user_email = _u["email"] if _u else ""
                except Exception: pass
                _udata = dict(st.session_state.get("user_data", {}))
                _udata["email"] = _user_email
                _ok, _msg = send_daily_reminder(uname, _udata, st.session_state)
                if _ok:
                    st.toast("✅ Test reminder sent!", icon="📧")
                else:
                    st.error("Failed: " + _msg)
            except Exception as _ex:
                st.error("Error: " + str(_ex))

    st.markdown("</div>", unsafe_allow_html=True)  # close reminder card

else:
    st.markdown(
        "<div style='background:rgba(229,9,20,0.07);border:1px solid rgba(229,9,20,0.22);"
        "border-radius:14px;padding:16px 22px;margin-bottom:14px;text-align:center;"
        "font-size:1.00rem;color:rgba(255,255,255,0.90)'>"
        "No active plan yet. Generate your personalised AI plan below.</div>",
        unsafe_allow_html=True
    )
    b1, b2 = st.columns(2)
    with b1:
        st.markdown("<div class='gen-btn'>", unsafe_allow_html=True)
        if st.button("⚡ GENERATE PLAN", use_container_width=True, key="pdisp_gen"):
            st.switch_page("pages/3_Workout_Plan.py")
        st.markdown("</div>", unsafe_allow_html=True)
    with b2:
        if st.button("✏️ Edit Profile", use_container_width=True, key="pdisp_edit2"):
            st.session_state.edit_profile_mode = True
            st.rerun()