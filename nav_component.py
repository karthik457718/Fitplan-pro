"""
nav_component.py — Shared nav bar for FitPlan Pro.
Pure Streamlit columns — compact icon+label buttons, never wraps.
"""
import streamlit as st
from auth_token import logout

NAV_PAGES = [
    ("dashboard", "🏠 Home",    "pages/2_Dashboard.py"),
    ("workout",   "⚡ Workout", "pages/3_Workout_Plan.py"),
    ("diet",      "🥗 Diet",    "pages/4_Diet_Plan.py"),
    ("meals",     "🍽️ Meals",  "pages/11_meal_planner.py"),
    ("sleep",     "😴 Sleep",   "pages/12_sleep_tracker.py"),
    ("cardio",    "🏃 Cardio",  "pages/13_cardio_tracker.py"),
    ("streak",    "🔥 Streak",  "pages/14_streaks.py"),
    ("charts",    "📈 Charts",  "pages/15_progress_charts.py"),
    ("coach",     "🤖 Coach",   "pages/5_ai_coach.py"),
    ("records",   "🏆 Records", "pages/6_records.py"),
]

NAV_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@500;600;700&display=swap');

/* ── Streamlit chrome ────────────────────────────────────── */
#MainMenu,footer,header,[data-testid="stToolbar"],
[data-testid="stDecoration"],[data-testid="stSidebarNav"],
section[data-testid="stSidebar"]{display:none!important;}

/* ── Nav shell ───────────────────────────────────────────── */
.fp-nav-outer{
  background:rgba(5,2,1,0.97);
  border-bottom:1px solid rgba(229,9,20,0.20);
  box-shadow:0 3px 20px rgba(0,0,0,0.70);
  padding:5px 12px 5px 10px;
  display:flex;align-items:center;gap:0;
  margin-bottom:6px;
}
.fp-logo{
  font-family:'Bebas Neue',sans-serif;
  font-size:1.15rem;letter-spacing:3px;
  color:#E50914;line-height:1.1;
  text-shadow:0 0 14px rgba(229,9,20,0.50);
  white-space:nowrap;padding-right:8px;flex-shrink:0;
}

/* ── All nav buttons (targets the Streamlit column row) ─── */
div[data-testid="stHorizontalBlock"]:has(button[data-fp-nav]) button,
.fp-nav-row div[data-testid="stButton"]>button{
  background:rgba(255,255,255,0.04)!important;
  border:1px solid rgba(229,9,20,0.22)!important;
  color:rgba(255,255,255,0.72)!important;
  border-radius:8px!important;
  font-family:'DM Sans',sans-serif!important;
  font-size:0.70rem!important;font-weight:700!important;
  padding:3px 7px!important;
  height:28px!important;min-height:28px!important;
  white-space:nowrap!important;
  box-shadow:none!important;
  transition:all 0.14s ease!important;
  letter-spacing:0.2px!important;
}
div[data-testid="stHorizontalBlock"]:has(button[data-fp-nav]) button:hover,
.fp-nav-row div[data-testid="stButton"]>button:hover{
  background:rgba(229,9,20,0.20)!important;
  border-color:rgba(229,9,20,0.65)!important;
  color:#fff!important;
  transform:translateY(-1px)!important;
  box-shadow:0 0 10px rgba(229,9,20,0.25)!important;
}
/* active page button */
.fp-nav-row .fp-active div[data-testid="stButton"]>button{
  background:rgba(229,9,20,0.30)!important;
  border:1.5px solid #E50914!important;
  color:#fff!important;
  box-shadow:0 0 12px rgba(229,9,20,0.45)!important;
}
/* sign out button */
.fp-nav-row .fp-signout div[data-testid="stButton"]>button{
  background:rgba(35,4,4,0.60)!important;
  border-color:rgba(229,9,20,0.18)!important;
  color:rgba(255,255,255,0.38)!important;
}
.fp-nav-row .fp-signout div[data-testid="stButton"]>button:hover{
  background:rgba(130,0,6,0.65)!important;
  border-color:rgba(229,9,20,0.60)!important;
  color:#fff!important;
  box-shadow:none!important;
}
</style>
"""

_CLEAR_KEYS = [
    "logged_in","username","auth_token","user_data","workout_plan",
    "structured_days","dietary_type","full_plan_data","plan_id","plan_start",
    "plan_duration","plan_for","force_regen","tracking","_plan_checked",
    "_db_loaded_dash","_auto_redirect","_diet_chosen","_needs_rerun",
    "_db_streak","edit_profile_mode","_login_db_err","_notes_loaded",
    "_streak_synced","last_badge_count","_regen_confirm",
]

def render_nav(current_page: str, username: str = None):
    """
    Render the shared nav bar.
    current_page: 'dashboard'|'workout'|'diet'|'meals'|'sleep'|
                  'cardio'|'streak'|'charts'|'coach'|'records'
    """
    if username is None:
        username = st.session_state.get("username", "Athlete")

    st.markdown(NAV_CSS, unsafe_allow_html=True)

    # Logo + nav row in a single flex line using HTML + st.columns side by side
    st.markdown("""
<div style='background:rgba(5,2,1,0.97);border-bottom:1px solid rgba(229,9,20,0.20);
  box-shadow:0 3px 20px rgba(0,0,0,0.70);padding:0;margin-bottom:0;'>
</div>""", unsafe_allow_html=True)

    # Single row: logo col + 10 nav cols + signout col
    cols = st.columns([1.4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1.1])

    with cols[0]:
        st.markdown(
            "<div style='font-family:Bebas Neue,sans-serif;font-size:1.15rem;"
            "letter-spacing:3px;color:#E50914;text-shadow:0 0 14px rgba(229,9,20,0.50);"
            "line-height:1.15;padding:6px 0 4px 4px'>⚡ FITPLAN<br>PRO</div>",
            unsafe_allow_html=True
        )

    for i, (page_key, label, path) in enumerate(NAV_PAGES):
        with cols[i + 1]:
            is_active = (page_key == current_page)
            # Active page: prepend bullet
            btn_lbl = ("● " + label) if is_active else label
            if is_active:
                st.markdown("<div class='fp-active'>", unsafe_allow_html=True)
            if st.button(btn_lbl, key=f"fpnav_{page_key}", use_container_width=True):
                try:
                    st.switch_page(path)
                except Exception:
                    pass
            if is_active:
                st.markdown("</div>", unsafe_allow_html=True)

    with cols[11]:
        st.markdown("<div class='fp-signout'>", unsafe_allow_html=True)
        if st.button("🚪 Out", key="fpnav_signout", use_container_width=True):
            logout(username)
            for k in _CLEAR_KEYS:
                st.session_state.pop(k, None)
            st.switch_page("app.py")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)