import streamlit as st
import os, sys, json, base64
import streamlit.components.v1 as components
from datetime import date, timedelta
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth_token import logout

st.set_page_config(page_title="Workout Plan | FitPlan Pro", page_icon="⚡", layout="wide", initial_sidebar_state="collapsed")

if not st.session_state.get("logged_in"):
    st.switch_page("app.py")
if "user_data" not in st.session_state:
    st.switch_page("pages/1_Profile.py")

uname   = st.session_state.get("username", "Athlete")
data    = st.session_state.user_data
plan_id = st.session_state.get("plan_id", "")

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="stAppViewContainer"]::before {
  content:'';position:fixed;inset:0;z-index:-1;
  background:url('https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=1800&q=80&auto=format&fit=crop')
    center center/cover no-repeat;
  filter:blur(6px) brightness(0.35) saturate(0.7);
  transform:scale(1.05);
}
[data-testid="stAppViewContainer"] { background:rgba(3,1,0,0.72)!important; }
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow+Condensed:wght@700;800;900&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700&display=swap');
#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stDecoration"],
[data-testid="stSidebarNav"],section[data-testid="stSidebar"]{display:none!important;}
html,body,.stApp{background:#0d0806!important;color:#fff!important;font-family:'DM Sans',sans-serif!important;}
[data-testid="stAppViewContainer"]{
  background:radial-gradient(ellipse at center,rgba(0,0,0,0.40) 0%,rgba(0,0,0,0.75) 100%),
    linear-gradient(180deg,rgba(3,1,0,0.88) 0%,rgba(3,1,0,0.80) 40%,rgba(3,1,0,0.92) 100%) !important;
  backdrop-filter:blur(0px)!important;}
[data-testid="stAppViewContainer"]>section>div.block-container{
  max-width:1100px!important;margin:0 auto!important;padding:0 24px 100px!important;}
[data-testid="stWidgetLabel"],[data-testid="stWidgetLabel"] p,.stCheckbox>label{
  color:#fff!important;font-size:1.05rem!important;font-weight:700!important;
  letter-spacing:2px!important;text-transform:uppercase!important;text-shadow:0 1px 10px rgba(0,0,0,0.95)!important;}
.stTextArea>div>div>textarea{background:rgba(10,5,3,0.70)!important;
  border:2px solid rgba(229,9,20,0.40)!important;color:#fff!important;border-radius:10px!important;}
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"] > button{
  background:rgba(18,4,4,0.82)!important;border:2px solid rgba(229,9,20,0.65)!important;
  color:rgba(255,255,255,0.92)!important;border-radius:9px!important;
  font-family:'DM Sans',sans-serif!important;font-size:0.85rem!important;font-weight:700!important;
  padding:5px 8px!important;height:32px!important;min-height:32px!important;
  white-space:nowrap!important;box-shadow:0 0 8px rgba(229,9,20,0.22)!important;
  transition:all 0.15s ease!important;text-transform:none!important;}
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"] > button:hover{
  background:rgba(229,9,20,0.28)!important;border-color:rgba(229,9,20,0.85)!important;
  color:#fff!important;box-shadow:0 0 18px rgba(229,9,20,0.60)!important;transform:translateY(-1px)!important;}
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"]:last-child > button{
  background:linear-gradient(135deg,#c0000c,#8b0000)!important;
  border-color:rgba(229,9,20,0.80)!important;animation:so-p 2.6s ease-in-out infinite!important;}
@keyframes so-p{0%,100%{box-shadow:0 0 12px rgba(229,9,20,0.55);}50%{box-shadow:0 0 24px rgba(229,9,20,0.88);}}
.stButton>button{background:linear-gradient(135deg,rgba(229,9,20,0.85),rgba(160,0,10,0.90))!important;
  border:2px solid rgba(229,9,20,0.65)!important;color:#fff!important;border-radius:10px!important;
  font-family:'DM Sans',sans-serif!important;font-size:0.85rem!important;font-weight:700!important;
  box-shadow:0 0 16px rgba(229,9,20,0.40)!important;transition:all 0.25s!important;}
.stButton>button:hover{transform:translateY(-2px) scale(1.02)!important;
  box-shadow:0 0 28px rgba(229,9,20,0.65)!important;}
.stTabs [data-baseweb="tab-list"]{background:rgba(0,0,0,0.75)!important;
  border-radius:10px!important;padding:4px!important;gap:3px!important;
  border:1px solid rgba(255,255,255,0.07)!important;}
.stTabs [data-baseweb="tab"]{background:transparent!important;color:rgba(255,255,255,0.90)!important;
  border-radius:7px!important;font-family:'DM Sans',sans-serif!important;font-size:1.05rem!important;
  font-weight:600!important;border:none!important;padding:9px 16px!important;}
.stTabs [aria-selected="true"]{background:linear-gradient(135deg,#E50914,#c0000c)!important;
  color:#fff!important;box-shadow:0 3px 12px rgba(229,9,20,0.40)!important;}
.stTabs [data-baseweb="tab-highlight"],.stTabs [data-baseweb="tab-border"]{display:none!important;}
.nav-wrap{background:rgba(5,2,1,0.97);backdrop-filter:blur(36px);
  border-bottom:1.5px solid rgba(229,9,20,0.22);box-shadow:0 2px 24px rgba(0,0,0,0.65);
  padding:5px 0;margin-bottom:4px;}
.nav-logo{font-family:'Bebas Neue',sans-serif;font-size:1.4rem;letter-spacing:5px;
  color:#E50914;text-shadow:0 0 18px rgba(229,9,20,0.45);line-height:1;}
.hero{background:linear-gradient(135deg,rgba(229,9,20,0.20),rgba(120,0,8,0.12) 40%,rgba(10,5,3,0.55));
  border:2px solid rgba(229,9,20,0.47);border-radius:18px;padding:36px 44px;margin:20px 0 28px;
  position:relative;overflow:hidden;backdrop-filter:blur(28px);}
.hero::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,transparent,#E50914,transparent);}
.hero-title{font-family:'Barlow Condensed',sans-serif;font-size:clamp(2rem,5vw,3.8rem);
  font-weight:900;text-transform:uppercase;color:#fff;line-height:1;margin-bottom:10px;}
.hero-title span{color:#E50914;}
.stat-row{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-bottom:32px;}
.stat{background:rgba(10,6,4,0.85);border:2px solid rgba(229,9,20,0.33);border-radius:12px;
  padding:18px 12px;text-align:center;backdrop-filter:blur(34px);position:relative;overflow:hidden;}
.stat::before{content:'';position:absolute;top:0;left:0;right:0;height:1.5px;
  background:linear-gradient(90deg,transparent,rgba(229,9,20,0.45),transparent);}
.stat-lbl{font-size:0.85rem;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;
  color:rgba(255,255,255,0.90);margin-bottom:8px;}
.stat-val{font-family:'Bebas Neue',sans-serif;font-size:2rem;color:#fff;letter-spacing:1px;}
.stat-unit{font-size:0.85rem;color:rgba(255,255,255,0.90);margin-top:4px;}
.day-card{background:rgba(10,6,4,0.85);border:2px solid rgba(229,9,20,0.30);
  border-radius:16px;padding:28px 32px;backdrop-filter:blur(32px);position:relative;overflow:hidden;}
.day-card::before{content:'';position:absolute;top:0;left:0;right:0;height:1.5px;
  background:linear-gradient(90deg,transparent,rgba(229,9,20,0.40),transparent);}
.sec-title{font-size:0.85rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;
  color:rgba(229,9,20,0.75);margin:20px 0 14px;display:flex;align-items:center;gap:8px;}
.sec-title::before{content:'';width:16px;height:1.5px;background:#E50914;border-radius:1px;}
.sec-title::after{content:'';flex:1;height:1px;background:linear-gradient(90deg,rgba(229,9,20,0.18),transparent);}
.badge{display:inline-flex;flex-direction:column;align-items:center;
  min-width:48px;padding:5px 10px;border-radius:7px;line-height:1.2;}
.badge-num{font-size:1.05rem;font-weight:800;}
.badge-lbl{font-size:0.85rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;opacity:0.70;}
.b-sets{background:rgba(100,160,255,0.13);border:1px solid rgba(100,160,255,0.24);color:#93c5fd;}
.b-reps{background:rgba(100,230,180,0.11);border:1px solid rgba(100,230,180,0.21);color:#6ee7b7;}
.b-rest{background:rgba(255,180,80,0.11);border:1px solid rgba(255,180,80,0.21);color:#fdba74;}
.rest-day{text-align:center;padding:40px;background:rgba(229,9,20,0.06);
  border:2px solid rgba(229,9,20,0.33);border-radius:16px;}
.caution-box{background:rgba(251,191,36,0.08);border:1px solid rgba(251,191,36,0.28);
  border-radius:12px;padding:16px 20px;margin:14px 0;}
.meal-card{background:rgba(10,20,12,0.55);border:1px solid rgba(34,197,94,0.18);
  border-radius:12px;padding:14px 18px;margin-bottom:8px;}
.meal-lbl{font-size:0.85rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;
  color:rgba(34,197,94,0.70);margin-bottom:4px;}
.meal-txt{font-size:0.85rem;color:rgba(255,255,255,0.80);line-height:1.5;}
.stCheckbox{margin-top:4px!important;}
html,body,.stApp,.stMarkdown,p,div,span,label{text-shadow:0 2px 6px rgba(0,0,0,0.98)!important;}
[data-testid="stWidgetLabel"],[data-testid="stWidgetLabel"] p{color:#fff!important;font-size:1.05rem!important;font-weight:700!important;text-shadow:0 2px 8px rgba(0,0,0,0.99)!important;}
.stCheckbox>label,.stCheckbox>label p{color:#fff!important;font-weight:700!important;font-size:1.05rem!important;text-shadow:0 2px 8px rgba(0,0,0,0.99)!important;}
.stTabs [data-baseweb="tab"]{color:rgba(255,255,255,0.92)!important;font-size:0.95rem!important;font-weight:700!important;text-shadow:0 2px 6px rgba(0,0,0,0.95)!important;}
.stExpander details summary{color:#fff!important;font-size:1.05rem!important;font-weight:700!important;text-shadow:0 2px 6px rgba(0,0,0,0.95)!important;}
.stMarkdown p,.stMarkdown li{color:#fff!important;font-size:1.05rem!important;line-height:1.75!important;text-shadow:0 2px 8px rgba(0,0,0,0.99)!important;}
.g-panel{background:rgba(8,4,2,0.88)!important;backdrop-filter:blur(32px)!important;}
</style>
""", unsafe_allow_html=True)

# ── NAV ────────────────────────────────────────────────────────────────────────
st.markdown("<div class='nav-wrap'>", unsafe_allow_html=True)
_n = st.columns([1.8,1,1,1,1,1,1,1,1.3])
with _n[0]: st.markdown("<div class='nav-logo'>⚡ FITPLAN PRO</div>", unsafe_allow_html=True)
with _n[1]:
    if st.button("🏠 Home", key="nb_db", use_container_width=True):
        st.switch_page("pages/2_Dashboard.py")
with _n[2]:
    if st.button("● ⚡ Workout", key="nb_wp", use_container_width=True):
        st.switch_page("pages/3_Workout_Plan.py")
with _n[3]:
    if st.button("🥗 Diet", key="nb_dp", use_container_width=True):
        st.switch_page("pages/4_Diet_Plan.py")
with _n[4]:
    if st.button("🍽️ Meals", key="nb_mp", use_container_width=True):
        try: st.switch_page("pages/11_meal_planner.py")
        except Exception as e: st.warning(f"Upload 11_meal_planner.py: {e}")
with _n[5]:
    if st.button("🤖 AI Coach", key="nb_ai", use_container_width=True):
        try: st.switch_page("pages/5_ai_coach.py")
        except Exception as e: st.warning(f"Upload 5_AI_Coach.py: {e}")
with _n[6]:
    if st.button("🏆 Records", key="nb_rc", use_container_width=True):
        try: st.switch_page("pages/6_records.py")
        except Exception as e: st.warning(f"Upload 6_Records.py: {e}")
with _n[7]:
    if st.button("📸 Photos", key="nb_ph", use_container_width=True):
        try: st.switch_page("pages/7_progress_photos.py")
        except Exception as e: st.warning(f"Upload 7_Progress_Photos.py: {e}")
with _n[8]:
    if st.button("🚪 Sign Out", key="nb_so", use_container_width=True):
        logout(uname)
        for _k in ["logged_in","username","auth_token","user_data","workout_plan",
                   "structured_days","dietary_type","full_plan_data","plan_id","plan_start",
                   "plan_duration","plan_for","force_regen","tracking","_plan_checked",
                   "_db_loaded_dash","_auto_redirect","_diet_chosen","_needs_rerun",
                   "_db_streak","edit_profile_mode","_login_db_err","_notes_loaded"]:
            st.session_state.pop(_k, None)
        st.switch_page("app.py")
st.markdown("</div>", unsafe_allow_html=True)

# ── VARIABLES ─────────────────────────────────────────────────────────────────
sdays        = st.session_state.get("structured_days", [])
dietary_type = st.session_state.get("dietary_type", "veg")

from prompt_builder import calculate_bmi, bmi_category
bmi     = calculate_bmi(data["weight"], data["height"])
bmi_cat = bmi_category(bmi)

# ── PLAN GENERATION ───────────────────────────────────────────────────────────
need_gen = (not sdays) or st.session_state.get("force_regen", False)

if need_gen:
    # ── TWO-STEP DIET PICKER ──────────────────────────────────────────────────
    # Step 1: choose cuisine | Step 2: choose veg / non-veg / flexible
    if "dietary_type" not in st.session_state or st.session_state.get("force_regen"):

        CUISINE_LIST = [
            {"id":"indian",       "label":"Indian",        "icon":"🍛", "desc":"Curry, dal, roti, biryani"},
            {"id":"chinese",      "label":"Chinese",       "icon":"🥡", "desc":"Stir-fry, fried rice, noodles"},
            {"id":"thai",         "label":"Thai",          "icon":"🌿", "desc":"Basil dishes, curry, pad thai"},
            {"id":"japanese",     "label":"Japanese",      "icon":"🍱", "desc":"Teriyaki, sushi, miso, ramen"},
            {"id":"korean",       "label":"Korean",        "icon":"🥘", "desc":"Bibimbap, jjigae, dakgalbi"},
            {"id":"italian",      "label":"Italian",       "icon":"🍝", "desc":"Pasta, risotto, grilled dishes"},
            {"id":"middle_eastern","label":"Middle Eastern","icon":"🧆","desc":"Shawarma, hummus, falafel"},
            {"id":"western",      "label":"Western",       "icon":"🥗", "desc":"Grilled, salads, baked dishes"},
            {"id":"mediterranean","label":"Mediterranean", "icon":"🫒", "desc":"Olive oil, greens, legumes"},
            {"id":"mexican",      "label":"Mexican",       "icon":"🫔", "desc":"Burritos, beans, guac, rice"},
        ]

        # Which step are we on?
        _step = st.session_state.get("_diet_step", 1)

        if _step == 1:
            # ── STEP 1: Cuisine picker ────────────────────────────────────
            st.markdown("""
            <div style='max-width:700px;margin:40px auto 0;text-align:center'>
              <div style='font-size:0.85rem;font-weight:700;letter-spacing:4px;text-transform:uppercase;
                color:rgba(229,9,20,0.80);margin-bottom:8px'>Step 1 of 2</div>
              <div style='font-family:Bebas Neue,sans-serif;font-size:2.4rem;letter-spacing:3px;
                color:#fff;margin-bottom:8px'>Choose Your Cuisine Style</div>
              <div style='font-size:0.85rem;color:rgba(255,255,255,0.70);margin-bottom:28px'>
                Your meals will be prepared in this style every day</div>
            </div>
            """, unsafe_allow_html=True)

            # 5 columns × 2 rows
            rows = [CUISINE_LIST[:5], CUISINE_LIST[5:]]
            for row in rows:
                cols = st.columns(5)
                for col, cuisine in zip(cols, row):
                    with col:
                        st.markdown(
                            f"<div style='background:rgba(10,6,4,0.85);border:2px solid rgba(229,9,20,0.28);"
                            f"border-radius:14px;padding:16px 10px;text-align:center;margin-bottom:6px'>"
                            f"<div style='font-size:2rem;margin-bottom:6px'>{cuisine['icon']}</div>"
                            f"<div style='font-size:0.85rem;font-weight:700;color:#fff;"
                            f"letter-spacing:1px'>{cuisine['label']}</div>"
                            f"<div style='font-size:0.70rem;color:rgba(255,255,255,0.55);"
                            f"margin-top:4px;line-height:1.4'>{cuisine['desc']}</div></div>",
                            unsafe_allow_html=True
                        )
                        if st.button(f"Select", key=f"pick_cuisine_{cuisine['id']}", use_container_width=True):
                            st.session_state._selected_cuisine_id    = cuisine["id"]
                            st.session_state._selected_cuisine_label = cuisine["label"]
                            st.session_state._selected_cuisine_icon  = cuisine["icon"]
                            st.session_state._diet_step = 2
                            st.rerun()
            st.stop()

        else:
            # ── STEP 2: Veg / Non-Veg / Flexible for chosen cuisine ──────
            _cid   = st.session_state.get("_selected_cuisine_id", "indian")
            _clbl  = st.session_state.get("_selected_cuisine_label", "Indian")
            _cicon = st.session_state.get("_selected_cuisine_icon", "🍛")

            st.markdown(
                f"<div style='max-width:620px;margin:40px auto 0;text-align:center'>"
                f"<div style='font-size:0.85rem;font-weight:700;letter-spacing:4px;text-transform:uppercase;"
                f"color:rgba(229,9,20,0.80);margin-bottom:8px'>Step 2 of 2 — {_cicon} {_clbl} Cuisine</div>"
                f"<div style='font-family:Bebas Neue,sans-serif;font-size:2.4rem;letter-spacing:3px;"
                f"color:#fff;margin-bottom:8px'>Choose Your Diet Type</div>"
                f"<div style='font-size:0.85rem;color:rgba(255,255,255,0.70);margin-bottom:28px'>"
                f"All meals will follow {_cicon} {_clbl} style</div></div>",
                unsafe_allow_html=True
            )

            dc1, dc2, dc3 = st.columns(3)
            with dc1:
                st.markdown(
                    f"<div style='background:rgba(5,40,15,0.80);border:2px solid rgba(34,197,94,0.45);"
                    f"border-radius:14px;padding:20px;text-align:center;margin-bottom:10px'>"
                    f"<div style='font-size:2.5rem'>&#127807;</div>"
                    f"<div style='font-family:Bebas Neue,sans-serif;font-size:1.2rem;color:#22c55e;"
                    f"letter-spacing:2px;margin-top:8px'>Vegetarian</div>"
                    f"<div style='font-size:0.85rem;color:rgba(255,255,255,0.70);margin-top:4px'>"
                    f"{_cicon} {_clbl} veg meals</div></div>",
                    unsafe_allow_html=True
                )
                if st.button("Select Veg", use_container_width=True, key="pick_veg"):
                    st.session_state.dietary_type      = "veg"
                    st.session_state.cuisine_label     = _clbl
                    st.session_state.cuisine_icon      = _cicon
                    st.session_state.cuisine_id        = _cid
                    # Also update user_data so AI prompt gets it
                    if "user_data" in st.session_state:
                        st.session_state.user_data["diet_type"]          = "veg"
                        st.session_state.user_data["cuisine_preference"] = f"{_cid}_veg"
                        st.session_state.user_data["cuisine_label"]      = _clbl
                        st.session_state.user_data["cuisine_icon"]       = _cicon
                    st.session_state.pop("force_regen", None)
                    st.session_state.pop("_diet_step", None)
                    st.rerun()
            with dc2:
                st.markdown(
                    f"<div style='background:rgba(50,15,5,0.80);border:2px solid rgba(249,115,22,0.45);"
                    f"border-radius:14px;padding:20px;text-align:center;margin-bottom:10px'>"
                    f"<div style='font-size:2.5rem'>&#127829;</div>"
                    f"<div style='font-family:Bebas Neue,sans-serif;font-size:1.2rem;color:#f97316;"
                    f"letter-spacing:2px;margin-top:8px'>Non-Vegetarian</div>"
                    f"<div style='font-size:0.85rem;color:rgba(255,255,255,0.70);margin-top:4px'>"
                    f"{_cicon} {_clbl} non-veg meals</div></div>",
                    unsafe_allow_html=True
                )
                if st.button("Select Non-Veg", use_container_width=True, key="pick_nveg"):
                    st.session_state.dietary_type      = "nonveg"
                    st.session_state.cuisine_label     = _clbl
                    st.session_state.cuisine_icon      = _cicon
                    st.session_state.cuisine_id        = _cid
                    if "user_data" in st.session_state:
                        st.session_state.user_data["diet_type"]          = "nonveg"
                        st.session_state.user_data["cuisine_preference"] = f"{_cid}_nonveg"
                        st.session_state.user_data["cuisine_label"]      = _clbl
                        st.session_state.user_data["cuisine_icon"]       = _cicon
                    st.session_state.pop("force_regen", None)
                    st.session_state.pop("_diet_step", None)
                    st.rerun()
            with dc3:
                st.markdown(
                    f"<div style='background:rgba(20,35,5,0.80);border:2px solid rgba(250,204,21,0.40);"
                    f"border-radius:14px;padding:20px;text-align:center;margin-bottom:10px'>"
                    f"<div style='font-size:2.5rem'>&#127807;&#127829;</div>"
                    f"<div style='font-family:Bebas Neue,sans-serif;font-size:1.2rem;color:#facc15;"
                    f"letter-spacing:2px;margin-top:8px'>Flexible</div>"
                    f"<div style='font-size:0.85rem;color:rgba(255,255,255,0.70);margin-top:4px'>"
                    f"{_cicon} {_clbl} mixed meals</div></div>",
                    unsafe_allow_html=True
                )
                if st.button("Select Flexible", use_container_width=True, key="pick_both"):
                    st.session_state.dietary_type      = "both"
                    st.session_state.cuisine_label     = _clbl
                    st.session_state.cuisine_icon      = _cicon
                    st.session_state.cuisine_id        = _cid
                    if "user_data" in st.session_state:
                        st.session_state.user_data["diet_type"]          = "both"
                        st.session_state.user_data["cuisine_preference"] = f"{_cid}_both"
                        st.session_state.user_data["cuisine_label"]      = _clbl
                        st.session_state.user_data["cuisine_icon"]       = _cicon
                    st.session_state.pop("force_regen", None)
                    st.session_state.pop("_diet_step", None)
                    st.rerun()

            # Back button
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            if st.button("← Back to Cuisine", key="back_to_cuisine"):
                st.session_state._diet_step = 1
                st.rerun()

        st.stop()

    dietary_type   = st.session_state.get("dietary_type", "veg")
    total_days_gen = data.get("total_days", 28)
    days_per_week  = data.get("days_per_week", 5)
    months_val     = data.get("months", 1)
    if days_per_week and months_val:
        total_days_gen = days_per_week * 4 * months_val

    diet_label = {"veg":"🌿 Vegetarian","nonveg":"🍗 Non-Vegetarian","both":"🌿🍗 Flexible"}.get(dietary_type, "Vegetarian")

    # Show injury/allergy notice
    _injuries      = data.get("injuries", [])
    _cuisine_notes = data.get("cuisine_notes", "")
    if _injuries or _cuisine_notes:
        _parts = []
        if _injuries:
            _parts.append(f"⚠️ Injury adaptations: <b>{', '.join(_injuries)}</b>")
        if _cuisine_notes:
            _parts.append(f"🥗 Allergy/preference: <b>{_cuisine_notes}</b>")
        st.markdown(
            "<div style='max-width:600px;margin:0 auto 16px;background:rgba(251,191,36,0.08);"
            "border:1px solid rgba(251,191,36,0.30);border-radius:12px;padding:12px 18px;"
            "font-size:0.85rem;color:rgba(255,255,255,0.90);text-align:center'>"
            + " &nbsp;·&nbsp; ".join(_parts) +
            "<br><span style='font-size:0.75rem;color:rgba(255,255,255,0.55)'>"
            "The AI will apply these rules to every day of your plan.</span></div>",
            unsafe_allow_html=True
        )

    st.markdown(
        "<div style='max-width:600px;margin:50px auto 0;text-align:center'>"
        "<div style='font-family:Bebas Neue,sans-serif;font-size:2.4rem;letter-spacing:3px;color:#fff;margin-bottom:8px'>Generating Your Plan</div>"
        "<div style='display:inline-block;padding:4px 16px;border-radius:20px;background:rgba(229,9,20,0.12);"
        "border:1px solid rgba(229,9,20,0.30);color:#E50914;margin-bottom:12px;font-size:0.80rem;font-weight:700'>"
        + diet_label + "</div>"
        "<div style='font-size:1.00rem;color:rgba(255,255,255,0.90);margin-bottom:24px'>"
        "Building your <b style='color:#E50914'>" + str(total_days_gen) + "-day</b> "
        "(" + str(days_per_week) + " days/week &times; " + str(months_val) + " month) plan &#9889;</div>"
        "</div>",
        unsafe_allow_html=True
    )

    prog = st.progress(0, text="Starting AI generation...")
    sph  = st.empty()

    def _gen_cb(cn, tc, dd, td, status=None):
        pct = min(int((dd / max(td, 1)) * 100), 99)
        prog.progress(pct, text=status or f"Generating {td}-day plan...")
        sph.markdown(
            f"<div style='text-align:center;font-size:0.75rem;color:rgba(255,255,255,0.90)'>{pct}% complete</div>",
            unsafe_allow_html=True
        )

    try:
        from model_api import query_model_chunked
        wplan, new_sdays, _b, _bc = query_model_chunked(
            name=data["name"], gender=data["gender"],
            height=data["height"], weight=data["weight"],
            goal=data["goal"], fitness_level=data["level"],
            equipment=data.get("equipment", []),
            days_per_week=days_per_week, months=months_val,
            dietary_type=dietary_type,
            progress_callback=_gen_cb,
            injuries           = data.get("injuries", []),
            cuisine_preference = data.get("cuisine_preference", ""),
            cuisine_label      = data.get("cuisine_label", ""),
            cuisine_icon       = data.get("cuisine_icon", ""),
            cuisine_notes      = data.get("cuisine_notes", ""),
        )
        prog.progress(100, text="✅ Plan Ready!")
        sph.empty()

        for _i, _d in enumerate(new_sdays):
            _d["day"] = _i + 1

        st.session_state.structured_days = new_sdays
        st.session_state.full_plan_data  = new_sdays
        st.session_state.workout_plan    = wplan
        st.session_state.plan_for        = uname
        st.session_state.dietary_type    = dietary_type
        st.session_state.pop("force_regen", None)
        st.session_state.pop("_plan_checked", None)
        st.session_state.pop("_db_loaded_dash", None)

        if "plan_start" not in st.session_state:
            st.session_state.plan_start = date.today().isoformat()

        # ── Save to DB — errors shown so nothing fails silently ───────────────
        _saved_pid = None
        _db_err    = None
        try:
            from utils.db import save_plan as _sp
            _saved_pid = _sp(uname, dietary_type, total_days_gen, new_sdays,
                             cuisine_type=data.get("cuisine_preference", ""))
        except Exception as _e:
            _db_err = str(_e)

        if _saved_pid:
            st.session_state.plan_id = _saved_pid
        elif _db_err:
            st.warning(f"⚠️ Plan generated but DB save failed: {_db_err} — your plan is active this session but may not persist after re-login.")

        prog.empty()
        sph.empty()
        st.markdown(
            "<div style='max-width:500px;margin:16px auto;text-align:center;"
            "background:rgba(34,197,94,0.12);border:1.5px solid rgba(34,197,94,0.40);"
            "border-radius:14px;padding:18px 24px;backdrop-filter:blur(10px)'>"
            "<div style='font-size:1.8rem;margin-bottom:8px'>🎉</div>"
            "<div style='font-family:Bebas Neue,sans-serif;font-size:1.6rem;color:#22c55e;letter-spacing:2px'>Plan Ready!</div>"
            "<div style='font-size:1.00rem;color:rgba(255,255,255,0.90);margin-top:6px'>"
            "Your " + str(len(new_sdays)) + "-day plan has been generated. Loading now...</div>"
            "</div>",
            unsafe_allow_html=True
        )
        st.rerun()

    except Exception as _gen_err:
        try: prog.empty()
        except Exception: pass
        try: sph.empty()
        except Exception: pass
        _raw_err = str(_gen_err)
        if "rate limit" in _raw_err.lower() or "429" in _raw_err:
            _err_msg = "The AI service is busy. Please wait 60 seconds and try again."
        elif "api key" in _raw_err.lower() or "401" in _raw_err:
            _err_msg = "API key issue — check your GROQ_API_KEY in HuggingFace Secrets."
        elif "connect" in _raw_err.lower() or "timeout" in _raw_err.lower():
            _err_msg = "Could not reach the AI service. Check your connection and retry."
        else:
            _err_msg = f"Plan generation failed: {_raw_err[:200]}"
        st.markdown(
            "<div style='max-width:560px;margin:20px auto;background:rgba(229,9,20,0.10);"
            "border:1px solid rgba(229,9,20,0.30);border-radius:14px;padding:24px 28px'>"
            "<div style='font-size:1rem;font-weight:700;color:#ff6b6b;margin-bottom:8px'>&#9888; Generation Failed</div>"
            "<div style='font-size:1.00rem;color:rgba(255,255,255,0.90);line-height:1.7'>" + _err_msg + "</div>"
            "</div>",
            unsafe_allow_html=True
        )
        _c1, _c2 = st.columns(2)
        with _c1:
            if st.button("&#8592; Back to Profile", key="gen_fail_prof"):
                st.switch_page("pages/1_Profile.py")
        with _c2:
            if st.button("&#8635; Try Again", key="gen_fail_retry"):
                st.session_state.pop("structured_days", None)
                st.rerun()
        st.stop()

# ── HERO ──────────────────────────────────────────────────────────────────────
total_days = len(sdays)
st.markdown(f"""
<div class='hero'>
  <div style='font-size:0.85rem;font-weight:700;letter-spacing:4px;text-transform:uppercase;
    color:rgba(229,9,20,0.75);margin-bottom:10px'>⚡ Personalised AI Fitness Plan</div>
  <div class='hero-title'>{data['name'].upper()}'S <span>{total_days}-DAY PLAN</span></div>
  <div style='font-size:0.85rem;color:rgba(255,255,255,0.90);display:flex;gap:12px;flex-wrap:wrap'>
    <span>🎯 {data['goal']}</span><span>·</span>
    <span>📊 {data['level']}</span><span>·</span>
    <span>⚖️ BMI {bmi:.1f} · {bmi_cat}</span><span>·</span>
    <span>{'🌿 Vegetarian' if dietary_type=='veg' else '🍗 Non-Veg'}</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── STAT CARDS ────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class='stat-row'>
  <div class='stat'><div class='stat-lbl'>🎂 Age</div><div class='stat-val'>{data['age']}</div><div class='stat-unit'>years</div></div>
  <div class='stat'><div class='stat-lbl'>📏 Height</div><div class='stat-val'>{data['height']}</div><div class='stat-unit'>cm</div></div>
  <div class='stat'><div class='stat-lbl'>⚖️ Weight</div><div class='stat-val'>{data['weight']}</div><div class='stat-unit'>kg</div></div>
  <div class='stat'><div class='stat-lbl'>📈 BMI</div><div class='stat-val'>{bmi:.1f}</div><div class='stat-unit'>{bmi_cat}</div></div>
  <div class='stat'><div class='stat-lbl'>🎯 Goal</div><div class='stat-val' style='font-size:1.1rem;line-height:1.2'>{data['goal']}</div><div class='stat-unit'>{data['level']}</div></div>
</div>
""", unsafe_allow_html=True)


# ── PLAN PROGRESS BAR ─────────────────────────────────────────────────────────
try:
    _plan_start_dt2 = date.fromisoformat(st.session_state.get("plan_start", date.today().isoformat()))
    _day_offset2    = (date.today() - _plan_start_dt2).days + 1
    _current_day    = max(1, min(_day_offset2, total_days))
    _pct_done       = int(_current_day / max(total_days, 1) * 100)
    _rest_count     = sum(1 for d in sdays if d.get("is_rest_day"))
    _work_count     = total_days - _rest_count
    _done_count     = sum(1 for d in sdays
                          if st.session_state.get(f"ex_d{d.get('day',0)}_done_all", False)
                          or st.session_state.get(f"day_done_{d.get('day',0)}", False))
    _pbar_col = "#22c55e" if _pct_done >= 75 else "#fbbf24" if _pct_done >= 40 else "#E50914"
    st.markdown(
        f"<div style='background:rgba(8,4,2,0.82);border:1px solid rgba(255,255,255,0.08);"
        f"border-radius:12px;padding:12px 18px;margin-bottom:12px'>"
        f"<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:7px'>"
        f"<div style='font-size:0.72rem;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;"
        f"color:rgba(255,255,255,0.55)'>📅 Plan Progress</div>"
        f"<div style='font-size:0.80rem;font-weight:700;color:{_pbar_col}'>"
        f"Day {_current_day} of {total_days} &nbsp;·&nbsp; {_pct_done}% complete</div>"
        f"</div>"
        f"<div style='height:7px;background:rgba(255,255,255,0.08);border-radius:4px;overflow:hidden'>"
        f"<div style='height:100%;width:{_pct_done}%;"
        f"background:linear-gradient(90deg,#E50914,{_pbar_col});border-radius:4px;"
        f"transition:width 0.5s ease'></div></div>"
        f"<div style='display:flex;justify-content:space-between;margin-top:6px;"
        f"font-size:0.68rem;color:rgba(255,255,255,0.35)'>"
        f"<span>🏋️ {_work_count} workout days</span>"
        f"<span>😴 {_rest_count} rest days</span>"
        f"<span>✅ {total_days - _current_day} days remaining</span>"
        f"</div></div>",
        unsafe_allow_html=True
    )
except Exception:
    pass

# ── SAFETY + PDF ──────────────────────────────────────────────────────────────
with st.expander("⚠️ Safety Cautions — Read Before Starting", expanded=False):
    st.markdown("""
    <div class='caution-box'>
      <div style='font-size:0.85rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:rgba(251,191,36,0.80);margin-bottom:12px'>⚠ WORKOUT SAFETY REMINDERS</div>
      <div style='display:grid;grid-template-columns:1fr 1fr;gap:8px'>
        <div style='font-size:1.00rem;color:rgba(255,255,255,0.72);padding:6px 0;border-bottom:1px solid rgba(255,255,255,0.05)'>🧘 Maintain correct posture throughout</div>
        <div style='font-size:1.00rem;color:rgba(255,255,255,0.72);padding:6px 0;border-bottom:1px solid rgba(255,255,255,0.05)'>💧 Stay hydrated — drink water regularly</div>
        <div style='font-size:1.00rem;color:rgba(255,255,255,0.72);padding:6px 0;border-bottom:1px solid rgba(255,255,255,0.05)'>🔥 Always warm up before starting</div>
        <div style='font-size:1.00rem;color:rgba(255,255,255,0.72);padding:6px 0;border-bottom:1px solid rgba(255,255,255,0.05)'>🛑 Stop immediately if pain occurs</div>
        <div style='font-size:1.00rem;color:rgba(255,255,255,0.72);padding:6px 0;border-bottom:1px solid rgba(255,255,255,0.05)'>😮‍💨 Breathe steadily — never hold breath</div>
        <div style='font-size:1.00rem;color:rgba(255,255,255,0.72);padding:6px 0'>⚖️ Use appropriate resistance level</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

with st.expander("📄 Export Plan as PDF", expanded=False):
    pdf_lines = [f"<h1>{data.get('name','').upper()}'S {total_days}-DAY FITNESS PLAN</h1>",
                 f"<p><b>Goal:</b> {data.get('goal','')} | <b>Level:</b> {data.get('level','')} | <b>Diet:</b> {'Veg' if dietary_type=='veg' else 'Non-Veg'}</p><hr>"]
    for d in sdays:
        dn = d.get('day',1); mg = d.get('muscle_group','Full Body')
        if d.get('is_rest_day'):
            pdf_lines.append(f"<h2>Day {dn} — Rest Day</h2><hr>")
        else:
            pdf_lines.append(f"<h2>Day {dn} — {mg}</h2><ul>")
            for ex in d.get('workout',[]):
                pdf_lines.append(f"<li><b>{ex.get('name','')}</b> — {ex.get('sets',3)}×{ex.get('reps','12')} (rest {ex.get('rest','60s')})</li>")
            pdf_lines.append("</ul><hr>")
    full_html = ("<html><head><style>body{font-family:Arial;font-size:13px;max-width:800px;margin:0 auto;padding:20px}"
                 "h1{color:#c0000c}h2{border-bottom:1px solid #ddd;padding-bottom:4px}</style></head><body>"
                 + "".join(pdf_lines) + "</body></html>")
    b64 = base64.b64encode(full_html.encode()).decode()
    st.markdown(f"<a href='data:text/html;base64,{b64}' download='fitplan_{data.get('name','plan').lower()}.html' "
                f"style='display:inline-block;background:#E50914;color:#fff;padding:10px 24px;"
                f"border-radius:10px;font-weight:700;text-decoration:none'>📄 Download Plan (Open → Ctrl+P → Save PDF)</a>",
                unsafe_allow_html=True)

# ── PROGRESS HEATMAP ─────────────────────────────────────────────────────────
st.markdown("<div class='sec-title'>Your Workout Schedule</div>", unsafe_allow_html=True)

completed_days = []
for _d in sdays:
    _dn   = _d.get("day", 0)
    _ex   = _d.get("workout", [])
    _rest = _d.get("is_rest_day", False)
    if _rest:
        completed_days.append("rest")
    elif all(st.session_state.get(f"ex_d{_dn}_{_i}", False) for _i in range(len(_ex))) and len(_ex) > 0:
        completed_days.append("done")
    else:
        try:
            from utils.db import get_progress
            _prog = get_progress(uname, plan_id, _dn)
            if _prog.get("day_completed"):
                completed_days.append("done")
                for _i in range(len(_ex)): st.session_state[f"ex_d{_dn}_{_i}"] = True
            else: completed_days.append("pending")
        except Exception: completed_days.append("pending")

done_count = completed_days.count("done")
pct_done   = int(done_count / max(total_days, 1) * 100)

heatmap_cells = ""
for _i, _status in enumerate(completed_days):
    _dn2 = sdays[_i].get("day", _i+1)
    if _status=="done":   col="#22c55e"; bg="rgba(34,197,94,0.25)";   brd="rgba(34,197,94,0.55)"
    elif _status=="rest": col="#94a3b8"; bg="rgba(148,163,184,0.15)"; brd="rgba(148,163,184,0.30)"
    else:                 col="rgba(255,255,255,0.25)"; bg="rgba(255,255,255,0.05)"; brd="rgba(255,255,255,0.10)"
    heatmap_cells += (f"<div title='Day {_dn2}' style='width:28px;height:28px;border-radius:5px;"
                      f"background:{bg};border:1.5px solid {brd};display:flex;align-items:center;"
                      f"justify-content:center;font-size:0.85rem;font-weight:700;color:{col}'>{_dn2}</div>")

st.markdown(f"""
<div style='background:rgba(10,6,4,0.85);border:1px solid rgba(229,9,20,0.15);
  border-radius:16px;padding:20px 24px;margin-bottom:24px;position:relative;overflow:hidden'>
  <div style='position:absolute;top:0;left:0;right:0;height:1.5px;
    background:linear-gradient(90deg,transparent,rgba(229,9,20,0.40),transparent)'></div>
  <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:14px'>
    <span style='font-size:0.85rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:rgba(229,9,20,0.75)'>
      📊 Progress — {done_count}/{total_days} days completed</span>
    <span style='font-family:Bebas Neue,sans-serif;font-size:1.6rem;color:#E50914'>{pct_done}%</span>
  </div>
  <div style='height:8px;background:rgba(0,0,0,0.75);border-radius:4px;overflow:hidden;margin-bottom:14px'>
    <div style='height:100%;width:{pct_done}%;background:linear-gradient(90deg,#E50914,#ff4444);border-radius:4px'></div>
  </div>
  <div style='display:flex;flex-wrap:wrap;gap:4px'>{heatmap_cells}</div>
  <div style='display:flex;gap:16px;margin-top:10px;font-size:1.00rem;color:rgba(255,255,255,0.90)'>
    <span><span style='color:#22c55e'>■</span> Completed</span>
    <span><span style='color:#94a3b8'>■</span> Rest Day</span>
    <span><span style='color:rgba(255,255,255,0.90)'>■</span> Pending</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── SOCIAL SHARE ─────────────────────────────────────────────────────────────
with st.expander("🎉 Share Your Progress", expanded=False):
    streak_val = st.session_state.get("_db_streak", 0)
    st.markdown(f"""
<div style='background:linear-gradient(135deg,#0d0806,#1a0a0a);border:2px solid rgba(229,9,20,0.50);
  border-radius:16px;padding:28px 32px;text-align:center;max-width:380px;margin:0 auto;font-family:Bebas Neue,sans-serif'>
  <div style='font-size:0.85rem;letter-spacing:4px;color:rgba(229,9,20,0.70);margin-bottom:6px'>⚡ FITPLAN PRO</div>
  <div style='font-size:2.2rem;color:#fff;letter-spacing:2px;margin-bottom:4px'>{uname.upper()}</div>
  <div style='font-size:3.5rem;color:#E50914;letter-spacing:2px;line-height:1'>{streak_val}</div>
  <div style='font-size:0.85rem;letter-spacing:3px;color:rgba(255,255,255,0.90);margin-bottom:10px'>DAY STREAK</div>
  <div style='display:flex;justify-content:center;gap:20px'>
    <div><div style='font-size:1.4rem;color:#fff'>{done_count}</div>
         <div style='font-size:0.85rem;letter-spacing:2px;color:rgba(255,255,255,0.90)'>DAYS DONE</div></div>
    <div style='color:rgba(255,255,255,0.90)'>|</div>
    <div><div style='font-size:1.4rem;color:#fff'>{pct_done}%</div>
         <div style='font-size:0.85rem;letter-spacing:2px;color:rgba(255,255,255,0.90)'>COMPLETE</div></div>
    <div style='color:rgba(255,255,255,0.90)'>|</div>
    <div><div style='font-size:1.4rem;color:#fff'>{total_days}</div>
         <div style='font-size:0.85rem;letter-spacing:2px;color:rgba(255,255,255,0.90)'>TOTAL DAYS</div></div>
  </div>
</div>""", unsafe_allow_html=True)
    st.caption("Screenshot this and share on WhatsApp or Instagram! 📱")

# ── WATER INTAKE TRACKER ──────────────────────────────────────────────────────
_water_date  = date.today().isoformat()
_water_goal  = 8   # glasses per day
_water_key   = f"water_glasses_{_water_date}"

# Load from DB once per day
if _water_key not in st.session_state:
    try:
        from utils.db import get_water
        st.session_state[_water_key] = int(get_water(uname, _water_date) or 0)
    except Exception:
        st.session_state[_water_key] = 0

_glasses = st.session_state.get(_water_key, 0)
_pct     = min(100, int(_glasses / _water_goal * 100))

# SVG ring constants
_R       = 54
_CIRC    = round(3.14159 * 2 * _R, 1)
_DASH    = round(_CIRC * _pct / 100, 1)
_GAP     = round(_CIRC - _DASH, 1)

# Color: blue → green as you fill up
_ring_color = (
    "#22c55e" if _glasses >= _water_goal else
    "#06b6d4" if _glasses >= 5 else
    "#3b82f6"
)

_water_msg = (
    "🎉 Goal reached! Great job staying hydrated!" if _glasses >= _water_goal else
    f"💧 {_water_goal - _glasses} more glass{'es' if _water_goal - _glasses > 1 else ''} to go!" if _glasses > 0 else
    "💧 Start hydrating — drink your first glass!"
)

st.markdown(f"""
<style>
@keyframes wring{{from{{stroke-dashoffset:{_CIRC}}}to{{stroke-dashoffset:{_CIRC - _DASH}}}}}
@keyframes wdrop{{0%{{transform:translateY(-8px);opacity:0}}60%{{transform:translateY(2px);opacity:1}}100%{{transform:translateY(0);opacity:1}}}}
.water-card{{
  background:linear-gradient(135deg,rgba(3,12,22,0.96),rgba(2,8,18,0.94));
  border:1.5px solid rgba(6,182,212,0.22);border-radius:20px;
  padding:20px 24px;margin-bottom:14px;position:relative;overflow:hidden;
}}
.water-card::before{{content:'';position:absolute;top:0;left:0;right:0;height:1.5px;
  background:linear-gradient(90deg,transparent,rgba(6,182,212,0.70),rgba(34,197,94,0.50),rgba(6,182,212,0.70),transparent);}}
.water-inner{{display:flex;align-items:center;gap:24px;}}
.water-ring-wrap{{position:relative;width:130px;height:130px;flex-shrink:0;}}
.water-ring-wrap svg{{transform:rotate(-90deg);}}
.ring-track{{fill:none;stroke:rgba(6,182,212,0.12);stroke-width:9;}}
.ring-fill{{fill:none;stroke-width:9;stroke-linecap:round;
  stroke-dasharray:{_DASH} {_GAP};
  stroke-dashoffset:0;
  animation:wring 1.0s cubic-bezier(0.34,1.56,0.64,1) both;}}
.ring-center{{position:absolute;inset:0;display:flex;flex-direction:column;
  align-items:center;justify-content:center;}}
.ring-num{{font-family:'Bebas Neue',sans-serif;font-size:2.4rem;color:#fff;line-height:1;}}
.ring-sub{{font-size:0.60rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;
  color:rgba(255,255,255,0.35);margin-top:1px;}}
.water-info{{flex:1;}}
.water-title{{font-size:0.78rem;font-weight:800;letter-spacing:3px;text-transform:uppercase;
  color:{_ring_color};margin-bottom:4px;}}
.water-msg{{font-size:0.82rem;color:rgba(255,255,255,0.55);margin-bottom:14px;line-height:1.4;}}
.water-glasses{{display:flex;flex-wrap:wrap;gap:7px;margin-bottom:14px;}}
.wg{{width:30px;height:38px;border-radius:4px 4px 6px 6px;cursor:default;
  display:flex;align-items:center;justify-content:center;font-size:1.05rem;
  border:1.5px solid rgba(6,182,212,0.18);background:rgba(6,182,212,0.05);
  transition:all 0.18s;}}
.wg.done{{background:rgba(6,182,212,0.22);border-color:{_ring_color};
  animation:wdrop 0.35s ease;}}
.wg.goal-done{{background:rgba(34,197,94,0.20);border-color:#22c55e;}}
.water-btns{{display:flex;gap:8px;}}
</style>
<div class='water-card'>
  <div class='water-inner'>
    <div class='water-ring-wrap'>
      <svg width='130' height='130' viewBox='0 0 130 130'>
        <circle class='ring-track' cx='65' cy='65' r='{_R}'/>
        <circle class='ring-fill' cx='65' cy='65' r='{_R}' stroke='{_ring_color}'/>
      </svg>
      <div class='ring-center'>
        <div class='ring-num'>{_glasses}</div>
        <div class='ring-sub'>of {_water_goal}</div>
      </div>
    </div>
    <div class='water-info'>
      <div class='water-title'>💧 Water Intake</div>
      <div class='water-msg'>{_water_msg}</div>
      <div class='water-glasses'>
        {''.join([
            f"<div class='wg {'goal-done' if i < _glasses and _glasses >= _water_goal else 'done' if i < _glasses else ''}'>"
            f"{'💧' if i < _glasses else '○'}</div>"
            for i in range(_water_goal)
        ])}
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# Buttons row — add / remove / reset
_wb1, _wb2, _wb3, _wb4 = st.columns([2, 2, 2, 4])
with _wb1:
    if st.button("＋ Add Glass", key="water_add", use_container_width=True,
                 disabled=(_glasses >= 12)):
        st.session_state[_water_key] = min(12, _glasses + 1)
        try:
            from utils.db import save_water
            save_water(uname, _water_date, st.session_state[_water_key])
        except Exception:
            pass
        st.rerun()
with _wb2:
    if st.button("－ Remove", key="water_remove", use_container_width=True,
                 disabled=(_glasses <= 0)):
        st.session_state[_water_key] = max(0, _glasses - 1)
        try:
            from utils.db import save_water
            save_water(uname, _water_date, st.session_state[_water_key])
        except Exception:
            pass
        st.rerun()
with _wb3:
    if st.button("↺ Reset", key="water_reset", use_container_width=True,
                 disabled=(_glasses == 0)):
        st.session_state[_water_key] = 0
        try:
            from utils.db import save_water
            save_water(uname, _water_date, 0)
        except Exception:
            pass
        st.rerun()
with _wb4:
    _pct_txt = f"{_pct}% of daily goal"
    st.markdown(
        f"<div style='display:flex;align-items:center;height:38px;"
        f"font-size:0.80rem;color:rgba(255,255,255,0.35);padding-left:8px'>"
        f"🗓️ Today · {_pct_txt}</div>",
        unsafe_allow_html=True
    )

st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

# ── PRE-LOAD WORKOUT NOTES ────────────────────────────────────────────────────
if not st.session_state.get("_notes_loaded") and plan_id:
    try:
        from utils.db import get_workout_notes
        for _dn_pre in range(1, min(6, len(sdays)+1)):
            _nk = f"notes_loaded_d{_dn_pre}"
            if not st.session_state.get(_nk):
                for _eidx, _note in get_workout_notes(uname, plan_id, _dn_pre).items():
                    st.session_state[f"note_d{_dn_pre}_e{_eidx}"] = _note
                st.session_state[_nk] = True
        st.session_state._notes_loaded = True
    except Exception: pass



# ── WORKOUT COMPLETION CELEBRATION ────────────────────────────────────────────
if st.session_state.get("_show_celebration"):
    _celeb_dn = st.session_state.pop("_show_celebration")
    # Custom full-screen confetti + trophy celebration using HTML component
    import streamlit.components.v1 as _cv1
    _cv1.html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');
#celeb-overlay{
  position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:99999;
  background:rgba(0,0,0,0.88);display:flex;align-items:center;justify-content:center;
  animation:fadeIn 0.35s ease;
}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}
#celeb-card{
  background:linear-gradient(135deg,rgba(6,28,12,0.97),rgba(4,18,8,0.98));
  border:2.5px solid rgba(34,197,94,0.60);border-radius:24px;
  padding:40px 52px;text-align:center;max-width:480px;width:90%;
  position:relative;overflow:hidden;
  box-shadow:0 0 80px rgba(34,197,94,0.30),0 30px 80px rgba(0,0,0,0.80);
  animation:slideUp 0.45s cubic-bezier(0.34,1.56,0.64,1);
}
@keyframes slideUp{from{opacity:0;transform:translateY(40px) scale(0.90)}to{opacity:1;transform:translateY(0) scale(1)}}
#celeb-card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;
  background:linear-gradient(90deg,transparent,#22c55e,#4ade80,#22c55e,transparent);}
#celeb-card::after{content:'';position:absolute;bottom:0;left:0;right:0;height:1px;
  background:linear-gradient(90deg,transparent,rgba(34,197,94,0.40),transparent);}
.trophy{font-size:5rem;animation:trophyBounce 0.7s cubic-bezier(0.34,1.56,0.64,1) 0.2s both;}
@keyframes trophyBounce{from{transform:scale(0) rotate(-20deg)}to{transform:scale(1) rotate(0deg)}}
.headline{font-family:'Bebas Neue',sans-serif;font-size:3rem;letter-spacing:4px;
  color:#22c55e;margin:12px 0 6px;text-shadow:0 0 40px rgba(34,197,94,0.60);
  animation:glowPulse 2s ease-in-out infinite;}
@keyframes glowPulse{0%,100%{text-shadow:0 0 20px rgba(34,197,94,0.60)}50%{text-shadow:0 0 50px rgba(34,197,94,0.90),0 0 80px rgba(34,197,94,0.40)}}
.subline{font-size:1.1rem;color:rgba(255,255,255,0.80);margin-bottom:6px;line-height:1.5;}
.stats-row{display:flex;justify-content:center;gap:20px;margin:18px 0;flex-wrap:wrap;}
.stat-chip{background:rgba(34,197,94,0.10);border:1px solid rgba(34,197,94,0.30);
  border-radius:20px;padding:6px 16px;font-size:0.85rem;color:rgba(34,197,94,0.90);}
.dismiss-btn{
  background:linear-gradient(135deg,#22c55e,#16a34a);border:none;color:#fff;
  font-size:1rem;font-weight:700;padding:12px 32px;border-radius:12px;
  cursor:pointer;margin-top:18px;letter-spacing:1px;
  box-shadow:0 4px 20px rgba(34,197,94,0.40);
  transition:all 0.20s;}
.dismiss-btn:hover{transform:translateY(-2px);box-shadow:0 8px 30px rgba(34,197,94,0.60);}

/* Confetti */
.confetti-piece{position:fixed;width:10px;height:10px;top:-10px;animation:confettiFall linear infinite;}
@keyframes confettiFall{
  0%{top:-10px;transform:rotate(0deg) translateX(0);}
  100%{top:110vh;transform:rotate(720deg) translateX(var(--drift));}}
</style>
<div id="celeb-overlay">
  <div id="celeb-card">
    <div class="trophy">🏆</div>
    <div class="headline">DAY COMPLETE!</div>
    <div class="subline">Every rep. Every set. <strong style="color:#4ade80">Absolutely crushed it.</strong></div>
    <div class="subline" style="font-size:0.90rem;color:rgba(255,255,255,0.50);margin-top:4px">
      Rest up and come back stronger tomorrow 💪
    </div>
    <div class="stats-row">
      <div class="stat-chip">🔥 Workout Done</div>
      <div class="stat-chip">⚡ Streak Active</div>
      <div class="stat-chip">💎 Keep it up</div>
    </div>
    <button class="dismiss-btn" onclick="document.getElementById('celeb-overlay').style.display='none'">
      🎯 Let's Go!
    </button>
  </div>
</div>
<script>
// Confetti cannon
var colors = ['#22c55e','#4ade80','#86efac','#fbbf24','#E50914','#fff','#60a5fa'];
var container = document.body;
for(var i=0;i<80;i++){
  var piece = document.createElement('div');
  piece.className = 'confetti-piece';
  var left = Math.random()*100;
  var size = 6 + Math.random()*10;
  var delay = Math.random()*3;
  var dur   = 2.5 + Math.random()*2;
  var drift = (Math.random()-0.5)*200;
  var color = colors[Math.floor(Math.random()*colors.length)];
  var shape = Math.random()>0.5 ? '50%' : '0%';
  piece.style.cssText = [
    'left:'+left+'vw',
    'width:'+size+'px','height:'+size+'px',
    'animation-delay:'+delay+'s',
    'animation-duration:'+dur+'s',
    '--drift:'+drift+'px',
    'background:'+color,
    'border-radius:'+shape,
    'opacity:'+(0.7+Math.random()*0.3),
    'z-index:99998',
  ].join(';');
  document.body.appendChild(piece);
}
// Auto dismiss after 6 seconds
setTimeout(function(){
  var ov = document.getElementById('celeb-overlay');
  if(ov) ov.style.display='none';
  // Remove confetti
  document.querySelectorAll('.confetti-piece').forEach(function(p){p.remove();});
}, 6000);
</script>
""", height=0)

# ── MUSIC PLAYER ──────────────────────────────────────────────────────────────────────────────
# Genre switching is 100% in-iframe JS — no Streamlit rerun, no white boxes.
# The Spotify embed src is swapped directly by JS when user clicks a chip.
import streamlit.components.v1 as _cmp
import json as _json

_PL_DATA = [{'key': '🔥 Beast Mode', 'id': '37i9dQZF1DX76Wlfdnj7AP', 'desc': 'Hard-hitting gym tracks', 'color': '#ff4500', 'emoji': '🔥', 'label': 'BEAST MODE'}, {'key': '💪 Workout Hits', 'id': '4mk1o6g93vy9e9DDOaapX3', 'desc': 'Top workout bangers', 'color': '#E50914', 'emoji': '💪', 'label': 'WORKOUT HITS'}, {'key': '🎤 Hip-Hop', 'id': '37i9dQZF1DX9oh43oAzkyx', 'desc': 'Hip-hop motivation', 'color': '#a855f7', 'emoji': '🎤', 'label': 'HIP-HOP'}, {'key': '⚡ EDM', 'id': '37i9dQZF1DXdURFimg6Blm', 'desc': 'High energy EDM', 'color': '#06b6d4', 'emoji': '⚡', 'label': 'EDM'}, {'key': '🎸 Rock', 'id': '3W6QwXZyaiG8qRkaie63Cr', 'desc': 'Rock & metal energy', 'color': '#f59e0b', 'emoji': '🎸', 'label': 'ROCK'}, {'key': '🎵 Bollywood', 'id': '37i9dQZF1DWXtlo6ENS92N', 'desc': 'Bollywood pump-up', 'color': '#ec4899', 'emoji': '🎵', 'label': 'BOLLYWOOD'}, {'key': '🎶 Tollywood', 'id': '37i9dQZF1DX4H5837Y8I1n', 'desc': 'Telugu beats & energy', 'color': '#f97316', 'emoji': '🎶', 'label': 'TOLLYWOOD'}, {'key': '🎬 Hollywood', 'id': '37i9dQZF1DX0XUfTFmNBRM', 'desc': 'Epic movie soundtracks', 'color': '#3b82f6', 'emoji': '🎬', 'label': 'HOLLYWOOD'}, {'key': '🧘 Chill Recovery', 'id': '37i9dQZF1DX9s3cYAeKW5d', 'desc': 'Calm down & recover', 'color': '#22c55e', 'emoji': '🧘', 'label': 'CHILL RECOVERY'}]

_genre     = st.session_state.get('music_genre_sel', _PL_DATA[0]['key'])
# Bake current active genre into the HTML so chip renders correctly on load
_pl_json   = _json.dumps(_PL_DATA)
_genre_js  = _json.dumps(_genre)

_base_html = '<!DOCTYPE html>\n<html>\n<head>\n<meta charset=\'UTF-8\'>\n<link href=\'https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@400;600;700;800&display=swap\' rel=\'stylesheet\'>\n<style>\n*{box-sizing:border-box;margin:0;padding:0;}\nbody{background:transparent;font-family:\'DM Sans\',sans-serif;}\n@keyframes eq1{0%,100%{height:5px}20%{height:22px}50%{height:12px}80%{height:18px}}\n@keyframes eq2{0%,100%{height:18px}25%{height:7px}60%{height:24px}85%{height:10px}}\n@keyframes eq3{0%,100%{height:12px}30%{height:26px}55%{height:8px}90%{height:20px}}\n@keyframes eq4{0%,100%{height:20px}15%{height:9px}50%{height:28px}75%{height:6px}}\n@keyframes eq5{0%,100%{height:8px}35%{height:20px}65%{height:14px}85%{height:24px}}\n@keyframes eq6{0%,100%{height:16px}20%{height:5px}55%{height:22px}80%{height:11px}}\n@keyframes eq7{0%,100%{height:10px}30%{height:24px}60%{height:7px}90%{height:19px}}\n@keyframes scanGlow{0%,100%{opacity:0}50%{opacity:1}}\n@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-3px)}}\n@keyframes rp{0%,100%{box-shadow:0 0 0 0 rgba(229,9,20,0),0 0 20px rgba(229,9,20,0.55)}50%{box-shadow:0 0 0 6px rgba(229,9,20,0.10),0 0 32px rgba(229,9,20,0.75)}}\n@keyframes db{0%,100%{transform:scale(1);opacity:1}50%{transform:scale(0.7);opacity:0.45}}\n@keyframes ci{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}\n.shell{border-radius:22px;overflow:hidden;position:relative;\n  background:linear-gradient(140deg,#06030c,#0d0408 55%,#040610);\n  border:1px solid rgba(255,255,255,0.08);\n  box-shadow:0 32px 100px rgba(0,0,0,0.92),inset 0 1px 0 rgba(255,255,255,0.06);\n  animation:float 6s ease-in-out infinite;}\n.shell::before{content:\'\';position:absolute;top:0;left:0;right:0;height:1.5px;z-index:2;\n  background:linear-gradient(90deg,transparent,#E50914 30%,rgba(255,120,50,0.7) 50%,#E50914 70%,transparent);\n  animation:scanGlow 3s ease-in-out infinite;}\n.orb{position:absolute;top:-90px;right:-90px;width:280px;height:280px;border-radius:50%;pointer-events:none;\n  background:radial-gradient(circle,rgba(229,9,20,0.11) 0%,transparent 70%);}\n.hdr{display:flex;align-items:center;padding:18px 22px 14px;border-bottom:1px solid rgba(255,255,255,0.05);}\n.ring{width:46px;height:46px;border-radius:50%;flex-shrink:0;font-size:1.25rem;\n  background:linear-gradient(135deg,#E50914,#7c000a);\n  display:flex;align-items:center;justify-content:center;animation:rp 2.5s ease-in-out infinite;}\n.ht{margin-left:13px;flex:1;}\n.h1{font-size:0.78rem;font-weight:800;letter-spacing:3.5px;text-transform:uppercase;color:#fff;}\n.h2{font-size:0.65rem;color:rgba(255,255,255,0.28);margin-top:3px;}\n.eq{display:flex;align-items:flex-end;gap:3px;height:28px;}\n.eq span{display:block;width:4px;border-radius:3px;background:linear-gradient(to top,#E50914,#ff7043);box-shadow:0 0 8px rgba(229,9,20,0.65);}\n.eq span:nth-child(1){animation:eq1 0.70s ease-in-out infinite;}\n.eq span:nth-child(2){animation:eq2 0.90s ease-in-out infinite 0.10s;}\n.eq span:nth-child(3){animation:eq3 0.75s ease-in-out infinite 0.20s;}\n.eq span:nth-child(4){animation:eq4 0.85s ease-in-out infinite 0.05s;}\n.eq span:nth-child(5){animation:eq5 0.65s ease-in-out infinite 0.15s;}\n.eq span:nth-child(6){animation:eq6 0.95s ease-in-out infinite 0.08s;}\n.eq span:nth-child(7){animation:eq7 0.80s ease-in-out infinite 0.12s;}\n.chips{display:flex;flex-wrap:wrap;gap:8px;padding:16px 20px 8px;}\n.chip{flex:1;min-width:82px;display:flex;flex-direction:column;align-items:center;gap:5px;\n  padding:13px 8px 11px;border-radius:16px;cursor:pointer;\n  border:1.5px solid rgba(255,255,255,0.08);background:rgba(255,255,255,0.03);\n  transition:all 0.22s cubic-bezier(0.34,1.56,0.64,1);animation:ci 0.4s ease both;}\n.chip:hover{transform:translateY(-4px) scale(1.06);border-color:rgba(255,255,255,0.18);background:rgba(255,255,255,0.07);}\n.chip.on{transform:translateY(-5px) scale(1.10);}\n.cem{font-size:1.55rem;line-height:1;pointer-events:none;}\n.clb{font-size:0.57rem;font-weight:800;letter-spacing:1.2px;text-transform:uppercase;\n  color:rgba(255,255,255,0.40);text-align:center;pointer-events:none;}\n.chip.on .clb{color:#fff;}\n.np{display:flex;align-items:center;gap:11px;margin:6px 20px 12px;padding:12px 16px;\n  border-radius:14px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.07);\n  transition:border-color 0.35s;}\n.dot{width:9px;height:9px;border-radius:50%;flex-shrink:0;animation:db 1.4s ease-in-out infinite;}\n.dv{width:1px;height:28px;background:rgba(255,255,255,0.09);flex-shrink:0;}\n.npi{flex:1;}\n.nll{font-size:0.58rem;font-weight:800;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.30);}\n.nn{font-size:0.90rem;font-weight:700;color:#fff;}\n.nd{font-size:0.68rem;color:rgba(255,255,255,0.28);margin-top:2px;}\n.bdg{font-size:0.60rem;font-weight:700;letter-spacing:1px;text-transform:uppercase;\n  padding:4px 10px;border-radius:20px;background:rgba(255,255,255,0.06);\n  border:1px solid rgba(255,255,255,0.09);color:rgba(255,255,255,0.35);white-space:nowrap;}\n.spw{padding:0 20px 20px;}\n.spw iframe{border-radius:18px;display:block;box-shadow:0 16px 60px rgba(0,0,0,0.75);}\n</style>\n</head>\n<body>\n<div class=\'shell\'>\n  <div class=\'orb\'></div>\n  <div class=\'hdr\'>\n    <div class=\'ring\'>🎵</div>\n    <div class=\'ht\'>\n      <div class=\'h1\'>Workout Music</div>\n      <div class=\'h2\'>Spotify · Choose your vibe · Click any genre below</div>\n    </div>\n    <div class=\'eq\'><span></span><span></span><span></span><span></span><span></span><span></span><span></span></div>\n  </div>\n  <div class=\'chips\' id=\'chips\'></div>\n  <div class=\'np\' id=\'np\'>\n    <div class=\'dot\' id=\'dot\'></div>\n    <div class=\'dv\'></div>\n    <div class=\'npi\'>\n      <div class=\'nll\'>Now Playing</div>\n      <div class=\'nn\' id=\'nn\'></div>\n      <div class=\'nd\' id=\'nd\'></div>\n    </div>\n    <div class=\'bdg\'>Spotify</div>\n  </div>\n  <div class=\'spw\'>\n    <iframe id=\'sp\' width=\'100%\' height=\'380\' frameBorder=\'0\'\n      allow=\'autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture\'\n      loading=\'lazy\'></iframe>\n  </div>\n</div>\n<script>\nvar PL=[{"key": "\\ud83d\\udd25 Beast Mode", "id": "37i9dQZF1DX76Wlfdnj7AP", "desc": "Hard-hitting gym tracks", "color": "#ff4500", "emoji": "\\ud83d\\udd25", "label": "BEAST MODE"}, {"key": "\\ud83d\\udcaa Workout Hits", "id": "4mk1o6g93vy9e9DDOaapX3", "desc": "Top workout bangers", "color": "#E50914", "emoji": "\\ud83d\\udcaa", "label": "WORKOUT HITS"}, {"key": "\\ud83c\\udfa4 Hip-Hop", "id": "37i9dQZF1DX9oh43oAzkyx", "desc": "Hip-hop motivation", "color": "#a855f7", "emoji": "\\ud83c\\udfa4", "label": "HIP-HOP"}, {"key": "\\u26a1 EDM", "id": "37i9dQZF1DXdURFimg6Blm", "desc": "High energy EDM", "color": "#06b6d4", "emoji": "\\u26a1", "label": "EDM"}, {"key": "\\ud83c\\udfb8 Rock", "id": "3W6QwXZyaiG8qRkaie63Cr", "desc": "Rock & metal energy", "color": "#f59e0b", "emoji": "\\ud83c\\udfb8", "label": "ROCK"}, {"key": "\\ud83c\\udfb5 Bollywood", "id": "37i9dQZF1DWXtlo6ENS92N", "desc": "Bollywood pump-up", "color": "#ec4899", "emoji": "\\ud83c\\udfb5", "label": "BOLLYWOOD"}, {"key": "\\ud83c\\udfb6 Tollywood", "id": "37i9dQZF1DX4H5837Y8I1n", "desc": "Telugu beats & energy", "color": "#f97316", "emoji": "\\ud83c\\udfb6", "label": "TOLLYWOOD"}, {"key": "\\ud83c\\udfac Hollywood", "id": "37i9dQZF1DX0XUfTFmNBRM", "desc": "Epic movie soundtracks", "color": "#3b82f6", "emoji": "\\ud83c\\udfac", "label": "HOLLYWOOD"}, {"key": "\\ud83e\\uddd8 Chill Recovery", "id": "37i9dQZF1DX9s3cYAeKW5d", "desc": "Calm down & recover", "color": "#22c55e", "emoji": "\\ud83e\\uddd8", "label": "CHILL RECOVERY"}];\nvar active="\\ud83d\\udd25 Beast Mode";\nfunction rgb(h){h=h.replace(\'#\',\'\');return parseInt(h.slice(0,2),16)+\',\'+parseInt(h.slice(2,4),16)+\',\'+parseInt(h.slice(4,6),16);}\nfunction pick(k){active=k;render();}\nfunction render(){\n  var pl=null;\n  for(var i=0;i<PL.length;i++){if(PL[i].key===active){pl=PL[i];break;}}\n  if(!pl)pl=PL[0];\n  var h=\'\';\n  PL.forEach(function(p,i){\n    var on=(p.key===active);\n    var r=rgb(p.color);\n    var s=on?\'border-color:\'+p.color+\';background:rgba(\'+r+\',0.14);box-shadow:0 0 22px rgba(\'+r+\',0.55),0 8px 24px rgba(0,0,0,0.55);\':\'\';\n    h+=\'<div class="chip\'+(on?\' on\':\'\')+\'" style="\'+s+\'animation-delay:\'+(i*0.04).toFixed(2)+\'s" data-key="\'+p.key.replace(/&/g,\'&amp;\').replace(/"/g,\'&quot;\')+\'">\'\n      +\'<div class="cem">\'+p.emoji+\'</div>\'\n      +\'<div class="clb">\'+p.label+\'</div></div>\';\n  });\n  document.getElementById(\'chips\').innerHTML=h;\n  document.querySelectorAll(\'.chip\').forEach(function(el){\n    el.addEventListener(\'click\',function(){pick(this.getAttribute(\'data-key\'));});\n  });\n  var r2=rgb(pl.color);\n  document.getElementById(\'dot\').style.cssText=\'background:\'+pl.color+\';box-shadow:0 0 12px rgba(\'+r2+\',0.80);\';\n  document.getElementById(\'np\').style.borderColor=pl.color+\'44\';\n  document.getElementById(\'nn\').textContent=pl.emoji+\' \'+(pl.key.split(\' \').slice(1).join(\' \')||pl.key);\n  document.getElementById(\'nd\').textContent=pl.desc;\n  var src=\'https://open.spotify.com/embed/playlist/\'+pl.id+\'?utm_source=generator&theme=0\';\n  var fr=document.getElementById(\'sp\');\n  if(fr.getAttribute(\'src\')!==src)fr.setAttribute(\'src\',src);\n}\nrender();\n</script>\n</body>\n</html>\n'

# Replace active key so the correct chip is highlighted on page load
_final_html = _base_html.replace('__ACTIVE_KEY__', _genre_js).replace('__PL_DATA__', _pl_json)

_cmp.html(_final_html, height=620, scrolling=False)
# ── DAY TABS ──────────────────────────────────────────────────────────────────
tab_labels = [f"Day {d.get('day',i+1)}" + (" 😴" if d.get("is_rest_day") else "")
              for i, d in enumerate(sdays)]
_today_tab_idx = 0
if sdays:
    _plan_start_dt = date.fromisoformat(st.session_state.get("plan_start", date.today().isoformat()))
    _day_offset    = (date.today() - _plan_start_dt).days
    _today_tab_idx = max(0, min(_day_offset, len(sdays)-1))
    if _today_tab_idx > 0:
        st.markdown(
            f"<div style='background:rgba(229,9,20,0.10);border:1px solid rgba(229,9,20,0.30);"
            f"border-radius:10px;padding:8px 16px;margin-bottom:10px;font-size:0.80rem;"
            f"color:rgba(255,255,255,0.75);display:flex;align-items:center;gap:8px'>"
            f"<span style='color:#E50914;font-size:1rem'>&#128197;</span>"
            f"Today is <b style='color:#E50914'>Day {sdays[_today_tab_idx].get('day',_today_tab_idx+1)}"
            f"</b> &mdash; {sdays[_today_tab_idx].get('muscle_group','Workout')}</div>",
            unsafe_allow_html=True
        )

tabs = st.tabs(tab_labels)
EX_ICONS   = ["🏋️","💪","🔄","⬆️","🦵","🤸","🏃","🚴","🧗","🥊"]
MEAL_ICONS = {"breakfast":"🌅","lunch":"☀️","dinner":"🌙","snacks":"🍎"}

for tab, day_data in zip(tabs, sdays):
    with tab:
        dn      = day_data.get("day", 1)
        is_rest = day_data.get("is_rest_day", False)
        mg      = day_data.get("muscle_group", "Full Body")

        if is_rest:
            prev_day = next((x for x in sdays if x.get("day") == dn-1), {})
            prev_mg  = prev_day.get("muscle_group", "")

            # ── REST DAY HERO ─────────────────────────────────────────────
            st.markdown(
                f"<div style='background:linear-gradient(135deg,rgba(34,197,94,0.10),rgba(6,30,15,0.80));"
                f"border:1.5px solid rgba(34,197,94,0.28);border-radius:20px;padding:28px 36px;margin-bottom:20px;"
                f"position:relative;overflow:hidden'>"
                f"<div style='position:absolute;top:0;left:0;right:0;height:2px;"
                f"background:linear-gradient(90deg,transparent,#22c55e,transparent)'></div>"
                f"<div style='font-size:2.5rem;margin-bottom:10px'>😴</div>"
                f"<div style='font-family:Bebas Neue,sans-serif;font-size:2.2rem;letter-spacing:3px;"
                f"color:#22c55e;margin-bottom:8px'>Day {dn} — Rest &amp; Recovery</div>"
                f"<div style='font-size:0.95rem;color:rgba(255,255,255,0.65);max-width:500px;line-height:1.6'>"
                f"Your muscles grow during rest, not during training. Make today count.</div>"
                f"</div>",
                unsafe_allow_html=True
            )

            # ── REST DAY ACTIVITIES GRID ──────────────────────────────────
            _rest_activities = [
                {"icon":"🧘","title":"Yoga","desc":"Improve flexibility & calm the mind","duration":"20–30 min",
                 "video":"https://www.youtube.com/embed/v7AYKMP6rOE","color":"34,197,94"},
                {"icon":"🚶","title":"Walking","desc":"Low-impact cardio, boosts recovery","duration":"20–45 min",
                 "video":"https://www.youtube.com/embed/jeNwE4VXqgs","color":"96,165,250"},
                {"icon":"🧘","title":"Meditation","desc":"Reduce cortisol, improve sleep","duration":"10–15 min",
                 "video":"https://www.youtube.com/embed/sTANio_2E0Q","color":"251,191,36"},
                {"icon":"🌊","title":"Foam Rolling","desc":"Release tight muscles & knots","duration":"10–15 min",
                 "video":"https://www.youtube.com/embed/2pLT-olgUJs","color":"249,115,22"},
            ]

            st.markdown(
                "<div style='font-size:0.75rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;"
                "color:rgba(34,197,94,0.75);margin-bottom:12px;display:flex;align-items:center;gap:8px'>"
                "<span style='width:14px;height:1.5px;background:#22c55e;display:block'></span>"
                "Today's Recovery Activities</div>",
                unsafe_allow_html=True
            )

            act_cols = st.columns(4)
            for _ai, _act in enumerate(_rest_activities):
                with act_cols[_ai]:
                    _vid_key = f"rest_vid_d{dn}_{_ai}"
                    _showing = st.session_state.get(_vid_key, False)
                    st.markdown(
                        f"<div style='background:rgba(8,4,2,0.80);"
                        f"border:1.5px solid rgba({_act['color']},0.28);"
                        f"border-radius:14px;padding:14px;text-align:center;margin-bottom:8px'>"
                        f"<div style='font-size:2rem;margin-bottom:6px'>{_act['icon']}</div>"
                        f"<div style='font-size:0.90rem;font-weight:700;color:#fff;margin-bottom:4px'>{_act['title']}</div>"
                        f"<div style='font-size:0.72rem;color:rgba(255,255,255,0.50);margin-bottom:6px;line-height:1.4'>{_act['desc']}</div>"
                        f"<div style='font-size:0.70rem;color:rgba({_act['color']},0.80);font-weight:700'>"
                        f"⏱ {_act['duration']}</div></div>",
                        unsafe_allow_html=True
                    )
                    if st.button(
                        "▶ Watch" if not _showing else "✕ Hide",
                        key=f"rest_vid_btn_d{dn}_{_ai}",
                        use_container_width=True
                    ):
                        st.session_state[_vid_key] = not _showing
                        st.rerun()
                    if _showing:
                        st.markdown(
                            f"<div style='position:relative;padding-bottom:56.25%;height:0;"
                            f"overflow:hidden;border-radius:10px;margin-top:6px'>"
                            f"<iframe src='{_act['video']}?rel=0&modestbranding=1' "
                            f"style='position:absolute;top:0;left:0;width:100%;height:100%;border:none' "
                            f"allowfullscreen></iframe></div>",
                            unsafe_allow_html=True
                        )

            # ── AI REST DAY SUGGESTIONS ───────────────────────────────────
            st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
            rest_sugg_key = f"rest_sugg_d{dn}"
            if not st.session_state.get(rest_sugg_key):
                if st.button(f"🤖 Get Personalised AI Recovery Plan", key=f"rest_btn_{dn}", use_container_width=False):
                    with st.spinner("Getting personalised suggestions..."):
                        try:
                            from model_api import query_model
                            rp = (
                                f"Give 4 personalised rest day recovery activities for a "
                                f"{data.get('level','Beginner')} person, goal: {data.get('goal','Fitness')}."
                                + (f" They just trained: {prev_mg}." if prev_mg else "")
                                + " Include nutrition tip too. Format: ACTIVITY: duration — benefit. One per line."
                            )
                            st.session_state[rest_sugg_key] = query_model(rp, max_tokens=220).strip()
                            st.rerun()
                        except Exception as e:
                            st.error(str(e))
            else:
                html_r = ""
                for line in st.session_state[rest_sugg_key].splitlines():
                    line = line.strip()
                    if not line: continue
                    if ":" in line:
                        p = line.split(":", 1)
                        html_r += (
                            f"<div style='display:flex;align-items:flex-start;gap:10px;"
                            f"padding:8px 0;border-bottom:1px solid rgba(34,197,94,0.10)'>"
                            f"<span style='color:#22c55e;flex-shrink:0'>▶</span>"
                            f"<div><b style='color:#22c55e'>{p[0].strip()}</b>"
                            f"<span style='color:rgba(255,255,255,0.70)'> {p[1].strip()}</span></div></div>"
                        )
                    else:
                        html_r += f"<div style='font-size:0.82rem;color:rgba(255,255,255,0.55);padding:4px 0'>{line}</div>"
                st.markdown(
                    f"<div style='background:rgba(34,197,94,0.06);border:1.5px solid rgba(34,197,94,0.22);"
                    f"border-radius:14px;padding:16px 20px;margin-top:4px'>"
                    f"<div style='font-size:0.72rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;"
                    f"color:rgba(34,197,94,0.75);margin-bottom:10px'>🤖 YOUR PERSONALISED RECOVERY PLAN</div>"
                    f"{html_r}</div>",
                    unsafe_allow_html=True
                )
                if st.button("↻ Refresh", key=f"rest_refresh_{dn}"):
                    st.session_state.pop(rest_sugg_key, None)
                    st.rerun()
            continue

        left_col, right_col = st.columns([3, 2])

        with left_col:
            pre = day_data.get("pre_stretch", [])
            with st.expander("🔥 Pre-Workout Warm-Up", expanded=False):
                for s in pre:
                    st.markdown(f"<div style='display:flex;gap:10px;align-items:center;padding:6px 0;"
                                f"border-bottom:1px solid rgba(255,255,255,0.05)'>"
                                f"<span style='color:#fbbf24'>🔥</span><div>"
                                f"<div style='font-size:1.05rem;font-weight:600'>{s.get('name','Stretch')}</div>"
                                f"<div style='font-size:0.85rem;color:rgba(255,255,255,0.90)'>⏱ {s.get('duration','30s')}</div></div></div>",
                                unsafe_allow_html=True)
                _pre_urls = [
                    "https://www.youtube.com/embed/2pLT-olgUJs",
                    "https://www.youtube.com/embed/UBMk30rjy0o",
                    "https://www.youtube.com/embed/1f8yoFFdkcY",
                ]
                vurl = _pre_urls[(dn - 1) % len(_pre_urls)]
                st.markdown(f"<div style='position:relative;padding-bottom:56.25%;height:0;overflow:hidden;border-radius:10px;margin-top:8px'>"
                            f"<iframe src='{vurl}?rel=0&modestbranding=1' style='position:absolute;top:0;left:0;width:100%;height:100%;border:none' allowfullscreen></iframe></div>",
                            unsafe_allow_html=True)

            st.markdown(f"<div class='sec-title'>💪 Day {dn} — {mg}</div>", unsafe_allow_html=True)
            exercises = day_data.get("workout", [])
            if not exercises:
                st.markdown("<div style='color:rgba(255,255,255,0.90);padding:20px;text-align:center'>No exercises for this day.</div>", unsafe_allow_html=True)
            else:
                for idx, ex in enumerate(exercises):
                    name_   = ex.get("name",  f"Exercise {idx+1}")
                    sets_   = ex.get("sets",  3)
                    reps_   = ex.get("reps",  "12")
                    rest_   = ex.get("rest",  "60s")
                    timer_  = ex.get("timer", 60)
                    notes_  = ex.get("notes", "Maintain proper form")
                    icon_   = EX_ICONS[idx % len(EX_ICONS)]
                    ck_key  = f"ex_d{dn}_{idx}"
                    is_done = st.session_state.get(ck_key, False)
                    yt_url  = f"https://www.youtube.com/results?search_query={name_.replace(' ','+')}+exercise+tutorial"

                    with st.expander(f"{icon_} {name_}  —  {sets_} × {reps_}", expanded=False):
                        ec1, ec2 = st.columns([3, 2])
                        with ec1:
                            st.markdown(f"""
                            <div class='day-card' style='padding:16px 18px'>
                              <div style='display:flex;gap:8px;margin-bottom:12px;flex-wrap:wrap'>
                                <div class='badge b-sets'><span class='badge-num'>{sets_}</span><span class='badge-lbl'>SETS</span></div>
                                <div class='badge b-reps'><span class='badge-num'>{reps_}</span><span class='badge-lbl'>REPS</span></div>
                                <div class='badge b-rest'><span class='badge-num'>{rest_}</span><span class='badge-lbl'>REST</span></div>
                              </div>
                              <div style='font-size:0.75rem;color:rgba(255,255,255,0.90);border-top:1px solid rgba(255,255,255,0.06);padding-top:10px'>
                                <span style='color:rgba(229,9,20,0.70);font-weight:700'>Form tip: </span>{notes_}
                              </div>
                              <a href='{yt_url}' target='_blank' style='display:inline-block;margin-top:10px;font-size:0.85rem;font-weight:700;color:#ff6b6b;text-decoration:none;border:1px solid rgba(255,107,107,0.30);border-radius:6px;padding:3px 10px;background:rgba(255,107,107,0.08)'>▶ Watch Demo</a>
                            </div>""", unsafe_allow_html=True)

                        # ── EXERCISE SWAP ───────────────────────────────────
                        _swap_key = f"swap_ex_d{dn}_{idx}"
                        _swap_res = st.session_state.get(_swap_key)
                        sc1, sc2 = st.columns([1,1])
                        with sc1:
                            if st.button("🔄 Can't do this? Get Alternative", key=f"swap_btn_d{dn}_{idx}", use_container_width=True):
                                with st.spinner("Finding alternative..."):
                                    try:
                                        from model_api import query_model
                                        _eq  = ", ".join(data.get("equipment", [])) or "bodyweight only"
                                        _inj = ", ".join(data.get("injuries",  [])) or "none"
                                        _swap_prompt = (
                                            f"You are a fitness coach. Suggest exactly 1 alternative exercise "
                                            f"to replace '{name_}' for a {data.get('level','Beginner')} person. "
                                            f"Equipment available: {_eq}. Injuries/limitations: {_inj}. "
                                            f"Muscle group: {mg}. Keep same sets and reps: {sets_} sets x {reps_} reps. "
                                            f"IMPORTANT: Reply in this exact format on one single line — no JSON, no bullets, no extra text:\n"
                                            f"EXERCISE NAME | Why it works | Form tip\n"
                                            f"Example: Dumbbell Press | Targets chest with less shoulder strain | Keep elbows at 45 degrees"
                                        )
                                        _swap_raw = query_model(_swap_prompt, max_tokens=120).strip()
                                        # Robust parser: handles JSON fallback gracefully
                                        import json as _jmod, re as _re
                                        _swap_result = _swap_raw
                                        # If AI returned JSON, extract fields
                                        if _swap_raw.startswith("[") or _swap_raw.startswith("{"):
                                            try:
                                                _jdata = _jmod.loads(_swap_raw)
                                                if isinstance(_jdata, list): _jdata = _jdata[0]
                                                _jname = _jdata.get("EXERCISE NAME") or _jdata.get("name") or _jdata.get("exercise") or ""
                                                _jwhy  = _jdata.get("why it works") or _jdata.get("why") or _jdata.get("reason") or ""
                                                _jtip  = _jdata.get("form tip") or _jdata.get("tip") or _jdata.get("form") or ""
                                                _swap_result = f"{_jname} | {_jwhy} | {_jtip}"
                                            except Exception:
                                                # Strip JSON brackets and use as name
                                                _swap_result = _re.sub(r'[{}\[\]"\':]', ' ', _swap_raw).strip()
                                        st.session_state[_swap_key] = _swap_result
                                        st.rerun()
                                    except Exception as e:
                                        st.error("Swap failed: " + str(e))
                        if _swap_res:
                            with sc2:
                                if st.button("✕ Dismiss", key=f"dismiss_swap_d{dn}_{idx}", use_container_width=True):
                                    st.session_state.pop(_swap_key, None)
                                    st.rerun()
                            # Parse pipe-separated result
                            _parts    = _swap_res.split("|") if "|" in _swap_res else [_swap_res, "", ""]
                            _alt_name = _parts[0].strip() if len(_parts) > 0 else _swap_res
                            _alt_why  = _parts[1].strip() if len(_parts) > 1 else ""
                            _alt_tip  = _parts[2].strip() if len(_parts) > 2 else ""
                            st.markdown(
                                f"<div style='background:rgba(34,197,94,0.07);border:1.5px solid rgba(34,197,94,0.35);"
                                f"border-radius:14px;padding:14px 18px;margin-top:8px;position:relative;overflow:hidden'>"
                                f"<div style='position:absolute;top:0;left:0;right:0;height:2px;"
                                f"background:linear-gradient(90deg,transparent,rgba(34,197,94,0.60),transparent)'></div>"
                                f"<div style='font-size:0.68rem;font-weight:800;letter-spacing:2.5px;text-transform:uppercase;"
                                f"color:rgba(34,197,94,0.70);margin-bottom:8px'>🔄 AI Alternative Exercise</div>"
                                f"<div style='font-size:1.05rem;font-weight:800;color:#22c55e;margin-bottom:6px'>{_alt_name}</div>"
                                + (f"<div style='font-size:0.82rem;color:rgba(255,255,255,0.65);margin-bottom:4px'>"
                                   f"<span style='color:rgba(34,197,94,0.70);font-weight:700'>✅ Why it works:</span> {_alt_why}</div>" if _alt_why else "")
                                + (f"<div style='font-size:0.80rem;color:rgba(255,255,255,0.50)'>"
                                   f"<span style='color:rgba(34,197,94,0.60);font-weight:700'>💡 Form tip:</span> {_alt_tip}</div>" if _alt_tip else "")
                                + f"</div>", unsafe_allow_html=True
                            )

                        with ec2:
                            tid = f"d{dn}_e{idx}"
                            components.html(f"""
<div data-timer-id='{tid}' data-total='{timer_}' style='background:rgba(10,6,4,0.70);border:1.5px solid rgba(229,9,20,0.30);border-radius:14px;padding:18px;text-align:center;position:relative;overflow:hidden'>
  <div style='position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,rgba(229,9,20,0.60),transparent)'></div>
  <div style='font-size:0.85rem;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;color:rgba(229,9,20,0.65);margin-bottom:6px'>⏱ TIMER</div>
  <div data-display='1' style='font-family:Bebas Neue,sans-serif;font-size:3.4rem;color:#E50914;letter-spacing:3px;line-height:1'>{timer_}s</div>
  <div style='font-size:0.85rem;color:rgba(255,255,255,0.90);margin:4px 0 6px'>{name_}</div>
  <div style='margin:0 auto 12px;width:100%;height:5px;background:rgba(0,0,0,0.75);border-radius:3px;overflow:hidden'>
    <div data-bar='1' style='height:100%;width:100%;background:linear-gradient(90deg,#E50914,#ff4444);border-radius:3px;transition:width 0.6s linear'></div>
  </div>
  <div style='display:flex;gap:6px;justify-content:center'>
    <button data-action='start' style='background:linear-gradient(135deg,#E50914,#c0000c);border:none;color:#fff;padding:8px 16px;border-radius:7px;cursor:pointer;font-size:1.00rem;font-weight:700;min-width:76px'>▶ Start</button>
    <button data-action='pause' style='background:rgba(0,0,0,0.75);border:1px solid rgba(255,255,255,0.18);color:rgba(255,255,255,0.90);padding:8px 14px;border-radius:7px;cursor:pointer;font-size:1.00rem;font-weight:700'>⏸</button>
    <button data-action='reset' style='background:rgba(0,0,0,0.75);border:1px solid rgba(255,255,255,0.10);color:rgba(255,255,255,0.90);padding:8px 14px;border-radius:7px;cursor:pointer;font-size:1.00rem;font-weight:700'>↺</button>
  </div>
  <div data-done='1' style='display:none;margin-top:10px;font-family:Bebas Neue,sans-serif;font-size:1.4rem;letter-spacing:2px;color:#22c55e'>✓ TIME'S UP!</div>
</div>
<script>
(function(){{
  var c=document.querySelector('[data-timer-id="{tid}"]');
  if(!c)return;
  var TOTAL=parseFloat(c.getAttribute('data-total'))||{timer_};
  var TID='{tid}',LR='fpt_'+TID+'_rem',LRN='fpt_'+TID+'_run',LT='fpt_'+TID+'_ts',IK='_fptiv_'+TID;
  var disp=c.querySelector('[data-display]'),bar=c.querySelector('[data-bar]'),done=c.querySelector('[data-done]');
  var sb=c.querySelector('[data-action=start]'),pb=c.querySelector('[data-action=pause]'),rb=c.querySelector('[data-action=reset]');
  function ls(k,v){{try{{localStorage.setItem(k,v);}}catch(e){{}}}}
  function lg(k){{try{{return localStorage.getItem(k);}}catch(e){{return null;}}}}
  function ld(k){{try{{localStorage.removeItem(k);}}catch(e){{}}}}
  function ss(r,run){{ls(LR,r);ls(LRN,run?'1':'0');ls(LT,Date.now());}}
  function lr(){{var r=parseFloat(lg(LR));if(isNaN(r)||r<0)return TOTAL;if(lg(LRN)==='1'){{var t=parseFloat(lg(LT)||0);if(t>0)r=Math.max(0,r-(Date.now()-t)/1000);}}return r;}}
  function cs(){{ld(LR);ld(LRN);ld(LT);}}
  function fmt(s){{var x=Math.ceil(s);if(x<=0)return'✓';var m=Math.floor(x/60),r=x%60;return m>0?(m<10?'0':'')+m+':'+(r<10?'0':'')+r:x+'s';}}
  function upd(r){{if(!disp)return;disp.textContent=fmt(r);disp.style.color=r<=0?'#22c55e':r<=5?'#ef4444':r<=10?'#fbbf24':'#E50914';if(bar)bar.style.width=Math.max(0,(r/TOTAL)*100)+'%';}}
  function ssb(run){{if(!sb)return;sb.textContent=run?'▶ Running':'▶ Start';sb.style.opacity=run?'0.5':'1';sb.style.cursor=run?'not-allowed':'pointer';}}
  function beep(){{try{{var ctx=new(window.AudioContext||window.webkitAudioContext)();[880,1100,1320].forEach(function(f,i){{var o=ctx.createOscillator(),g=ctx.createGain();o.connect(g);g.connect(ctx.destination);o.frequency.value=f;g.gain.setValueAtTime(0.3,ctx.currentTime+i*0.18);g.gain.exponentialRampToValueAtTime(0.001,ctx.currentTime+i*0.18+0.3);o.start(ctx.currentTime+i*0.18);o.stop(ctx.currentTime+i*0.18+0.3);}});}}catch(e){{}}}}
  function stop(){{if(window[IK]){{clearInterval(window[IK]);window[IK]=null;}}}}
  function start(r){{stop();ss(r,true);window[IK]=setInterval(function(){{var x=lr();upd(x);ss(x,true);if(x<=0){{stop();ss(0,false);if(done)done.style.display='block';ssb(false);beep();}}}},300);}}
  if(sb)sb.addEventListener('click',function(){{var r=lr();if(r<=0||window[IK])return;if(done)done.style.display='none';ssb(true);start(r);}});
  if(pb)pb.addEventListener('click',function(){{if(!window[IK])return;var r=lr();stop();ss(r,false);ssb(false);}});
  if(rb)rb.addEventListener('click',function(){{stop();cs();upd(TOTAL);if(done)done.style.display='none';ssb(false);}});
  (function(){{var r=lr(),run=lg(LRN)==='1'&&r>0;upd(r);ssb(run);if(r<=0&&lg(LR)!==null){{if(done)done.style.display='block';}}else if(run){{start(r);}}}})();
}})();
</script>""", height=220, scrolling=False)

                        note_key   = f"note_d{dn}_e{idx}"
                        saved_note = st.session_state.get(note_key, "")
                        with st.form(key=f"note_form_d{dn}_e{idx}", clear_on_submit=False):
                            new_note = st.text_area("📝 Workout Note", value=saved_note,
                                                    placeholder="e.g. Felt easy — increase weight next time", height=68)
                            _note_saved = st.form_submit_button("💾 Save Note")
                        if _note_saved and new_note != saved_note:
                            st.session_state[note_key] = new_note
                            if plan_id:
                                try:
                                    from utils.db import save_workout_note
                                    save_workout_note(uname, plan_id, dn, idx, new_note)
                                except Exception: pass
                            st.toast("Note saved!", icon="📝")

                        _cb_new = st.checkbox(
                            f"✅ {name_} — {'Completed ✓' if is_done else 'Mark as done'}",
                            value=is_done, key=ck_key+"_cb"
                        )
                        if _cb_new != is_done:
                            st.session_state[ck_key] = _cb_new
                            if plan_id:
                                try:
                                    from utils.db import save_progress
                                    wc = {f"ex_{i}": st.session_state.get(f"ex_d{dn}_{i}", False) for i in range(len(exercises))}
                                    dc = {m: st.session_state.get(f"meal_d{dn}_{m}", False) for m in ["breakfast","lunch","dinner","snacks"]}
                                    save_progress(uname, plan_id, dn, wc, dc)
                                except Exception: pass
                            # ── CHECK IF ALL EXERCISES DONE FOR THIS DAY ──────
                            _all_done_now = all(
                                st.session_state.get(f"ex_d{dn}_{_ei}", False)
                                for _ei in range(len(exercises))
                            )
                            if _all_done_now and _cb_new:
                                _celeb_key = f"_celebrated_d{dn}"
                                if not st.session_state.get(_celeb_key):
                                    st.session_state[_celeb_key] = True
                                    st.session_state["_show_celebration"] = dn
                            st.session_state["_needs_rerun"] = True

            rpe_key     = f"rpe_d{dn}"
            current_rpe = st.session_state.get(rpe_key, 0)
            _rpe_descs  = {0:"Not rated",1:"Very Easy 😌",2:"Easy 🙂",3:"Moderate 😊",
                           4:"Somewhat Hard 😤",5:"Hard 😰",6:"Hard 😰",
                           7:"Very Hard 🥵",8:"Very Hard 🥵",9:"Max Effort 😵",10:"Max Effort 💀"}
            st.markdown(
                "<div style='background:rgba(10,6,4,0.70);border:1px solid rgba(255,255,255,0.12);"
                "border-radius:12px;padding:14px 18px;margin:12px 0;backdrop-filter:blur(8px)'>"
                "<div style='font-size:0.85rem;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;"
                "color:rgba(229,9,20,0.75);margin-bottom:10px'>⚡ Rate Workout Intensity (RPE 1–10)</div>",
                unsafe_allow_html=True
            )
            _rpe_new = st.select_slider("Intensity", options=list(range(0, 11)), value=current_rpe,
                                        format_func=lambda x: "Not rated" if x == 0 else f"RPE {x}",
                                        key=f"rpe_slider_{dn}", label_visibility="collapsed")
            if _rpe_new != current_rpe:
                st.session_state[rpe_key] = _rpe_new
                try:
                    from utils.db import save_user_setting
                    save_user_setting(uname, f"rpe_d{dn}", str(_rpe_new))
                except Exception: pass
                st.toast(f"⚡ RPE {_rpe_new} saved!", icon="💪")
                st.rerun()
            if _rpe_new > 0:
                _rpe_c = "#22c55e" if _rpe_new<=3 else "#fbbf24" if _rpe_new<=6 else "#f97316" if _rpe_new<=8 else "#ef4444"
                st.markdown(f"<div style='font-size:1.05rem;font-weight:600;color:{_rpe_c};margin-top:4px'>"
                            f"RPE {_rpe_new} — {_rpe_descs.get(_rpe_new,'')}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            post = day_data.get("post_stretch", [])
            with st.expander("🧊 Post-Workout Cool-Down", expanded=False):
                for s in post:
                    st.markdown(f"<div style='display:flex;gap:10px;align-items:center;padding:6px 0;"
                                f"border-bottom:1px solid rgba(255,255,255,0.05)'>"
                                f"<span style='color:#22c55e'>🧊</span><div>"
                                f"<div style='font-size:1.05rem;font-weight:600'>{s.get('name','Stretch')}</div>"
                                f"<div style='font-size:0.85rem;color:rgba(255,255,255,0.90)'>⏱ {s.get('duration','40s')}</div></div></div>",
                                unsafe_allow_html=True)
                _post_urls = [
                    "https://www.youtube.com/embed/v7AYKMP6rOE",
                    "https://www.youtube.com/embed/jeNwE4VXqgs",
                    "https://www.youtube.com/embed/sTANio_2E0Q",
                ]
                vurl2 = _post_urls[(dn - 1) % len(_post_urls)]
                st.markdown(f"<div style='position:relative;padding-bottom:56.25%;height:0;overflow:hidden;border-radius:10px;margin-top:8px'>"
                            f"<iframe src='{vurl2}?rel=0&modestbranding=1' style='position:absolute;top:0;left:0;width:100%;height:100%;border:none' allowfullscreen></iframe></div>",
                            unsafe_allow_html=True)

        with right_col:
            dietary  = day_data.get("dietary", {})
            diet_t   = st.session_state.get("dietary_type", "veg")
            st.markdown(f"""
            <div style='background:rgba(10,20,12,0.60);border:1px solid rgba(34,197,94,0.20);
              border-radius:16px;padding:20px 22px;position:relative;overflow:hidden'>
              <div style='position:absolute;top:0;left:0;right:0;height:1.5px;
                background:linear-gradient(90deg,transparent,rgba(34,197,94,0.50),transparent)'></div>
              <div style='font-size:0.85rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;
                color:rgba(34,197,94,0.75);margin-bottom:16px;display:flex;align-items:center;gap:6px'>
                <span style='width:14px;height:1.5px;background:#22c55e;display:block'></span>
                🥗 Day {dn} Diet Plan
                <span style='margin-left:auto;font-size:0.85rem;color:rgba(34,197,94,0.55)'>
                  {'🌿 Veg' if diet_t=='veg' else '🍗 Non-Veg'}
                </span>
              </div>
            """, unsafe_allow_html=True)
            for meal, desc in dietary.items():
                if not desc: continue
                icon  = MEAL_ICONS.get(meal, "🍽️")
                ck    = f"meal_d{dn}_{meal}"
                done  = st.session_state.get(ck, False)
                strike = "text-decoration:line-through;opacity:0.50;" if done else ""
                st.markdown(f"<div class='meal-card'><div class='meal-lbl'>{icon} {meal.upper()}</div>"
                            f"<div class='meal-txt' style='{strike}'>{desc}</div></div>", unsafe_allow_html=True)
                _meal_new = st.checkbox(f"✅ {meal.title()} done", value=done, key=ck+"_cb")
                if _meal_new != done:
                    st.session_state[ck] = _meal_new
                    if plan_id:
                        try:
                            from utils.db import save_progress
                            wc_ = {f"ex_{i}": st.session_state.get(f"ex_d{dn}_{i}", False)
                                   for i in range(len(exercises if not is_rest else []))}
                            dc_ = {m2: st.session_state.get(f"meal_d{dn}_{m2}", False)
                                   for m2 in ["breakfast","lunch","dinner","snacks"]}
                            save_progress(uname, plan_id, dn, wc_, dc_)
                        except Exception: pass
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

if st.session_state.pop("_needs_rerun", False):
    st.rerun()