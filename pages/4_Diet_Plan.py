# -*- coding: utf-8 -*-
"""
pages/4_diet_unified.py — Complete Diet Plan Page
Fixed: water tracker glass animation, smart grocery ingredient extraction
"""
import streamlit as st
import os, sys, json as _json, re as _re
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(
    page_title="FitPlan Pro - Diet Plan", page_icon="🥗",
    layout="wide", initial_sidebar_state="collapsed"
)
if not st.session_state.get("logged_in"):     st.switch_page("app.py")
if "user_data" not in st.session_state:        st.switch_page("pages/1_Profile.py")

uname        = st.session_state.get("username", "Athlete")
data         = st.session_state.user_data
_dn          = data.get("display_name", "").strip() or data.get("name", "").strip() or uname
_display     = _dn if "@" not in _dn else uname
sdays        = st.session_state.get("structured_days", [])
plan_id      = st.session_state.get("plan_id", "")
today_str    = date.today().isoformat()
dietary_type = st.session_state.get("dietary_type", "veg")
if not dietary_type:
    dietary_type = "veg"
    st.session_state.dietary_type = "veg"

# ══════════════════════════════════════════════════════════════════════════════
# THEME CONFIG
# ══════════════════════════════════════════════════════════════════════════════
THEME = {
    "veg": {
        "icon": "🥦", "label": "Vegetarian",
        "accent": "#22c55e", "rgb": "34,197,94",
        "logo_color": "#22c55e", "logo_glow": "rgba(34,197,94,0.60)",
        "bg_url": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=1800&q=80&auto=format&fit=crop",
        "overlay": "rgba(0,30,5,0.52)", "tab_bg": "rgba(6,30,15,0.80)",
        "tips": [
            "💧 Drink 2–3 litres of water daily",
            "⏰ Eat every 3–4 hours to maintain energy",
            "🥦 Include protein in every meal (dal, paneer, tofu)",
            "☀️ Eat your largest meal at lunch",
            "🌈 Add colour to your plate — eat the rainbow",
            "🚫 Avoid processed foods and refined sugar",
            "💪 Pair carbs with protein for better absorption",
        ],
    },
    "nonveg": {
        "icon": "🍗", "label": "Non-Vegetarian",
        "accent": "#f97316", "rgb": "249,115,22",
        "logo_color": "#f97316", "logo_glow": "rgba(249,115,22,0.60)",
        "bg_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=1800&q=80&auto=format&fit=crop",
        "overlay": "rgba(40,15,4,0.52)", "tab_bg": "rgba(40,15,4,0.80)",
        "tips": [
            "💧 Drink 3 litres of water daily — protein needs hydration",
            "🥩 Eat lean protein within 30 mins post workout",
            "🍳 Grill or bake — avoid deep frying",
            "🥦 Include 2–3 servings of vegetables per meal",
            "⏰ Space meals 3–4 hours apart for metabolism",
            "🐟 Choose fish twice a week for omega-3",
            "🔴 Limit red meat to 2–3 times per week",
        ],
    },
    "both": {
        "icon": "🌿🍗", "label": "Flexible",
        "accent": "#facc15", "rgb": "250,204,21",
        "logo_color": "#facc15", "logo_glow": "rgba(250,204,21,0.55)",
        "bg_url": "https://images.unsplash.com/photo-1498837167922-ddd27525d352?w=1800&q=80&auto=format&fit=crop",
        "overlay": "rgba(20,35,8,0.52)", "tab_bg": "rgba(20,35,8,0.80)",
        "tips": [
            "💧 Drink 2.5–3 litres of water daily",
            "🥦 Fill half your plate with vegetables",
            "🌿🍗 Alternate veg & non-veg days for variety",
            "⏰ Eat every 3–4 hours to keep metabolism active",
            "🚫 Limit processed foods and refined carbs",
            "🥩 Post-workout: lean protein within 30 mins",
            "🍎 Snack on fruits, nuts, and yoghurt",
        ],
    },
}

cfg    = THEME.get(dietary_type, THEME["veg"])
accent = cfg["accent"]
rgb    = cfg["rgb"]

# ── Background ────────────────────────────────────────────────────────────────
_bg_url = cfg["bg_url"]
st.markdown(
    "<style>"
    "html,body,.stApp{background:#050202!important;color:#fff!important;}"
    "[data-testid='stAppViewContainer']::before{"
    "content:'';position:fixed;inset:0;z-index:0;"
    "background:url('" + _bg_url + "') center center/cover no-repeat;"
    "filter:blur(8px) brightness(0.25) saturate(0.55);"
    "transform:scale(1.06);}"
    "[data-testid='stAppViewContainer']{"
    "background:linear-gradient(160deg,rgba(3,1,0,0.88) 0%,rgba(4,2,0,0.80) 50%,rgba(3,1,0,0.92) 100%)!important;"
    "position:relative;}"
    "[data-testid='stAppViewContainer']>section>div.block-container{"
    "position:relative;z-index:2;}"
    "</style>", unsafe_allow_html=True)

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow+Condensed:wght@700;800;900&family=DM+Sans:opsz,wght@9..40,400;9..40,600;9..40,700&display=swap');
#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stDecoration"],
[data-testid="stSidebarNav"],[data-testid="collapsedControl"],
section[data-testid="stSidebar"],button[kind="header"]{{display:none!important;}}
html,body,.stApp{{background-color:transparent!important;color:#fff!important;font-family:'DM Sans',sans-serif!important;}}
[data-testid="stAppViewContainer"]>section>div.block-container{{
  max-width:1200px!important;margin:0 auto!important;padding:0 32px 80px!important;background:transparent!important;}}
[data-testid="stWidgetLabel"],[data-testid="stWidgetLabel"] p{{color:rgba(255,255,255,0.80)!important;}}
.stButton>button{{
  background:linear-gradient(135deg,{accent},rgba({rgb},0.80))!important;
  border:none!important;color:#fff!important;border-radius:8px!important;
  font-family:'DM Sans',sans-serif!important;font-size:1.00rem!important;font-weight:700!important;
  box-shadow:0 4px 16px rgba({rgb},0.35)!important;transition:all 0.20s!important;}}
.stButton>button:hover{{transform:translateY(-2px)!important;box-shadow:0 6px 24px rgba({rgb},0.60)!important;}}
.stTabs [data-baseweb="tab-list"]{{
  background:{cfg["tab_bg"]}!important;border-radius:10px!important;
  padding:4px!important;border:1px solid rgba({rgb},0.25)!important;}}
.stTabs [data-baseweb="tab"]{{
  background:transparent!important;color:rgba(255,255,255,0.90)!important;
  border-radius:7px!important;font-size:0.75rem!important;font-weight:600!important;padding:8px 14px!important;}}
.stTabs [aria-selected="true"]{{
  background:linear-gradient(135deg,{accent},rgba({rgb},0.75))!important;
  color:#fff!important;box-shadow:0 3px 12px rgba({rgb},0.50)!important;}}
.stCheckbox>label{{color:#fff!important;font-weight:500!important;}}
.stExpander{{
  background:rgba(0,0,0,0.65)!important;border:1.5px solid rgba(255,255,255,0.18)!important;
  border-radius:14px!important;backdrop-filter:blur(30px)!important;}}
.stExpander:hover{{border-color:rgba({rgb},0.45)!important;}}
.stExpander details summary{{color:#fff!important;font-weight:700!important;font-size:1.05rem!important;padding:14px 18px!important;}}
.stExpander details summary:hover,.stExpander details[open] summary{{color:{accent}!important;}}
.swap-mini .stButton>button{{
  background:rgba({rgb},0.15)!important;border:1px solid rgba({rgb},0.40)!important;
  color:rgba(255,255,255,0.85)!important;font-size:0.65rem!important;font-weight:700!important;
  padding:3px 10px!important;height:auto!important;border-radius:6px!important;
  box-shadow:none!important;text-transform:uppercase!important;letter-spacing:0.5px!important;}}
.swap-mini .stButton>button:hover{{background:rgba({rgb},0.35)!important;transform:none!important;}}
.meal-card{{
  background:rgba(0,0,0,0.78)!important;border:1.5px solid rgba({rgb},0.28)!important;
  border-radius:14px;padding:16px 20px;margin-bottom:10px;
  position:relative;overflow:hidden;backdrop-filter:blur(28px);}}
.meal-card::before{{content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,transparent,rgba({rgb},0.60),transparent);}}
.meal-label{{
  font-size:0.85rem;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;
  color:rgba({rgb},0.90);margin-bottom:8px;display:flex;align-items:center;justify-content:space-between;}}
.meal-text{{color:#fff!important;font-size:0.92rem!important;line-height:1.65;
  text-shadow:0 1px 4px rgba(0,0,0,0.90)!important;}}
.tip-card{{
  background:rgba(0,0,0,0.60);border:1px solid rgba({rgb},0.22);
  border-radius:10px;padding:10px 14px;margin-bottom:8px;
  font-size:1.00rem;color:rgba(255,255,255,0.75);}}
.feature-card{{
  background:rgba(0,0,0,0.78)!important;border:1.5px solid rgba(255,255,255,0.20)!important;
  border-radius:14px;padding:20px 18px;height:100%;backdrop-filter:blur(28px);transition:border-color 0.2s;}}
.feature-card:hover{{border-color:rgba({rgb},0.45);}}
.feature-card-title{{
  font-size:0.85rem;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;
  color:rgba({rgb},0.90)!important;margin-bottom:12px;}}
.prog-bar-bg{{height:5px;background:rgba(255,255,255,0.10);border-radius:3px;overflow:hidden;margin-top:6px;}}
.prog-bar-fill{{height:100%;background:linear-gradient(90deg,{accent},rgba({rgb},0.70));border-radius:3px;}}
.stNumberInput>div>div>input,.stTextInput>div>div>input,.stTextArea>div>div>textarea{{
  background:rgba(0,0,0,0.75)!important;border:1.5px solid rgba(255,255,255,0.22)!important;
  color:#fff!important;border-radius:14px!important;backdrop-filter:blur(28px)!important;}}
[data-baseweb="select"]>div{{
  background:rgba(0,0,0,0.75)!important;border:1.5px solid rgba(255,255,255,0.22)!important;
  border-radius:14px!important;backdrop-filter:blur(28px)!important;color:#fff!important;}}
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"] > button{{
  background:rgba(18,4,4,0.82)!important;border:1.5px solid rgba(229,9,20,0.35)!important;
  color:rgba(255,255,255,0.80)!important;border-radius:9px!important;
  font-size:0.85rem!important;font-weight:700!important;height:32px!important;animation:none!important;
  box-shadow:none!important;}}
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"] > button:hover{{
  background:rgba(229,9,20,0.22)!important;border-color:rgba(229,9,20,0.70)!important;color:#fff!important;}}
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"]:last-child > button{{
  background:rgba(60,5,5,0.70)!important;color:rgba(255,120,120,0.90)!important;animation:none!important;}}
html,body,.stApp,.stMarkdown,p,div,span,label{{text-shadow:0 2px 6px rgba(0,0,0,0.98)!important;}}
[data-testid="stWidgetLabel"],[data-testid="stWidgetLabel"] p{{color:#fff!important;font-size:0.88rem!important;font-weight:700!important;text-shadow:0 2px 8px rgba(0,0,0,0.99)!important;}}
.stCheckbox>label,.stCheckbox>label p{{color:#fff!important;font-weight:700!important;font-size:1.05rem!important;text-shadow:0 2px 8px rgba(0,0,0,0.99)!important;}}
.stTabs [data-baseweb="tab"]{{color:rgba(255,255,255,0.92)!important;font-size:0.95rem!important;font-weight:700!important;text-shadow:0 2px 6px rgba(0,0,0,0.95)!important;}}
.stExpander details summary{{color:#fff!important;font-size:1.05rem!important;font-weight:700!important;text-shadow:0 2px 6px rgba(0,0,0,0.95)!important;}}
.stMarkdown p,.stMarkdown li{{color:#fff!important;font-size:1.05rem!important;line-height:1.75!important;text-shadow:0 2px 8px rgba(0,0,0,0.99)!important;}}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# NAV
# ══════════════════════════════════════════════════════════════════════════════
try:
    from nav_component import render_nav as _render_nav
    _render_nav("diet", uname)
except ImportError:
    from auth_token import logout
    _n = st.columns([1.6,1,1,1,1,1,1,1,1.2])
    with _n[0]:
        st.markdown(
            f"<div style='font-family:Bebas Neue,sans-serif;font-size:1.5rem;letter-spacing:5px;"
            f"color:{cfg['logo_color']};text-shadow:0 0 20px {cfg['logo_glow']};line-height:1;"
            f"padding-top:4px'>{cfg['icon']} FITPLAN PRO</div>",
            unsafe_allow_html=True
        )
    nav_items = [
        ("Home",     "pages/2_Dashboard.py",      "fd_db"),
        ("Workout",  "pages/3_Workout_Plan.py",   "fd_wp"),
        ("● Diet",   "pages/4_Diet_Plan.py",      "fd_dp"),
        ("🍽️ Meals", "pages/11_meal_planner.py",  "fd_mp"),
        ("AI Coach", "pages/5_ai_coach.py",        "fd_ai"),
        ("Records",  "pages/6_records.py",         "fd_rc"),
        ("Photos",   "pages/7_progress_photos.py", "fd_ph"),
    ]
    for i, (lbl, path, key) in enumerate(nav_items):
        with _n[i+1]:
            if st.button(lbl, key=key, use_container_width=True):
                try: st.switch_page(path)
                except Exception: pass
    with _n[8]:
        if st.button("Sign Out", key="fd_so", use_container_width=True):
            logout(uname)
            for k in ["logged_in","username","auth_token","user_data","workout_plan","structured_days",
                      "dietary_type","full_plan_data","plan_id","plan_start","plan_duration","plan_for",
                      "force_regen","tracking","_plan_checked","_db_loaded_dash"]:
                st.session_state.pop(k, None)
            st.switch_page("app.py")

# ══════════════════════════════════════════════════════════════════════════════
# HERO
# ══════════════════════════════════════════════════════════════════════════════
uname_up   = _display.upper() if '@' not in _display else uname.upper()
diet_icons = {"veg":"&#127807;","nonveg":"&#127829;","both":"&#127807;&#127829;"}
d_icon     = diet_icons.get(dietary_type, "&#127807;")

st.markdown(
    f"<div style='background:rgba(0,0,0,0.58);border:1.5px solid rgba({rgb},0.40);"
    f"border-radius:20px;padding:28px 36px;margin-bottom:20px;backdrop-filter:blur(14px);"
    f"position:relative;overflow:hidden'>"
    f"<div style='position:absolute;top:0;left:0;right:0;height:2px;"
    f"background:linear-gradient(90deg,transparent,{accent},transparent)'></div>"
    f"<div style='position:absolute;top:16px;right:24px;font-size:0.85rem;font-weight:700;"
    f"letter-spacing:2px;color:rgba({rgb},0.80);background:rgba({rgb},0.12);"
    f"border:1px solid rgba({rgb},0.30);border-radius:20px;padding:4px 14px'>{d_icon} {cfg['label']}</div>"
    f"<div style='font-size:0.85rem;font-weight:700;letter-spacing:4px;text-transform:uppercase;"
    f"color:rgba({rgb},0.80);margin-bottom:10px'>Personalised Nutrition Plan</div>"
    f"<div style='font-family:Barlow Condensed,sans-serif;font-size:clamp(2rem,5vw,3.4rem);"
    f"font-weight:900;text-transform:uppercase;color:#fff;line-height:1;margin-bottom:12px'>"
    f"{uname_up}'s <span style='color:{accent}'>Diet Plan</span></div>"
    f"<div style='display:flex;gap:12px;flex-wrap:wrap'>"
    f"<span style='background:rgba({rgb},0.15);border:1px solid rgba({rgb},0.35);"
    f"border-radius:20px;padding:4px 14px;font-size:1.05rem;font-weight:600;color:{accent}'>"
    f"{d_icon} {cfg['label']}</span>"
    f"<span style='font-size:1.00rem;color:rgba(255,255,255,0.90);align-self:center'>"
    f"Goal: {data.get('goal','Fitness')} &middot; {len(sdays)} days</span>"
    f"</div></div>",
    unsafe_allow_html=True
)

if not sdays:
    st.markdown(
        "<div style='text-align:center;padding:60px 20px'>"
        "<div style='font-size:3rem;margin-bottom:14px'>🥗</div>"
        "<div style='font-family:Bebas Neue,sans-serif;font-size:1.8rem;color:#E50914;"
        "letter-spacing:2px;margin-bottom:8px'>No Plan Found</div>"
        "<div style='font-size:0.85rem;color:rgba(255,255,255,0.90);margin-bottom:24px'>"
        "Generate your personalised plan first from the Profile page.</div></div>",
        unsafe_allow_html=True
    )
    if st.button("👤 Go to Profile"): st.switch_page("pages/1_Profile.py")
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# WATER TRACKER — Animated glass UI, fixed rerun
# ══════════════════════════════════════════════════════════════════════════════
water_key = f"water_{uname}_{today_str}"
if water_key not in st.session_state:
    try:
        from utils.db import get_water as _gw
        st.session_state[water_key] = _gw(uname, today_str)
    except Exception:
        st.session_state[water_key] = 0

glasses = st.session_state[water_key]
goal_w  = 8
pct_w   = min(int(glasses / goal_w * 100), 100)

st.markdown(
    "<div style='font-size:0.85rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;"
    "color:rgba(229,9,20,0.75);margin:16px 0 8px;display:flex;align-items:center;gap:8px'>"
    "<span style='width:16px;height:1.5px;background:#E50914;display:block'></span>"
    "💧 Water Intake Tracker</div>",
    unsafe_allow_html=True
)

# Build animated glass grid
glass_html = ""
for gi in range(goal_w):
    filled = gi < glasses
    if filled:
        glass_html += (
            f"<div style='position:relative;width:52px;height:72px;'>"
            f"<div style='position:absolute;inset:0;border-radius:4px 4px 12px 12px;"
            f"background:rgba(96,165,250,0.15);border:2px solid rgba(56,189,248,0.70);overflow:hidden'>"
            f"<div style='position:absolute;bottom:0;left:0;right:0;height:78%;"
            f"background:linear-gradient(180deg,rgba(56,189,248,0.80) 0%,rgba(14,165,233,0.95) 100%);'>"
            f"</div>"
            f"<div style='position:absolute;inset:0;display:flex;align-items:center;"
            f"justify-content:center;font-size:1.3rem;z-index:2'>💧</div>"
            f"</div>"
            f"<div style='position:absolute;top:-10px;left:50%;transform:translateX(-50%);"
            f"font-size:0.65rem;font-weight:800;color:#38bdf8;letter-spacing:1px'>{gi+1}</div>"
            f"</div>"
        )
    else:
        glass_html += (
            f"<div style='position:relative;width:52px;height:72px;'>"
            f"<div style='position:absolute;inset:0;border-radius:4px 4px 12px 12px;"
            f"background:rgba(255,255,255,0.03);border:2px dashed rgba(255,255,255,0.18);"
            f"display:flex;align-items:center;justify-content:center;'>"
            f"<span style='font-size:1.1rem;opacity:0.20'>🥛</span>"
            f"</div>"
            f"<div style='position:absolute;top:-10px;left:50%;transform:translateX(-50%);"
            f"font-size:0.65rem;font-weight:800;color:rgba(255,255,255,0.22);letter-spacing:1px'>{gi+1}</div>"
            f"</div>"
        )

bar_color  = "#22c55e" if glasses >= goal_w else "#38bdf8"
bar_label  = "🎉 Daily goal reached! Excellent hydration!" if glasses >= goal_w \
             else f"💧 {goal_w - glasses} more glass{'es' if goal_w-glasses>1 else ''} to reach your goal"

st.markdown(f"""
<div style='background:rgba(0,20,40,0.72);border:1.5px solid rgba(96,165,250,0.38);
  border-radius:18px;padding:20px 24px;margin-bottom:12px;backdrop-filter:blur(20px);
  position:relative;overflow:hidden'>
  <div style='position:absolute;top:0;left:0;right:0;height:2px;
    background:linear-gradient(90deg,transparent,#38bdf8,transparent)'></div>
  <div style='display:flex;align-items:center;justify-content:space-between;margin-bottom:16px'>
    <div>
      <div style='font-size:0.85rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;
        color:rgba(96,165,250,0.90)'>Today's Water Intake</div>
      <div style='font-size:0.80rem;color:rgba(255,255,255,0.50);margin-top:2px'>
        Goal: 8 glasses · {today_str}</div>
    </div>
    <div style='text-align:right'>
      <div style='font-family:Bebas Neue,sans-serif;font-size:3rem;line-height:1;
        color:{bar_color}'>{glasses}</div>
      <div style='font-size:0.75rem;color:rgba(255,255,255,0.45);letter-spacing:1px'>OF {goal_w} GLASSES</div>
    </div>
  </div>
  <div style='display:flex;gap:8px;align-items:flex-end;margin-bottom:16px;flex-wrap:wrap'>
    {glass_html}
  </div>
  <div style='height:8px;background:rgba(255,255,255,0.08);border-radius:4px;overflow:hidden;margin-bottom:10px'>
    <div style='height:100%;width:{pct_w}%;background:linear-gradient(90deg,#38bdf8,{bar_color});
      border-radius:4px'></div>
  </div>
  <div style='display:flex;align-items:center;justify-content:space-between;
    font-size:0.85rem;color:rgba(255,255,255,0.75)'>
    <span>{bar_label}</span>
    <span style='font-weight:700;color:{bar_color}'>{pct_w}%</span>
  </div>
</div>
""", unsafe_allow_html=True)

wc1, wc2, _ = st.columns([2, 2, 6])
with wc1:
    if st.button("💧 + 1 Glass", key="water_add", use_container_width=True):
        st.session_state[water_key] = min(glasses + 1, 20)
        try:
            from utils.db import save_water as _sw
            _sw(uname, today_str, st.session_state[water_key])
        except Exception: pass
        st.rerun()
with wc2:
    if glasses > 0 and st.button("↩ Undo", key="water_undo", use_container_width=True):
        st.session_state[water_key] = max(glasses - 1, 0)
        try:
            from utils.db import save_water as _sw2
            _sw2(uname, today_str, st.session_state[water_key])
        except Exception: pass
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# FEATURE CARDS — Grocery / Supplement / Weekly Adherence
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
fe1, fe2, fe3 = st.columns(3)

# ── Smart ingredient extractor ────────────────────────────────────────────────
_STOPWORDS = {
    "cup","cups","tbsp","tsp","gram","grams","g","kg","ml","oz","lb","lbs",
    "handful","slice","slices","piece","pieces","bowl","plate","glass",
    "tablespoon","tablespoons","teaspoon","teaspoons","serving","servings",
    "grilled","baked","boiled","steamed","fried","roasted","cooked","mixed",
    "chopped","diced","sliced","mashed","blended","sauteed","poached","raw",
    "scrambled","topped","served","drizzled","seasoned","garnished","warm",
    "hot","cold","cool","chilled","fresh","frozen","dried","canned","whole",
    "lean","light","dark","medium","large","small","half","full","extra",
    "high","low","rich","good","best","mild","spicy","sweet","salty","soft",
    "crispy","thick","thin","plain","optional","homemade","classic",
    "breakfast","lunch","dinner","snack","snacks","meal","meals","dish","side",
    "salad","soup","curry","rice","bread","roti","toast","bowl","wrap","roll",
    "include","add","serve","use","make","cook","prepare","mix","season",
    "with","and","or","the","for","of","in","on","to","a","an","is","are",
    "plus","along","before","after","during","based","topped","from","into",
    "protein","carbs","carb","calories","calorie","macro","fiber","fat","sugar",
    "sodium","vitamin","mineral","omega","amino","daily","weekly","approximately",
}

_MULTI_WORD = [
    "brown rice","white rice","basmati rice","jasmine rice",
    "whole wheat","greek yogurt","sweet potato","olive oil",
    "coconut oil","chia seeds","flax seeds","pumpkin seeds",
    "sunflower seeds","black beans","kidney beans","chickpeas",
    "mixed nuts","green tea","black tea","protein powder",
    "almond milk","coconut milk","cottage cheese","cream cheese",
    "peanut butter","almond butter","soy sauce","fish sauce",
    "oyster sauce","red pepper","green pepper","bell pepper",
    "spring onion","green onion","red onion",
    "urad dal","moong dal","chana dal","toor dal","masoor dal",
    "paneer","tofu","tempeh","edamame",
    "chicken breast","chicken thigh","ground chicken",
    "salmon fillet","tuna","cod","tilapia","prawns","shrimp",
    "egg whites","whole eggs","boiled eggs",
    "multigrain bread","whole grain","oat bran","rolled oats",
    "greek yogurt","low fat yogurt",
]

def _extract_ingredients(meal_text):
    if not meal_text: return set()
    items = set()
    text_lower = meal_text.lower()

    # 1. Known multi-word ingredients
    for mw in _MULTI_WORD:
        if mw in text_lower:
            items.add(mw.title())

    # 2. quantity + food patterns: "150g chicken", "2 eggs", "1 cup oats"
    qty_pattern = _re.findall(
        r'(\d+(?:\.\d+)?(?:g|kg|ml|l|oz|lb|cups?|tbsp|tsp|pieces?)?\.?\s*)'
        r'([a-zA-Z][a-zA-Z\s]{2,20}?)(?=\s*[,\(\|]|\s+and\s|\s+with\s|$)',
        meal_text, _re.IGNORECASE
    )
    for qty, food in qty_pattern:
        food = food.strip().lower()
        words = [w for w in food.split() if w not in _STOPWORDS and len(w) > 2]
        if words:
            candidate = " ".join(words).strip()
            if candidate and len(candidate) > 2:
                items.add(candidate.title())

    # 3. Capitalized food words
    cap_words = _re.findall(r'\b([A-Z][a-z]{3,})\b', meal_text)
    for w in cap_words:
        wl = w.lower()
        if wl not in _STOPWORDS and len(wl) > 3 and not wl.endswith("ing") and not wl.endswith("ed"):
            items.add(w)

    # 4. After separators: "with X", "and X"
    after = _re.findall(
        r'(?:with|and|\+)\s+([a-zA-Z][a-zA-Z\s]{2,18}?)(?=\s*[,\(\|]|$)',
        meal_text, _re.IGNORECASE
    )
    for p in after:
        words = [w for w in p.strip().lower().split() if w not in _STOPWORDS and len(w) > 2]
        candidate = " ".join(words).strip()
        if candidate and len(candidate) > 3:
            items.add(candidate.title())

    # Filter out cooking methods and non-food
    filtered = set()
    for item in items:
        il = item.lower()
        if (len(il) > 3
                and il not in _STOPWORDS
                and not any(x in il for x in ["cook","bak","grill","steam","fry","boil","roast","serv"])):
            filtered.add(item)
    return filtered

def _grocery_icon(item):
    il = item.lower()
    if any(x in il for x in ["chicken","fish","salmon","tuna","prawn","shrimp","cod","tilapia"]): return "🍗"
    if any(x in il for x in ["egg","eggs"]): return "🥚"
    if any(x in il for x in ["paneer","tofu","dal","bean","lentil","chickpea","legume","tempeh"]): return "🫘"
    if any(x in il for x in ["rice","oat","bread","roti","wheat","grain","pasta","noodle","quinoa"]): return "🌾"
    if any(x in il for x in ["milk","yogurt","curd","cheese","butter","cream","ghee","whey"]): return "🥛"
    if any(x in il for x in ["spinach","broccoli","carrot","onion","tomato","pepper","cabbage",
                               "lettuce","kale","cucumber","zucchini","peas","corn","mushroom"]): return "🥦"
    if any(x in il for x in ["apple","banana","mango","orange","berry","fruit","grape","lemon",
                               "lime","watermelon","strawberry","blueberry"]): return "🍎"
    if any(x in il for x in ["almond","walnut","cashew","nut","seed","peanut","pistachio"]): return "🥜"
    if any(x in il for x in ["oil","olive","coconut","sauce","spice","masala","turmeric","cumin",
                               "ginger","garlic","pepper","coriander","cardamom","cinnamon"]): return "🫙"
    if any(x in il for x in ["honey","sugar","jaggery","maple"]): return "🍯"
    return "🛒"

# Collect all ingredients from plan (next 7 days)
all_ingredients = {}
for sd in sdays[:7]:
    for meal_type, meal_txt in sd.get("dietary", {}).items():
        if not meal_txt: continue
        found = _extract_ingredients(str(meal_txt))
        for ing in found:
            if ing not in all_ingredients:
                all_ingredients[ing] = set()
            all_ingredients[ing].add(meal_type)

sorted_ingredients = sorted(all_ingredients.keys())[:35]

with fe1:
    with st.expander("🛒  Grocery List — Next 7 Days", expanded=False):
        if sorted_ingredients:
            total_items = len(sorted_ingredients)
            done_items  = sum(1 for i in sorted_ingredients
                              if st.session_state.get(f"grocery_{uname}_{i}", False))

            st.markdown(
                f"<div style='display:flex;align-items:center;justify-content:space-between;margin-bottom:12px'>"
                f"<div style='font-size:0.80rem;color:rgba(255,255,255,0.65)'>✓ Tap to cross off while shopping</div>"
                f"<div style='font-size:0.80rem;font-weight:700;color:{accent}'>"
                f"{done_items}/{total_items} items</div></div>",
                unsafe_allow_html=True
            )

            for item in sorted_ingredients:
                g_key   = f"grocery_{uname}_{item}"
                checked = st.session_state.get(g_key, False)
                strike  = "text-decoration:line-through;opacity:0.35;" if checked else ""
                icon    = _grocery_icon(item)
                meals_in = all_ingredients.get(item, set())
                meal_tag = ", ".join(sorted(meals_in))

                c_item, c_check = st.columns([5, 1])
                with c_item:
                    _item_color = "rgba(255,255,255,0.35)" if checked else "#fff"
                    st.markdown(
                        f"<div style='display:flex;align-items:center;gap:10px;padding:7px 4px;"
                        f"border-bottom:1px solid rgba(255,255,255,0.06)'>"
                        f"<span style='font-size:1.1rem;flex-shrink:0'>{icon}</span>"
                        f"<div>"
                        f"<div style='font-size:0.90rem;font-weight:600;"
                        f"color:{_item_color};{strike}'>{item}</div>"
                        f"<div style='font-size:0.68rem;color:rgba(255,255,255,0.30);"
                        f"text-transform:capitalize'>{meal_tag}</div>"
                        f"</div></div>",
                        unsafe_allow_html=True
                    )
                with c_check:
                    new_val = st.checkbox("", value=checked, key=g_key+"_cb",
                                          label_visibility="collapsed")
                    if new_val != checked:
                        st.session_state[g_key] = new_val
                        st.rerun()

            if done_items > 0:
                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                if st.button(
                    f"🗑 Clear {done_items} checked item{'s' if done_items>1 else ''}",
                    key="grocery_clear", use_container_width=True
                ):
                    for i in sorted_ingredients:
                        st.session_state[f"grocery_{uname}_{i}"] = False
                    st.rerun()

            st.markdown(
                f"<div style='margin-top:10px;background:rgba({rgb},0.08);"
                f"border:1px solid rgba({rgb},0.20);border-radius:10px;"
                f"padding:8px 12px;font-size:0.75rem;color:rgba(255,255,255,0.60)'>"
                f"📋 {total_items} ingredients from your actual AI meal plan · {min(len(sdays),7)} days</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                "<div style='color:rgba(255,255,255,0.60);font-size:0.90rem;"
                "padding:12px 0;text-align:center'>"
                "No plan found. Generate your plan first to see your grocery list.</div>",
                unsafe_allow_html=True
            )

with fe2:
    with st.expander("💊  Supplement Guide", expanded=False):
        supp_key = f"supp_{uname}"
        if not st.session_state.get(supp_key):
            try:
                from utils.db import get_user_setting
                _db_supp = get_user_setting(uname, "supplement_guide")
                if _db_supp: st.session_state[supp_key] = _db_supp
            except Exception: pass
        if not st.session_state.get(supp_key):
            if st.button("Get AI Guide", key="supp_btn", use_container_width=True):
                with st.spinner("Generating personalised guide..."):
                    try:
                        from model_api import query_model
                        prompt = (
                            f"You are a fitness nutritionist. List exactly 5 supplements for a "
                            f"{data.get('level','Beginner')} {cfg['label']} person whose goal is {data.get('goal','Fitness')}. "
                            "STRICT FORMAT — use exactly this pattern for each line:\n"
                            "SUPPLEMENT NAME: dosage — one sentence benefit\n"
                            "Example: Creatine Monohydrate: 5g daily — boosts strength and muscle recovery.\n"
                            "Rules: plain text only, no JSON, no curly braces, no markdown, no numbering, no extra commentary."
                        )
                        raw = query_model(prompt, max_tokens=300).strip()
                        # Strip any JSON that slips through
                        import re as _re2
                        if raw.strip().startswith(("{","[")):
                            raw = "Could not generate guide in correct format. Please try again."
                        else:
                            _slines = [l for l in raw.splitlines()
                                       if not re.match(r'^\s*[{\[\]}\]],?\s*$', l)
                                       and not re.match(r'^\s*"[^"]+"\s*:\s*', l)]
                            raw = "\n".join(_slines).strip()
                        st.session_state[supp_key] = raw
                        try:
                            from utils.db import save_user_setting
                            save_user_setting(uname, "supplement_guide", raw)
                        except Exception: pass
                        st.rerun()
                    except Exception:
                        st.error("Could not generate guide. Try again.")
        else:
            raw_supp = st.session_state[supp_key]
            lines = []
            for line in raw_supp.splitlines():
                line = line.strip().lstrip("-*1234567890. ")
                if not line: continue
                if ":" in line:
                    parts = line.split(":", 1)
                    lines.append((parts[0].strip(), parts[1].strip()))
                else:
                    lines.append(("", line))
            for name, desc in lines[:5]:
                st.markdown(
                    "<div style='padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.10)'>"
                    + (f"<b style='color:{accent};font-size:0.85rem'>{name}</b><br>" if name else "")
                    + f"<span style='font-size:1.00rem;color:#fff;line-height:1.5'>{desc}</span></div>",
                    unsafe_allow_html=True
                )
            if st.button("↻ Refresh", key="supp_refresh"):
                st.session_state.pop(supp_key, None)
                st.rerun()

with fe3:
    with st.expander("📊  Weekly Adherence", expanded=False):
        done_m = 0; total_m = 0
        for i, sd in enumerate(sdays[:7]):
            dn2 = sd.get("day", i+1)
            for meal in sd.get("dietary", {}):
                total_m += 1
                if st.session_state.get(f"meal_d{dn2}_{meal}", False):
                    done_m += 1
        adh   = int(done_m / max(total_m, 1) * 100)
        col_a = "#22c55e" if adh >= 70 else ("#fbbf24" if adh >= 40 else "#ef4444")
        st.markdown(
            f"<div style='text-align:center;padding:8px 0'>"
            f"<div style='font-family:Bebas Neue,sans-serif;font-size:3.5rem;color:{col_a};line-height:1'>{adh}%</div>"
            f"<div style='font-size:1.05rem;color:#fff;margin-top:6px;font-weight:600'>Weekly Diet Adherence</div>"
            f"<div style='font-size:0.85rem;color:rgba(255,255,255,0.70);margin-top:4px'>{done_m} of {total_m} meals tracked</div>"
            f"<div class='prog-bar-bg' style='margin-top:10px'>"
            f"<div style='height:100%;width:{adh}%;background:{col_a};border-radius:3px'></div>"
            f"</div></div>",
            unsafe_allow_html=True
        )

# ══════════════════════════════════════════════════════════════════════════════
# DAY TABS — Meal cards + swap + nutrition summary + tips
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(
    f"<div style='font-size:0.85rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;"
    f"color:rgba({rgb},0.80);margin:20px 0 10px;display:flex;align-items:center;gap:8px'>"
    f"<span style='width:16px;height:1.5px;background:{accent};display:block'></span>"
    f"Your Meal Plan by Day</div>",
    unsafe_allow_html=True
)

MEAL_ICONS = {"breakfast":"🌅","lunch":"☀️","dinner":"🌙","snacks":"🍎"}

tab_labels = [
    "Day " + str(d.get("day", i+1)) + (" 😴" if d.get("is_rest_day") else "")
    for i, d in enumerate(sdays)
]
tabs = st.tabs(tab_labels)

for tab, day_data in zip(tabs, sdays):
    with tab:
        dn          = day_data.get("day", 1)
        dietary     = day_data.get("dietary", {})
        is_rest     = day_data.get("is_rest_day", False)
        mg          = day_data.get("muscle_group", "Full Body")
        total_meals = len([m for m, v in dietary.items() if v])
        done_meals  = sum(1 for m in dietary if st.session_state.get(f"meal_d{dn}_{m}", False))
        pct_m       = int(done_meals / max(total_meals, 1) * 100)

        hdr_col, pct_col = st.columns([4, 1])
        with hdr_col:
            tag = "REST DAY" if is_rest else f"DAILY NUTRITION — {mg.upper()}"
            st.markdown(
                f"<div style='font-size:0.85rem;font-weight:700;letter-spacing:3px;"
                f"text-transform:uppercase;color:{accent};margin-bottom:8px'>{tag}</div>",
                unsafe_allow_html=True
            )
        with pct_col:
            st.markdown(
                f"<div style='text-align:right;font-size:1.05rem;font-weight:700;"
                f"color:{accent};padding-top:2px'>{done_meals}/{total_meals} &middot; {pct_m}%</div>",
                unsafe_allow_html=True
            )

        left_col, right_col = st.columns([3, 2])

        with left_col:
            if not dietary:
                st.markdown(
                    "<div style='color:rgba(255,255,255,0.90);font-size:1.00rem;"
                    "padding:20px;text-align:center'>No meals for this day.</div>",
                    unsafe_allow_html=True
                )
            else:
                for meal, desc in dietary.items():
                    if not desc: continue
                    icon  = MEAL_ICONS.get(meal, "🍽️")
                    ck    = f"meal_d{dn}_{meal}"
                    done  = st.session_state.get(ck, False)
                    strike = "text-decoration:line-through;opacity:0.40;" if done else ""

                    mc_top, mc_btn = st.columns([4, 1])
                    with mc_top:
                        st.markdown(
                            f"<div class='meal-card'>"
                            f"<div class='meal-label'>"
                            f"<span style='color:{accent}'>{icon} {meal.upper()}</span>"
                            + (f" <span style='color:{accent};font-size:0.75rem'>✓ Done</span>" if done else "") +
                            f"</div>"
                            f"<div class='meal-text' style='{strike}'>{str(desc)}</div>"
                            f"</div>",
                            unsafe_allow_html=True
                        )
                    with mc_btn:
                        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
                        st.markdown("<div class='swap-mini'>", unsafe_allow_html=True)
                        if st.button("🤖 Swap", key=f"swap_{dn}_{meal}", use_container_width=True):
                            with st.spinner("Getting AI alternative..."):
                                try:
                                    from model_api import query_model
                                    d_label = {"veg":"Vegetarian","nonveg":"Non-Vegetarian","both":"Flexible"}.get(dietary_type,"")
                                    prompt = (
                                        f"You are a diet coach. Suggest 1 alternative {meal} meal for a "
                                        f"{d_label} person (goal: {data.get('goal','Fitness')}). "
                                        f"Current meal: {str(desc)[:80]}. "
                                        "Reply in ONE plain English sentence only. "
                                        "Format: Meal name — key ingredients. "
                                        "Example: Masala Oats — rolled oats, tomato, onion, spices. "
                                        "NEVER use JSON, curly braces, brackets, or markdown. Plain text only."
                                    )
                                    result = query_model(prompt, max_tokens=80)
                                    import re as _re3
                                    result = result.strip()
                                    if result.startswith(("{","[")):
                                        result = "Please try again for a meal suggestion."
                                    result = _re3.sub(r"[{}\[\]]", "", result).strip()
                                    st.session_state[f"swap_result_{dn}_{meal}"] = result.strip()
                                    st.rerun()
                                except Exception:
                                    st.error("Could not get swap. Try again.")
                        st.markdown("</div>", unsafe_allow_html=True)

                    # Swap picker UI
                    swap_res   = st.session_state.get(f"swap_result_{dn}_{meal}")
                    chosen_key = f"meal_choice_{dn}_{meal}"
                    if swap_res:
                        chosen     = st.session_state.get(chosen_key, "original")
                        orig_style = f"background:rgba(229,9,20,0.25);border:2px solid #E50914" \
                                     if chosen=="original" \
                                     else "background:rgba(0,0,0,0.75);border:1.5px solid rgba(255,255,255,0.15)"
                        swap_style = f"background:rgba({rgb},0.20);border:2px solid {accent}" \
                                     if chosen=="swap" \
                                     else "background:rgba(0,0,0,0.75);border:1.5px solid rgba(255,255,255,0.15)"
                        orig_lbl_c = "rgba(229,9,20,0.90)" if chosen=="original" else "rgba(255,255,255,0.45)"
                        swap_lbl_c = f"rgba({rgb},0.90)"   if chosen=="swap"     else "rgba(255,255,255,0.45)"
                        st.markdown(
                            "<div style='background:rgba(0,0,0,0.70);border:1px solid rgba(255,255,255,0.18);"
                            "border-radius:12px;padding:12px 14px;margin-bottom:8px;backdrop-filter:blur(10px)'>"
                            f"<div style='font-size:0.85rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;"
                            f"color:{accent};margin-bottom:8px'>🤖 Choose Your {meal.title()}</div>"
                            "<div style='display:flex;gap:8px;flex-wrap:wrap'>"
                            f"<div style='flex:1;min-width:140px;{orig_style};border-radius:10px;padding:10px 12px'>"
                            f"<div style='font-size:0.85rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;"
                            f"color:{orig_lbl_c};margin-bottom:4px'>⭐ Original</div>"
                            f"<div style='font-size:0.80rem;color:#fff;line-height:1.5'>{str(desc)}</div></div>"
                            f"<div style='flex:1;min-width:140px;{swap_style};border-radius:10px;padding:10px 12px'>"
                            f"<div style='font-size:0.85rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;"
                            f"color:{swap_lbl_c};margin-bottom:4px'>🤖 AI Alternative</div>"
                            f"<div style='font-size:0.80rem;color:#fff;line-height:1.5'>{swap_res}</div></div>"
                            "</div></div>",
                            unsafe_allow_html=True
                        )
                        pick1, pick2, pick3 = st.columns([2, 2, 1])
                        with pick1:
                            if st.button(
                                "✓ Original" if chosen=="original" else "Keep Original",
                                key=f"pick_orig_{dn}_{meal}", use_container_width=True
                            ):
                                st.session_state[chosen_key] = "original"
                                st.rerun()
                        with pick2:
                            if st.button(
                                "✓ AI Swap" if chosen=="swap" else "Use AI Swap",
                                key=f"pick_swap_{dn}_{meal}", use_container_width=True
                            ):
                                st.session_state[chosen_key] = "swap"
                                _sdays_ref = st.session_state.get("structured_days", [])
                                for _sd_item in _sdays_ref:
                                    if _sd_item.get("day") == dn:
                                        _sd_item.setdefault("dietary", {})[meal] = swap_res
                                        break
                                st.session_state.structured_days = _sdays_ref
                                st.rerun()
                        with pick3:
                            if st.button("✕", key=f"dismiss_swap_{dn}_{meal}", use_container_width=True):
                                st.session_state.pop(f"swap_result_{dn}_{meal}", None)
                                st.session_state.pop(chosen_key, None)
                                st.rerun()

                    # Two-way checkbox
                    _new_done = st.checkbox("Mark as done", value=done, key=ck+"_cb")
                    if _new_done != done:
                        st.session_state[ck] = _new_done
                        if plan_id:
                            try:
                                from utils.db import save_progress
                                dc_ = {m2: st.session_state.get(f"meal_d{dn}_{m2}", False)
                                       for m2 in ["breakfast","lunch","dinner","snacks"]}
                                save_progress(uname, plan_id, dn, {}, dc_)
                            except Exception: pass
                        st.rerun()

        with right_col:
            # Nutrition summary
            _cal_base  = {"breakfast":380,"lunch":560,"dinner":480,"snacks":170}
            _prot_base = {"breakfast":20, "lunch":38, "dinner":32, "snacks":8}
            _cal_mult  = 1.1 if dietary_type=="nonveg" else 1.0
            total_cal  = int(sum(_cal_base.get(m,0)*_cal_mult for m in dietary if dietary.get(m)))
            total_prot = int(sum(_prot_base.get(m,0)*_cal_mult for m in dietary if dietary.get(m)))

            st.markdown(
                "<div style='background:rgba(0,0,0,0.75);border:1.5px solid rgba(255,255,255,0.15);"
                "border-radius:14px;padding:16px 18px;margin-bottom:12px;backdrop-filter:blur(10px)'>"
                f"<div class='feature-card-title'>Nutrition Summary</div>"
                "<div style='display:grid;grid-template-columns:1fr 1fr;gap:8px'>"
                "<div style='background:rgba(229,9,20,0.12);border-radius:10px;padding:12px;text-align:center'>"
                f"<div style='font-family:Bebas Neue,sans-serif;font-size:2rem;color:#E50914'>{total_cal}"
                "<span style='font-size:0.85rem;opacity:0.60;vertical-align:super'>est.</span></div>"
                "<div style='font-size:0.85rem;color:rgba(255,255,255,0.80);letter-spacing:2px;text-transform:uppercase;font-weight:600'>Calories</div></div>"
                "<div style='background:rgba(96,165,250,0.12);border-radius:10px;padding:12px;text-align:center'>"
                f"<div style='font-family:Bebas Neue,sans-serif;font-size:2rem;color:#60a5fa'>{total_prot}g"
                "<span style='font-size:0.85rem;opacity:0.60;vertical-align:super'>est.</span></div>"
                "<div style='font-size:0.85rem;color:rgba(255,255,255,0.80);letter-spacing:2px;text-transform:uppercase;font-weight:600'>Protein</div></div>"
                "</div>"
                "<div class='prog-bar-bg' style='margin-top:12px'>"
                f"<div class='prog-bar-fill' style='width:{pct_m}%'></div></div>"
                f"<div style='font-size:0.85rem;color:rgba(255,255,255,0.90);margin-top:4px;text-align:right'>"
                f"{done_meals}/{total_meals} meals done</div>"
                "</div>",
                unsafe_allow_html=True
            )

            # Nutrition tips
            st.markdown(
                f"<div style='background:rgba(0,0,0,0.70);border:1px solid rgba({rgb},0.22);"
                f"border-radius:12px;padding:16px 18px'>"
                f"<div style='font-size:0.85rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;"
                f"color:rgba({rgb},0.75);margin-bottom:10px'>💡 Nutrition Tips</div>",
                unsafe_allow_html=True
            )
            for tip in cfg["tips"][:5]:
                st.markdown(f"<div class='tip-card'>{tip}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)