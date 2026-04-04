# -*- coding: utf-8 -*-
import streamlit as st
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth_token import logout

st.set_page_config(
    page_title="AI Meal Planner | FitPlan Pro",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if not st.session_state.get("logged_in"):
    st.switch_page("app.py")
if "user_data" not in st.session_state:
    st.switch_page("pages/1_Profile.py")

uname = st.session_state.get("username", "Athlete")
data  = st.session_state.user_data

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="stAppViewContainer"]::before {
  content:'';position:fixed;inset:0;z-index:-1;
  background:url('https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=1800&q=80&auto=format&fit=crop')
    center center/cover no-repeat;
  filter:blur(7px) brightness(0.28) saturate(0.65);
  transform:scale(1.06);
}
[data-testid="stAppViewContainer"] { background:rgba(2,6,3,0.78)!important; }
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow+Condensed:wght@700;800;900&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700&display=swap');
#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stDecoration"],
[data-testid="stSidebarNav"],section[data-testid="stSidebar"]{display:none!important;}
html,body,.stApp{background:#020802!important;color:#fff!important;font-family:'DM Sans',sans-serif!important;}
[data-testid="stAppViewContainer"]>section>div.block-container{
  max-width:1100px!important;margin:0 auto!important;padding:0 24px 100px!important;}

/* Nav */
.nav-wrap{background:rgba(2,8,4,0.97);backdrop-filter:blur(36px);
  border-bottom:1.5px solid rgba(34,197,94,0.22);box-shadow:0 2px 24px rgba(0,0,0,0.65);
  padding:5px 0;margin-bottom:4px;}
.nav-logo{font-family:'Bebas Neue',sans-serif;font-size:1.4rem;letter-spacing:5px;
  color:#22c55e;text-shadow:0 0 18px rgba(34,197,94,0.45);line-height:1;}

/* Buttons */
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"] > button{
  background:rgba(2,14,6,0.82)!important;border:2px solid rgba(34,197,94,0.55)!important;
  color:rgba(255,255,255,0.92)!important;border-radius:9px!important;
  font-family:'DM Sans',sans-serif!important;font-size:0.85rem!important;font-weight:700!important;
  padding:5px 8px!important;height:32px!important;min-height:32px!important;
  white-space:nowrap!important;transition:all 0.15s ease!important;}
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"] > button:hover{
  background:rgba(34,197,94,0.20)!important;border-color:rgba(34,197,94,0.85)!important;
  color:#fff!important;transform:translateY(-1px)!important;}
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"]:last-child > button{
  background:linear-gradient(135deg,#c0000c,#8b0000)!important;
  border-color:rgba(229,9,20,0.80)!important;}
.stButton>button{background:linear-gradient(135deg,rgba(34,197,94,0.85),rgba(16,120,50,0.90))!important;
  border:2px solid rgba(34,197,94,0.65)!important;color:#fff!important;border-radius:10px!important;
  font-family:'DM Sans',sans-serif!important;font-size:0.95rem!important;font-weight:700!important;
  box-shadow:0 0 16px rgba(34,197,94,0.30)!important;transition:all 0.25s!important;}
.stButton>button:hover{transform:translateY(-2px) scale(1.02)!important;
  box-shadow:0 0 28px rgba(34,197,94,0.55)!important;}

/* Widgets */
[data-testid="stWidgetLabel"],[data-testid="stWidgetLabel"] p{
  color:#fff!important;font-size:0.95rem!important;font-weight:700!important;
  letter-spacing:1.5px!important;text-transform:uppercase!important;}
.stSelectbox>div>div,.stNumberInput>div>div>input,.stSlider{
  background:rgba(5,18,8,0.75)!important;border-color:rgba(34,197,94,0.30)!important;color:#fff!important;}
.stSelectbox [data-baseweb="select"]>div{background:rgba(5,18,8,0.80)!important;
  border:1.5px solid rgba(34,197,94,0.30)!important;color:#fff!important;}
.stMarkdown p,.stMarkdown li{color:#fff!important;font-size:1rem!important;line-height:1.7!important;}
html,body,.stApp,.stMarkdown,p,div,span,label{text-shadow:0 2px 6px rgba(0,0,0,0.95)!important;}

/* Cards */
.meal-card{
  background:rgba(4,18,8,0.88);
  border:1.5px solid rgba(34,197,94,0.22);
  border-radius:18px;padding:20px 24px;margin-bottom:12px;
  position:relative;overflow:hidden;
}
.meal-card::before{content:'';position:absolute;top:0;left:0;right:0;height:1.5px;
  background:linear-gradient(90deg,transparent,rgba(34,197,94,0.60),transparent);}
.macro-bar-wrap{background:rgba(255,255,255,0.06);border-radius:6px;height:8px;
  overflow:hidden;margin-top:6px;}
.macro-bar{height:100%;border-radius:6px;transition:width 1s ease;}
.config-card{background:rgba(4,14,8,0.90);border:1.5px solid rgba(34,197,94,0.18);
  border-radius:18px;padding:24px 28px;margin-bottom:20px;position:relative;overflow:hidden;}
.config-card::before{content:'';position:absolute;top:0;left:0;right:0;height:1.5px;
  background:linear-gradient(90deg,transparent,rgba(34,197,94,0.50),transparent);}
.macro-chip{display:inline-flex;flex-direction:column;align-items:center;
  padding:10px 16px;border-radius:12px;min-width:80px;text-align:center;}
.plan-header{background:linear-gradient(135deg,rgba(34,197,94,0.15),rgba(16,80,32,0.10));
  border:1.5px solid rgba(34,197,94,0.35);border-radius:16px;padding:20px 26px;
  margin-bottom:20px;position:relative;overflow:hidden;}
.plan-header::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,transparent,#22c55e,rgba(34,197,94,0.40),#22c55e,transparent);}
.tip-box{background:rgba(6,182,212,0.07);border:1px solid rgba(6,182,212,0.22);
  border-radius:12px;padding:12px 16px;margin-top:8px;}
.history-card{background:rgba(4,14,8,0.75);border:1px solid rgba(34,197,94,0.14);
  border-radius:14px;padding:16px 20px;margin-bottom:10px;cursor:pointer;
  transition:border-color 0.18s;}
.history-card:hover{border-color:rgba(34,197,94,0.35);}
</style>
""", unsafe_allow_html=True)

# ── NAV ───────────────────────────────────────────────────────────────────────
st.markdown("<div class='nav-wrap'>", unsafe_allow_html=True)
_n = st.columns([1.8,1,1,1,1,1,1,1.1,1.3])
with _n[0]: st.markdown("<div class='nav-logo'>⚡ FITPLAN PRO</div>", unsafe_allow_html=True)
with _n[1]:
    if st.button("🏠 Home",     key="nm_db", use_container_width=True): st.switch_page("pages/2_Dashboard.py")
with _n[2]:
    if st.button("⚡ Workout",  key="nm_wp", use_container_width=True): st.switch_page("pages/3_Workout_Plan.py")
with _n[3]:
    if st.button("🥗 Diet",     key="nm_dp", use_container_width=True): st.switch_page("pages/4_Diet_Plan.py")
with _n[4]:
    if st.button("🤖 AI Coach", key="nm_ai", use_container_width=True):
        try: st.switch_page("pages/5_ai_coach.py")
        except Exception: pass
with _n[5]:
    if st.button("🏆 Records",  key="nm_rc", use_container_width=True):
        try: st.switch_page("pages/6_records.py")
        except Exception: pass
with _n[6]:
    if st.button("● 🍽️ Meals", key="nm_mp", use_container_width=True):
        st.rerun()
with _n[7]:
    if st.button("📅 History",  key="nm_hi", use_container_width=True):
        try: st.switch_page("pages/9_history.py")
        except Exception: pass
with _n[8]:
    if st.button("🚪 Sign Out", key="nm_so", use_container_width=True):
        logout(uname)
        for _k in ["logged_in","username","auth_token","user_data","workout_plan",
                   "structured_days","dietary_type","full_plan_data","plan_id","plan_start",
                   "plan_duration","force_regen","tracking","_plan_checked","_db_loaded_dash"]:
            st.session_state.pop(_k, None)
        st.switch_page("app.py")
st.markdown("</div>", unsafe_allow_html=True)

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='background:linear-gradient(135deg,rgba(34,197,94,0.14),rgba(16,80,32,0.08) 50%,rgba(4,14,8,0.60));
  border:2px solid rgba(34,197,94,0.38);border-radius:18px;padding:28px 36px;margin:12px 0 24px;
  position:relative;overflow:hidden;'>
  <div style='position:absolute;top:0;left:0;right:0;height:2px;
    background:linear-gradient(90deg,transparent,#22c55e,transparent);'></div>
  <div style='font-size:0.80rem;font-weight:700;letter-spacing:4px;text-transform:uppercase;
    color:rgba(34,197,94,0.80);margin-bottom:8px;'>🍽️ AI Meal Planner</div>
  <div style='font-family:Barlow Condensed,sans-serif;font-size:clamp(1.8rem,4vw,3rem);
    font-weight:900;text-transform:uppercase;color:#fff;line-height:1;margin-bottom:8px;'>
    Your Perfect Day of <span style='color:#22c55e;'>Eating</span>
  </div>
  <div style='font-size:0.95rem;color:rgba(255,255,255,0.60);max-width:560px;'>
    Pick your cuisine, dietary preference and calorie goal — AI generates a personalised
    full-day meal plan with exact macros in seconds.
  </div>
</div>
""", unsafe_allow_html=True)

# ── CUISINES ──────────────────────────────────────────────────────────────────
CUISINES = {
    "🇮🇳 Indian":      "Indian",
    "🇮🇹 Italian":     "Italian",
    "🇲🇽 Mexican":     "Mexican",
    "🇯🇵 Japanese":    "Japanese",
    "🇨🇳 Chinese":     "Chinese",
    "🇬🇷 Mediterranean":"Mediterranean",
    "🇺🇸 American":    "American",
    "🇹🇭 Thai":        "Thai",
    "🇦🇪 Middle Eastern":"Middle Eastern",
    "🌍 Pan-Asian":    "Pan-Asian",
}

DIETS = {
    "🌿 Vegetarian":   "Vegetarian",
    "🍗 Non-Vegetarian":"Non-Vegetarian",
    "🌱 Vegan":        "Vegan",
    "🥚 Eggetarian":   "Eggetarian",
    "💪 High Protein": "High Protein",
    "⚖️ Balanced":     "Balanced",
    "🔥 Keto":         "Keto",
    "🫀 Low Carb":     "Low Carb",
}

GOALS = {
    "⚡ Maintain Weight":   "maintain",
    "🔥 Lose Weight":       "lose",
    "💪 Build Muscle":      "build muscle",
    "🏃 Improve Performance":"athletic performance",
}

# ── USER PROFILE DEFAULTS ─────────────────────────────────────────────────────
_user_weight = data.get("weight", 70)
_user_goal   = data.get("goal", "General Fitness")
_user_diet   = data.get("diet_type", "veg")

# Sensible calorie default based on profile
_default_cal = (
    1800 if "lose"  in _user_goal.lower() else
    2500 if "build" in _user_goal.lower() or "muscle" in _user_goal.lower() else
    2000
)

# ── CONFIGURATION PANEL ───────────────────────────────────────────────────────
st.markdown("<div class='config-card'>", unsafe_allow_html=True)
st.markdown("""<div style='font-size:0.75rem;font-weight:800;letter-spacing:3px;
  text-transform:uppercase;color:rgba(34,197,94,0.70);margin-bottom:16px;'>
  ⚙️ Configure Your Plan</div>""", unsafe_allow_html=True)

_col1, _col2, _col3 = st.columns([1.4, 1.4, 1.2])
with _col1:
    _cuisine_label = st.selectbox(
        "🌍 Cuisine Style",
        list(CUISINES.keys()),
        index=0,
        key="mp_cuisine"
    )
    _cuisine = CUISINES[_cuisine_label]

with _col2:
    _diet_label = st.selectbox(
        "🥦 Dietary Preference",
        list(DIETS.keys()),
        index=list(DIETS.values()).index("Vegetarian") if _user_diet == "veg" else 1,
        key="mp_diet"
    )
    _diet = DIETS[_diet_label]

with _col3:
    _goal_label = st.selectbox(
        "🎯 Fitness Goal",
        list(GOALS.keys()),
        key="mp_goal"
    )
    _goal = GOALS[_goal_label]

_col4, _col5 = st.columns([2, 2])
with _col4:
    _calories = st.slider(
        "🔥 Daily Calorie Target",
        min_value=1200,
        max_value=4000,
        value=_default_cal,
        step=50,
        key="mp_calories",
        help="Total calories across all meals for the day"
    )
with _col5:
    _allergies = st.text_input(
        "⚠️ Allergies / Avoid (optional)",
        placeholder="e.g. nuts, dairy, gluten, shellfish",
        key="mp_allergies"
    )

# Macro breakdown preview
_prot_g  = int(_calories * 0.30 / 4)
_carb_g  = int(_calories * 0.40 / 4)
_fat_g   = int(_calories * 0.30 / 9)
if _goal == "build muscle":
    _prot_g = int(_calories * 0.35 / 4)
    _carb_g = int(_calories * 0.40 / 4)
    _fat_g  = int(_calories * 0.25 / 9)
elif _goal == "lose":
    _prot_g = int(_calories * 0.35 / 4)
    _carb_g = int(_calories * 0.30 / 4)
    _fat_g  = int(_calories * 0.35 / 9)
elif _diet == "Keto" or _diet == "Low Carb":
    _prot_g = int(_calories * 0.30 / 4)
    _carb_g = int(_calories * 0.10 / 4)
    _fat_g  = int(_calories * 0.60 / 9)

st.markdown(f"""
<div style='display:flex;gap:10px;margin-top:14px;flex-wrap:wrap;'>
  <div style='font-size:0.72rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;
    color:rgba(255,255,255,0.35);display:flex;align-items:center;margin-right:4px;'>
    TARGET MACROS →</div>
  <div class='macro-chip' style='background:rgba(59,130,246,0.12);border:1px solid rgba(59,130,246,0.30);'>
    <div style='font-family:Bebas Neue,sans-serif;font-size:1.3rem;color:#93c5fd;'>{_prot_g}g</div>
    <div style='font-size:0.60rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:rgba(147,197,253,0.60);'>Protein</div>
  </div>
  <div class='macro-chip' style='background:rgba(251,191,36,0.10);border:1px solid rgba(251,191,36,0.28);'>
    <div style='font-family:Bebas Neue,sans-serif;font-size:1.3rem;color:#fcd34d;'>{_carb_g}g</div>
    <div style='font-size:0.60rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:rgba(252,211,77,0.60);'>Carbs</div>
  </div>
  <div class='macro-chip' style='background:rgba(249,115,22,0.10);border:1px solid rgba(249,115,22,0.28);'>
    <div style='font-family:Bebas Neue,sans-serif;font-size:1.3rem;color:#fdba74;'>{_fat_g}g</div>
    <div style='font-size:0.60rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:rgba(253,186,116,0.60);'>Fats</div>
  </div>
  <div class='macro-chip' style='background:rgba(34,197,94,0.10);border:1px solid rgba(34,197,94,0.28);'>
    <div style='font-family:Bebas Neue,sans-serif;font-size:1.3rem;color:#86efac;'>{_calories}</div>
    <div style='font-size:0.60rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:rgba(134,239,172,0.60);'>kcal</div>
  </div>
</div>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ── GENERATE BUTTON ───────────────────────────────────────────────────────────
_gen_col, _hist_col = st.columns([2, 1])
with _gen_col:
    _generate = st.button(
        "🍽️ Generate My Meal Plan",
        key="mp_generate",
        use_container_width=True
    )

# ── AI PROMPT BUILDER ─────────────────────────────────────────────────────────
def build_meal_prompt(cuisine, diet, goal, calories, prot, carb, fat, allergies, name, weight):
    avoid_str = f" Avoid: {allergies}." if allergies.strip() else ""
    return f"""You are an expert nutritionist and chef. Create a detailed full-day {cuisine} meal plan for {name}.

User profile: weight {weight}kg, goal: {goal}, diet: {diet}.
Daily targets: {calories} kcal | Protein: {prot}g | Carbs: {carb}g | Fats: {fat}g.{avoid_str}

Create exactly 5 meals: Breakfast, Morning Snack, Lunch, Evening Snack, Dinner.
Use authentic {cuisine} cuisine dishes only. Make it realistic, delicious, and practical.

Return ONLY valid JSON in this exact structure (no markdown, no explanation):
{{
  "plan_title": "short catchy title for this meal plan",
  "cuisine": "{cuisine}",
  "diet": "{diet}",
  "total_calories": {calories},
  "total_protein": {prot},
  "total_carbs": {carb},
  "total_fats": {fat},
  "hydration_tip": "one specific hydration tip for {goal} goal",
  "meals": [
    {{
      "meal_type": "Breakfast",
      "time": "7:00 – 8:00 AM",
      "name": "dish name",
      "description": "2 sentence description of the dish and why it fits the goal",
      "ingredients": ["ingredient 1", "ingredient 2", "ingredient 3"],
      "calories": 400,
      "protein": 25,
      "carbs": 45,
      "fats": 12,
      "prep_time": "10 min",
      "tip": "one short cooking or eating tip"
    }},
    {{
      "meal_type": "Morning Snack",
      "time": "10:30 – 11:00 AM",
      "name": "snack name",
      "description": "description",
      "ingredients": ["ingredient 1", "ingredient 2"],
      "calories": 200,
      "protein": 10,
      "carbs": 25,
      "fats": 6,
      "prep_time": "5 min",
      "tip": "tip"
    }},
    {{
      "meal_type": "Lunch",
      "time": "1:00 – 2:00 PM",
      "name": "dish name",
      "description": "description",
      "ingredients": ["ingredient 1", "ingredient 2", "ingredient 3", "ingredient 4"],
      "calories": 550,
      "protein": 35,
      "carbs": 60,
      "fats": 18,
      "prep_time": "20 min",
      "tip": "tip"
    }},
    {{
      "meal_type": "Evening Snack",
      "time": "4:30 – 5:00 PM",
      "name": "snack name",
      "description": "description",
      "ingredients": ["ingredient 1", "ingredient 2"],
      "calories": 150,
      "protein": 8,
      "carbs": 20,
      "fats": 4,
      "prep_time": "3 min",
      "tip": "tip"
    }},
    {{
      "meal_type": "Dinner",
      "time": "7:30 – 8:30 PM",
      "name": "dish name",
      "description": "description",
      "ingredients": ["ingredient 1", "ingredient 2", "ingredient 3", "ingredient 4"],
      "calories": 500,
      "protein": 40,
      "carbs": 45,
      "fats": 16,
      "prep_time": "25 min",
      "tip": "tip"
    }}
  ]
}}"""

# ── MEAL CARD RENDERER ────────────────────────────────────────────────────────
MEAL_ICONS = {
    "Breakfast":      "🌅",
    "Morning Snack":  "🍎",
    "Lunch":          "☀️",
    "Evening Snack":  "🍵",
    "Dinner":         "🌙",
}
MEAL_COLORS = {
    "Breakfast":      ("#f59e0b", "rgba(245,158,11,0.15)", "rgba(245,158,11,0.30)"),
    "Morning Snack":  ("#22c55e", "rgba(34,197,94,0.12)",  "rgba(34,197,94,0.25)"),
    "Lunch":          ("#06b6d4", "rgba(6,182,212,0.12)",  "rgba(6,182,212,0.28)"),
    "Evening Snack":  ("#a855f7", "rgba(168,85,247,0.12)", "rgba(168,85,247,0.26)"),
    "Dinner":         ("#E50914", "rgba(229,9,20,0.12)",   "rgba(229,9,20,0.28)"),
}

def render_meal_card(meal: dict, total_cal: int):
    mt    = meal.get("meal_type", "Meal")
    icon  = MEAL_ICONS.get(mt, "🍽️")
    col, bg, border = MEAL_COLORS.get(mt, ("#22c55e", "rgba(34,197,94,0.12)", "rgba(34,197,94,0.28)"))
    name  = meal.get("name", "")
    desc  = meal.get("description", "")
    ingr  = meal.get("ingredients", [])
    cal   = meal.get("calories", 0)
    prot  = meal.get("protein", 0)
    carb  = meal.get("carbs", 0)
    fat   = meal.get("fats", 0)
    time_ = meal.get("time", "")
    prep  = meal.get("prep_time", "")
    tip   = meal.get("tip", "")
    pct   = min(100, int(cal / max(total_cal, 1) * 100))

    ingr_html = "".join(
        f"<span style='background:rgba(255,255,255,0.06);border:0.5px solid rgba(255,255,255,0.12);"
        f"border-radius:20px;padding:3px 10px;font-size:0.72rem;color:rgba(255,255,255,0.65);'>{i}</span>"
        for i in ingr
    )

    st.markdown(f"""
<div style='background:{bg};border:1.5px solid {border};border-radius:18px;
  padding:20px 24px;margin-bottom:14px;position:relative;overflow:hidden;'>
  <div style='position:absolute;top:0;left:0;right:0;height:2px;
    background:linear-gradient(90deg,transparent,{col},transparent);'></div>

  <!-- Header row -->
  <div style='display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:12px;'>
    <div style='display:flex;align-items:center;gap:12px;'>
      <div style='width:42px;height:42px;border-radius:12px;background:{bg};border:1.5px solid {border};
        display:flex;align-items:center;justify-content:center;font-size:1.4rem;flex-shrink:0;'>{icon}</div>
      <div>
        <div style='font-size:0.65rem;font-weight:800;letter-spacing:2.5px;text-transform:uppercase;
          color:{col};margin-bottom:2px;'>{mt}</div>
        <div style='font-size:1.05rem;font-weight:700;color:#fff;line-height:1.2;'>{name}</div>
      </div>
    </div>
    <div style='text-align:right;flex-shrink:0;margin-left:12px;'>
      <div style='font-family:Bebas Neue,sans-serif;font-size:1.6rem;color:{col};line-height:1;'>{cal}</div>
      <div style='font-size:0.62rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;
        color:rgba(255,255,255,0.35);'>kcal</div>
    </div>
  </div>

  <!-- Description -->
  <div style='font-size:0.83rem;color:rgba(255,255,255,0.58);margin-bottom:12px;line-height:1.55;'>{desc}</div>

  <!-- Macros row -->
  <div style='display:flex;gap:8px;margin-bottom:12px;flex-wrap:wrap;'>
    <div style='background:rgba(59,130,246,0.12);border:1px solid rgba(59,130,246,0.25);
      border-radius:8px;padding:6px 12px;text-align:center;'>
      <div style='font-size:0.88rem;font-weight:700;color:#93c5fd;'>{prot}g</div>
      <div style='font-size:0.58rem;font-weight:700;letter-spacing:1px;text-transform:uppercase;
        color:rgba(147,197,253,0.55);'>Protein</div>
    </div>
    <div style='background:rgba(251,191,36,0.10);border:1px solid rgba(251,191,36,0.25);
      border-radius:8px;padding:6px 12px;text-align:center;'>
      <div style='font-size:0.88rem;font-weight:700;color:#fcd34d;'>{carb}g</div>
      <div style='font-size:0.58rem;font-weight:700;letter-spacing:1px;text-transform:uppercase;
        color:rgba(252,211,77,0.55);'>Carbs</div>
    </div>
    <div style='background:rgba(249,115,22,0.10);border:1px solid rgba(249,115,22,0.25);
      border-radius:8px;padding:6px 12px;text-align:center;'>
      <div style='font-size:0.88rem;font-weight:700;color:#fdba74;'>{fat}g</div>
      <div style='font-size:0.58rem;font-weight:700;letter-spacing:1px;text-transform:uppercase;
        color:rgba(253,186,116,0.55);'>Fats</div>
    </div>
    <div style='display:flex;align-items:center;gap:14px;margin-left:auto;
      font-size:0.72rem;color:rgba(255,255,255,0.35);'>
      {'<span>⏰ ' + time_ + '</span>' if time_ else ''}
      {'<span>🔪 ' + prep + '</span>' if prep else ''}
    </div>
  </div>

  <!-- Calorie bar -->
  <div style='background:rgba(255,255,255,0.06);border-radius:6px;height:4px;overflow:hidden;margin-bottom:12px;'>
    <div style='width:{pct}%;height:100%;background:{col};border-radius:6px;'></div>
  </div>

  <!-- Ingredients -->
  <div style='display:flex;flex-wrap:wrap;gap:5px;margin-bottom:12px;'>{ingr_html}</div>

  <!-- Tip -->
  {f"<div style='background:rgba(255,255,255,0.04);border-left:2px solid {col};border-radius:0 8px 8px 0;padding:8px 12px;font-size:0.78rem;color:rgba(255,255,255,0.50);'>💡 {tip}</div>" if tip else ""}
</div>
""", unsafe_allow_html=True)


# ── MACROS SUMMARY CARD ───────────────────────────────────────────────────────
def render_macros_summary(plan: dict):
    tc = plan.get("total_calories", 0)
    tp = plan.get("total_protein",  0)
    tcarb = plan.get("total_carbs", 0)
    tf = plan.get("total_fats",    0)
    p_pct = int(tp * 4 / max(tc, 1) * 100)
    c_pct = int(tcarb * 4 / max(tc, 1) * 100)
    f_pct = int(tf * 9 / max(tc, 1) * 100)

    meals = plan.get("meals", [])
    act_cal   = sum(m.get("calories", 0) for m in meals)
    act_prot  = sum(m.get("protein",  0) for m in meals)
    act_carbs = sum(m.get("carbs",    0) for m in meals)
    act_fat   = sum(m.get("fats",     0) for m in meals)

    hydration = plan.get("hydration_tip", "")

    st.markdown(f"""
<div class='plan-header'>
  <div style='display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;'>
    <div>
      <div style='font-size:0.68rem;font-weight:800;letter-spacing:3px;text-transform:uppercase;
        color:rgba(34,197,94,0.65);margin-bottom:4px;'>📊 Full Day Nutrition Summary</div>
      <div style='font-size:1.1rem;font-weight:700;color:#fff;'>{plan.get("plan_title","Your Meal Plan")}</div>
      <div style='font-size:0.78rem;color:rgba(255,255,255,0.40);margin-top:2px;'>
        {plan.get("cuisine","")} · {plan.get("diet","")} · {len(meals)} meals
      </div>
    </div>
    <div style='display:flex;gap:10px;flex-wrap:wrap;'>
      <div style='text-align:center;'>
        <div style='font-family:Bebas Neue,sans-serif;font-size:2rem;color:#22c55e;line-height:1;'>{act_cal}</div>
        <div style='font-size:0.60rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:rgba(34,197,94,0.55);'>kcal total</div>
      </div>
      <div style='width:1px;background:rgba(255,255,255,0.08);'></div>
      <div style='text-align:center;'>
        <div style='font-family:Bebas Neue,sans-serif;font-size:2rem;color:#93c5fd;line-height:1;'>{act_prot}g</div>
        <div style='font-size:0.60rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:rgba(147,197,253,0.55);'>protein</div>
      </div>
      <div style='text-align:center;'>
        <div style='font-family:Bebas Neue,sans-serif;font-size:2rem;color:#fcd34d;line-height:1;'>{act_carbs}g</div>
        <div style='font-size:0.60rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:rgba(252,211,77,0.55);'>carbs</div>
      </div>
      <div style='text-align:center;'>
        <div style='font-family:Bebas Neue,sans-serif;font-size:2rem;color:#fdba74;line-height:1;'>{act_fat}g</div>
        <div style='font-size:0.60rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:rgba(253,186,116,0.55);'>fats</div>
      </div>
    </div>
  </div>

  <!-- Macro bars -->
  <div style='margin-top:16px;display:flex;flex-direction:column;gap:8px;'>
    <div style='display:flex;align-items:center;gap:10px;'>
      <div style='font-size:0.70rem;font-weight:700;color:rgba(147,197,253,0.70);width:52px;text-align:right;'>PROTEIN</div>
      <div style='flex:1;background:rgba(255,255,255,0.06);border-radius:6px;height:7px;overflow:hidden;'>
        <div style='width:{p_pct}%;height:100%;background:#3b82f6;border-radius:6px;'></div>
      </div>
      <div style='font-size:0.70rem;color:rgba(255,255,255,0.35);width:32px;'>{p_pct}%</div>
    </div>
    <div style='display:flex;align-items:center;gap:10px;'>
      <div style='font-size:0.70rem;font-weight:700;color:rgba(252,211,77,0.70);width:52px;text-align:right;'>CARBS</div>
      <div style='flex:1;background:rgba(255,255,255,0.06);border-radius:6px;height:7px;overflow:hidden;'>
        <div style='width:{c_pct}%;height:100%;background:#f59e0b;border-radius:6px;'></div>
      </div>
      <div style='font-size:0.70rem;color:rgba(255,255,255,0.35);width:32px;'>{c_pct}%</div>
    </div>
    <div style='display:flex;align-items:center;gap:10px;'>
      <div style='font-size:0.70rem;font-weight:700;color:rgba(253,186,116,0.70);width:52px;text-align:right;'>FATS</div>
      <div style='flex:1;background:rgba(255,255,255,0.06);border-radius:6px;height:7px;overflow:hidden;'>
        <div style='width:{f_pct}%;height:100%;background:#f97316;border-radius:6px;'></div>
      </div>
      <div style='font-size:0.70rem;color:rgba(255,255,255,0.35);width:32px;'>{f_pct}%</div>
    </div>
  </div>

  {f"<div style='margin-top:14px;background:rgba(6,182,212,0.07);border:1px solid rgba(6,182,212,0.22);border-radius:10px;padding:10px 14px;font-size:0.80rem;color:rgba(255,255,255,0.55);'>💧 {hydration}</div>" if hydration else ""}
</div>
""", unsafe_allow_html=True)


# ── GENERATION LOGIC ──────────────────────────────────────────────────────────
if _generate:
    st.session_state.pop("mp_plan", None)   # clear previous
    with st.spinner("🍽️ AI is crafting your personalised meal plan…"):
        try:
            from model_api import query_model
            _prompt = build_meal_prompt(
                cuisine=_cuisine, diet=_diet, goal=_goal,
                calories=_calories, prot=_prot_g, carb=_carb_g, fat=_fat_g,
                allergies=_allergies, name=uname, weight=_user_weight
            )
            _raw = query_model(_prompt, max_tokens=2000).strip()

            # Strip markdown fences if present
            import re as _re
            _raw = _re.sub(r"^```(?:json)?\s*", "", _raw)
            _raw = _re.sub(r"\s*```$", "", _raw)

            _plan = json.loads(_raw)
            st.session_state["mp_plan"] = _plan

            # Save to history
            _history = st.session_state.get("mp_history", [])
            _history.insert(0, {
                "cuisine":  _cuisine,
                "diet":     _diet,
                "goal":     _goal,
                "calories": _calories,
                "title":    _plan.get("plan_title", f"{_cuisine} {_diet} Plan"),
                "plan":     _plan,
            })
            st.session_state["mp_history"] = _history[:6]   # keep last 6
            st.rerun()

        except json.JSONDecodeError:
            # Try to extract JSON from partial response
            try:
                _start = _raw.find("{")
                _end   = _raw.rfind("}") + 1
                if _start != -1 and _end > _start:
                    _plan = json.loads(_raw[_start:_end])
                    st.session_state["mp_plan"] = _plan
                    st.rerun()
                else:
                    st.error("AI returned an unexpected format. Please try again.")
            except Exception:
                st.error("Could not parse meal plan. Please try again.")
        except Exception as e:
            err = str(e)
            if "GROQ_API_KEY" in err or "API" in err.upper():
                st.error("⚠️ GROQ_API_KEY not set. Add it to HuggingFace Secrets.")
            else:
                st.error(f"Error generating meal plan: {err}")


# ── DISPLAY CURRENT PLAN ──────────────────────────────────────────────────────
_current_plan = st.session_state.get("mp_plan")

if _current_plan:
    render_macros_summary(_current_plan)

    _meals = _current_plan.get("meals", [])
    if _meals:
        # Two-column layout for cards
        _mc1, _mc2 = st.columns(2)
        for i, _meal in enumerate(_meals):
            with (_mc1 if i % 2 == 0 else _mc2):
                render_meal_card(_meal, _current_plan.get("total_calories", _calories))

    # Re-generate / Save buttons
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    _ra, _rb, _rc = st.columns([2, 2, 3])
    with _ra:
        if st.button("🔄 Regenerate Plan", key="mp_regen", use_container_width=True):
            st.session_state.pop("mp_plan", None)
            st.rerun()
    with _rb:
        if st.button("🗑️ Clear Plan", key="mp_clear", use_container_width=True):
            st.session_state.pop("mp_plan", None)
            st.rerun()
    with _rc:
        # Show shopping list
        if st.button("🛒 Show Shopping List", key="mp_shop", use_container_width=True):
            st.session_state["mp_show_shopping"] = not st.session_state.get("mp_show_shopping", False)

    # Shopping list
    if st.session_state.get("mp_show_shopping") and _meals:
        _all_ingr = []
        for _m in _meals:
            _all_ingr.extend(_m.get("ingredients", []))
        _unique_ingr = sorted(set(_all_ingr))
        st.markdown(f"""
<div style='background:rgba(4,18,8,0.88);border:1.5px solid rgba(34,197,94,0.22);
  border-radius:16px;padding:20px 24px;margin-top:12px;'>
  <div style='font-size:0.72rem;font-weight:800;letter-spacing:3px;text-transform:uppercase;
    color:rgba(34,197,94,0.65);margin-bottom:14px;'>🛒 Shopping List — {len(_unique_ingr)} items</div>
  <div style='display:flex;flex-wrap:wrap;gap:7px;'>
    {"".join(f"<span style='background:rgba(34,197,94,0.08);border:1px solid rgba(34,197,94,0.20);border-radius:20px;padding:4px 12px;font-size:0.78rem;color:rgba(255,255,255,0.70);'>✓ {i}</span>" for i in _unique_ingr)}
  </div>
</div>
""", unsafe_allow_html=True)

elif not _generate:
    # Empty state
    st.markdown("""
<div style='text-align:center;padding:50px 20px;'>
  <div style='font-size:3.5rem;margin-bottom:16px;'>🍽️</div>
  <div style='font-size:1.1rem;font-weight:700;color:rgba(255,255,255,0.55);margin-bottom:8px;'>
    Your meal plan will appear here</div>
  <div style='font-size:0.85rem;color:rgba(255,255,255,0.30);max-width:400px;margin:0 auto;'>
    Configure your cuisine, dietary preference, and calorie goal above — then hit Generate.</div>
</div>
""", unsafe_allow_html=True)


# ── RECENT PLANS HISTORY ──────────────────────────────────────────────────────
_history = st.session_state.get("mp_history", [])
if len(_history) > 1:
    st.markdown("""
<div style='font-size:0.72rem;font-weight:800;letter-spacing:3px;text-transform:uppercase;
  color:rgba(34,197,94,0.50);margin:28px 0 12px;display:flex;align-items:center;gap:10px;'>
  <span>🕐 Recent Plans</span>
  <span style='flex:1;height:1px;background:linear-gradient(90deg,rgba(34,197,94,0.20),transparent);display:block;'></span>
</div>""", unsafe_allow_html=True)

    _hcols = st.columns(min(3, len(_history) - 1))
    for _hi, _hitem in enumerate(_history[1:4]):   # skip current (index 0)
        with _hcols[_hi % 3]:
            _htitle  = _hitem.get("title", "Meal Plan")
            _hcal    = _hitem.get("calories", 0)
            _hcuisine= _hitem.get("cuisine", "")
            _hdiet   = _hitem.get("diet", "")
            if st.button(
                f"↩ {_htitle[:28]}…" if len(_htitle) > 28 else f"↩ {_htitle}",
                key=f"mp_hist_{_hi}",
                use_container_width=True,
                help=f"{_hcuisine} · {_hdiet} · {_hcal} kcal"
            ):
                st.session_state["mp_plan"] = _hitem["plan"]
                st.rerun()