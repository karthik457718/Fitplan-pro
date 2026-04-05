"""
nav_component.py — FitPlan Pro Premium Navigation
Slim top bar (logo + current page + menu button) with a full-width
animated drawer that slides down on click. Works on laptop, tablet, desktop.
All navigation via hidden Streamlit buttons — fully compatible with st.switch_page.
"""
import streamlit as st
from auth_token import logout

NAV_PAGES = [
    ("dashboard", "🏠", "Home",    "pages/2_Dashboard.py"),
    ("workout",   "⚡", "Workout", "pages/3_Workout_Plan.py"),
    ("diet",      "🥗", "Diet",    "pages/4_Diet_Plan.py"),
    ("meals",     "🍽️","Meals",   "pages/11_meal_planner.py"),
    ("sleep",     "😴", "Sleep",   "pages/12_sleep_tracker.py"),
    ("cardio",    "🏃", "Cardio",  "pages/13_cardio_tracker.py"),
    ("streak",    "🔥", "Streak",  "pages/14_streaks.py"),
    ("charts",    "📈", "Charts",  "pages/15_progress_charts.py"),
    ("coach",     "🤖", "Coach",   "pages/5_ai_coach.py"),
    ("records",   "🏆", "Records", "pages/6_records.py"),
    ("photos",    "📸", "Photos",  "pages/7_progress_photos.py"),
    ("history",   "📅", "History", "pages/9_history.py"),
]

_CLEAR_KEYS = [
    "logged_in","username","auth_token","user_data","workout_plan",
    "structured_days","dietary_type","full_plan_data","plan_id","plan_start",
    "plan_duration","plan_for","force_regen","tracking","_plan_checked",
    "_db_loaded_dash","_auto_redirect","_diet_chosen","_needs_rerun",
    "_db_streak","edit_profile_mode","_login_db_err","_notes_loaded",
    "_streak_synced","last_badge_count","_regen_confirm","_nav_open",
]

def render_nav(current_page: str, username: str = None):
    if username is None:
        username = st.session_state.get("username", "Athlete")

    # ── Session state for drawer toggle ──────────────────────────────────
    if "_nav_open" not in st.session_state:
        st.session_state._nav_open = False

    # Find current page label & icon
    cur_icon, cur_label = "⚡", "FitPlan Pro"
    for key, icon, label, _ in NAV_PAGES:
        if key == current_page:
            cur_icon, cur_label = icon, label
            break

    # ── Build nav HTML ────────────────────────────────────────────────────
    drawer_state = "open" if st.session_state._nav_open else "closed"
    overlay_display = "block" if st.session_state._nav_open else "none"

    # Build drawer grid items
    grid_items = ""
    for key, icon, label, path in NAV_PAGES:
        is_active = (key == current_page)
        active_style = (
            "background:rgba(229,9,20,0.25);border:1.5px solid rgba(229,9,20,0.80);"
            "box-shadow:0 0 16px rgba(229,9,20,0.30);"
        ) if is_active else (
            "background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);"
        )
        active_label_color = "#fff" if is_active else "rgba(255,255,255,0.70)"
        active_icon_bg = "rgba(229,9,20,0.20)" if is_active else "rgba(255,255,255,0.06)"
        active_dot = "<div style=\'width:5px;height:5px;border-radius:50%;background:#E50914;margin:0 auto;\'></div>" if is_active else ""
        grid_items += f"""
<button onclick="document.getElementById(\'fpbtn_{key}\').click();closeDr();"
  style="cursor:pointer;{active_style}border-radius:14px;padding:14px 10px 12px;
  display:flex;flex-direction:column;align-items:center;gap:6px;
  transition:all 0.18s ease;color:{active_label_color};font-family:\'DM Sans\',sans-serif;">
  <div style="width:44px;height:44px;border-radius:12px;background:{active_icon_bg};
    display:flex;align-items:center;justify-content:center;font-size:22px;
    transition:all 0.18s ease;">{icon}</div>
  <div style="font-size:0.72rem;font-weight:700;letter-spacing:0.5px;text-align:center;
    line-height:1.2;">{label}</div>
  {active_dot}
</button>"""

    nav_html = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@400;500;600;700&display=swap');
#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stDecoration"],
[data-testid="stSidebarNav"],section[data-testid="stSidebar"]{{display:none!important;}}

.fp-topbar{{
  display:flex;align-items:center;justify-content:space-between;
  background:rgba(6,2,1,0.98);
  border-bottom:1px solid rgba(229,9,20,0.20);
  box-shadow:0 2px 20px rgba(0,0,0,0.60);
  padding:0 20px;height:52px;
  position:relative;z-index:1000;
}}
.fp-logo-text{{
  font-family:\'Bebas Neue\',sans-serif;font-size:1.35rem;
  letter-spacing:4px;color:#E50914;
  text-shadow:0 0 16px rgba(229,9,20,0.50);
  line-height:1;user-select:none;
}}
.fp-current-page{{
  display:flex;align-items:center;gap:8px;
  background:rgba(229,9,20,0.10);
  border:1px solid rgba(229,9,20,0.25);
  border-radius:20px;padding:4px 14px 4px 10px;
}}
.fp-current-icon{{font-size:16px;line-height:1;}}
.fp-current-label{{
  font-family:\'DM Sans\',sans-serif;font-size:0.78rem;
  font-weight:700;color:rgba(255,255,255,0.88);
  letter-spacing:0.3px;
}}
.fp-menu-btn{{
  cursor:pointer;
  background:rgba(255,255,255,0.05);
  border:1px solid rgba(229,9,20,0.28);
  border-radius:10px;padding:8px 10px;
  display:flex;flex-direction:column;gap:4px;
  transition:all 0.18s ease;
}}
.fp-menu-btn:hover{{
  background:rgba(229,9,20,0.18);
  border-color:rgba(229,9,20,0.65);
}}
.fp-bar{{
  width:20px;height:2px;background:#E50914;border-radius:2px;
  transition:all 0.25s ease;transform-origin:center;
}}
.fp-overlay{{
  display:{overlay_display};
  position:fixed;inset:0;background:rgba(0,0,0,0.55);
  z-index:998;backdrop-filter:blur(3px);
  animation:fadeOverlay 0.22s ease;
}}
@keyframes fadeOverlay{{from{{opacity:0}}to{{opacity:1}}}}
.fp-drawer{{
  background:linear-gradient(160deg,rgba(10,4,2,0.98) 0%,rgba(15,5,2,0.98) 100%);
  border-bottom:1px solid rgba(229,9,20,0.22);
  box-shadow:0 12px 48px rgba(0,0,0,0.80);
  overflow:hidden;
  max-height:{("520px" if st.session_state._nav_open else "0")};
  opacity:{("1" if st.session_state._nav_open else "0")};
  transition:max-height 0.35s cubic-bezier(0.4,0,0.2,1),opacity 0.25s ease;
  position:relative;z-index:999;
}}
.fp-drawer-inner{{
  padding:20px 20px 24px;
}}
.fp-drawer-header{{
  display:flex;align-items:center;justify-content:space-between;
  margin-bottom:16px;padding-bottom:14px;
  border-bottom:1px solid rgba(255,255,255,0.06);
}}
.fp-drawer-title{{
  font-family:\'Bebas Neue\',sans-serif;font-size:1.0rem;
  letter-spacing:4px;color:rgba(229,9,20,0.65);
}}
.fp-user-chip{{
  display:flex;align-items:center;gap:8px;
  background:rgba(229,9,20,0.08);border:1px solid rgba(229,9,20,0.20);
  border-radius:20px;padding:4px 12px 4px 6px;
}}
.fp-avatar{{
  width:24px;height:24px;border-radius:50%;
  background:linear-gradient(135deg,#E50914,#8b0000);
  display:flex;align-items:center;justify-content:center;
  font-size:11px;font-weight:700;color:#fff;font-family:\'DM Sans\',sans-serif;
}}
.fp-username{{
  font-size:0.75rem;font-weight:600;color:rgba(255,255,255,0.75);
  font-family:\'DM Sans\',sans-serif;
}}
.fp-grid{{
  display:grid;
  grid-template-columns:repeat(6,1fr);
  gap:8px;
  margin-bottom:16px;
}}
@media(max-width:900px){{.fp-grid{{grid-template-columns:repeat(4,1fr);}}}}
@media(max-width:600px){{.fp-grid{{grid-template-columns:repeat(3,1fr);}}}}
.fp-grid button:hover{{
  background:rgba(229,9,20,0.18)!important;
  border-color:rgba(229,9,20,0.55)!important;
  color:#fff!important;
  transform:translateY(-2px);
}}
.fp-signout-bar{{
  display:flex;align-items:center;justify-content:flex-end;
  padding-top:12px;border-top:1px solid rgba(255,255,255,0.05);
}}
.fp-signout-btn{{
  cursor:pointer;
  background:rgba(60,5,5,0.60);
  border:1px solid rgba(229,9,20,0.22);
  border-radius:10px;padding:7px 18px;
  color:rgba(255,255,255,0.45);
  font-family:\'DM Sans\',sans-serif;font-size:0.78rem;font-weight:700;
  display:flex;align-items:center;gap:7px;
  transition:all 0.18s ease;
}}
.fp-signout-btn:hover{{
  background:rgba(140,0,8,0.60);
  border-color:rgba(229,9,20,0.55);
  color:#fff;
}}
.fp-hidden{{position:absolute;opacity:0;pointer-events:none;height:0;overflow:hidden;width:0;}}
</style>

<div class="fp-overlay" id="fp-overlay" onclick="closeDr()"></div>

<div class="fp-topbar">
  <div class="fp-logo-text">⚡ FITPLAN PRO</div>

  <div class="fp-current-page">
    <span class="fp-current-icon">{cur_icon}</span>
    <span class="fp-current-label">{cur_label}</span>
  </div>

  <button class="fp-menu-btn" onclick="toggleDr()" id="fp-hamburger" title="Navigation menu">
    <div class="fp-bar" id="bar1"></div>
    <div class="fp-bar" id="bar2"></div>
    <div class="fp-bar" id="bar3"></div>
  </button>
</div>

<div class="fp-drawer" id="fp-drawer">
  <div class="fp-drawer-inner">
    <div class="fp-drawer-header">
      <div class="fp-drawer-title">NAVIGATE</div>
      <div class="fp-user-chip">
        <div class="fp-avatar">{username[0].upper() if username else "A"}</div>
        <span class="fp-username">{username}</span>
      </div>
    </div>

    <div class="fp-grid">
      {grid_items}
    </div>

    <div class="fp-signout-bar">
      <button class="fp-signout-btn" onclick="document.getElementById(\'fpbtn_signout\').click()">
        <span style="font-size:14px;">🚪</span>
        <span>Sign Out</span>
      </button>
    </div>
  </div>
</div>

<script>
var isOpen = {'true' if st.session_state._nav_open else 'false'};
function toggleDr(){{
  isOpen = !isOpen;
  var dr = document.getElementById('fp-drawer');
  var ov = document.getElementById('fp-overlay');
  var b1 = document.getElementById('bar1');
  var b2 = document.getElementById('bar2');
  var b3 = document.getElementById('bar3');
  if(isOpen){{
    dr.style.maxHeight = '520px';
    dr.style.opacity = '1';
    ov.style.display = 'block';
    b1.style.transform = 'translateY(6px) rotate(45deg)';
    b2.style.opacity = '0';
    b3.style.transform = 'translateY(-6px) rotate(-45deg)';
  }} else {{
    dr.style.maxHeight = '0';
    dr.style.opacity = '0';
    ov.style.display = 'none';
    b1.style.transform = 'none';
    b2.style.opacity = '1';
    b3.style.transform = 'none';
  }}
}}
function closeDr(){{
  if(!isOpen) return;
  isOpen = false;
  var dr = document.getElementById('fp-drawer');
  var ov = document.getElementById('fp-overlay');
  dr.style.maxHeight = '0';
  dr.style.opacity = '0';
  ov.style.display = 'none';
  var b1 = document.getElementById('bar1');
  var b2 = document.getElementById('bar2');
  var b3 = document.getElementById('bar3');
  b1.style.transform = 'none';
  b2.style.opacity = '1';
  b3.style.transform = 'none';
}}
</script>
"""

    st.markdown(nav_html, unsafe_allow_html=True)

    # ── Hidden Streamlit buttons (actual navigation) ──────────────────────
    st.markdown("<div class='fp-hidden'>", unsafe_allow_html=True)
    btn_cols = st.columns(len(NAV_PAGES) + 1)
    for i, (key, icon, label, path) in enumerate(NAV_PAGES):
        with btn_cols[i]:
            if st.button(f"{icon}{label}", key=f"fpbtn_{key}"):
                st.session_state._nav_open = False
                try:
                    st.switch_page(path)
                except Exception:
                    pass
    with btn_cols[-1]:
        if st.button("signout", key="fpbtn_signout"):
            logout(username)
            for k in _CLEAR_KEYS:
                st.session_state.pop(k, None)
            st.switch_page("app.py")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)