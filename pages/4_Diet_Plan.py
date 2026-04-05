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

# ── NAV ───────────────────────────────────────────────────────────────────────
from auth_token import logout
st.markdown("<div class='nav-wrap'>", unsafe_allow_html=True)
_n = st.columns([1.6,1,1,1,1,1,1,1,1,1,1,1.2])
with _n[0]: st.markdown("<div class='nav-logo'>⚡ FITPLAN PRO</div>", unsafe_allow_html=True)
with _n[1]:
    if st.button("🏠 Home", key="dp_db", use_container_width=True):
        try: st.switch_page("pages/2_Dashboard.py")
        except Exception: pass
with _n[2]:
    if st.button("⚡ Workout", key="dp_wp", use_container_width=True):
        try: st.switch_page("pages/3_Workout_Plan.py")
        except Exception: pass
with _n[3]:
    if st.button("● 🥗 Diet", key="dp_dp", use_container_width=True):
        try: st.switch_page("pages/4_Diet_Plan.py")
        except Exception: pass
with _n[4]:
    if st.button("🍽️ Meals", key="dp_mp", use_container_width=True):
        try: st.switch_page("pages/11_meal_planner.py")
        except Exception: pass
with _n[5]:
    if st.button("😴 Sleep", key="dp_sl", use_container_width=True):
        try: st.switch_page("pages/12_sleep_tracker.py")
        except Exception: pass
with _n[6]:
    if st.button("🏃 Cardio", key="dp_ca", use_container_width=True):
        try: st.switch_page("pages/13_cardio_tracker.py")
        except Exception: pass
with _n[7]:
    if st.button("🔥 Streak", key="dp_st", use_container_width=True):
        try: st.switch_page("pages/14_streaks.py")
        except Exception: pass
with _n[8]:
    if st.button("📈 Charts", key="dp_ch", use_container_width=True):
        try: st.switch_page("pages/15_progress_charts.py")
        except Exception: pass
with _n[9]:
    if st.button("🤖 Coach", key="dp_ai", use_container_width=True):
        try: st.switch_page("pages/5_ai_coach.py")
        except Exception: pass
with _n[10]:
    if st.button("🏆 Records", key="dp_rc", use_container_width=True):
        try: st.switch_page("pages/6_records.py")
        except Exception: pass
with _n[11]:
    if st.button("🚪 Sign Out", key="dp_so", use_container_width=True):
        logout(uname)
        for _k in ["logged_in","username","auth_token","user_data","workout_plan","structured_days",
                   "dietary_type","full_plan_data","plan_id","plan_start","plan_duration",
                   "force_regen","tracking","_plan_checked","_db_loaded_dash"]:
            st.session_state.pop(_k, None)
        st.switch_page("app.py")
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