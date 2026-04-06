"""
nav_component.py — FitPlan Pro Navigation (Upgraded).

DESKTOP  (>900px) : Persistent slim top bar with all 12 page icons always visible.
                    No click needed — icons shown inline, click to navigate.
TABLET   (600-900px): Top bar logo + current page pill + hamburger. 4-col drawer grid.
MOBILE   (<600px) : Same as tablet but drawer grid is 3 columns.

Hidden Streamlit nav buttons are pushed off-screen via CSS + JS.
"""
import streamlit as st
from auth_token import logout

NAV_PAGES = [
    ("dashboard", "🏠", "Home",    "pages/2_Dashboard.py"),
    ("workout",   "⚡", "Workout", "pages/3_Workout_Plan.py"),
    ("diet",      "🥗", "Diet",    "pages/4_Diet_Plan.py"),
    ("meals",     "🍽️", "Meals",  "pages/11_meal_planner.py"),
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

NAV_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@400;500;600;700&display=swap');

#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stDecoration"],
[data-testid="stSidebarNav"],section[data-testid="stSidebar"]{display:none!important;}

/* ── Shared top bar ── */
.fp-topbar{
  display:flex;align-items:center;gap:10px;
  background:rgba(6,2,1,0.98);
  border-bottom:1px solid rgba(229,9,20,0.22);
  box-shadow:0 2px 24px rgba(0,0,0,0.70);
  padding:0 16px;height:56px;
  position:relative;z-index:1000;
}
.fp-logo{
  font-family:'Bebas Neue',sans-serif;font-size:1.28rem;letter-spacing:4px;
  color:#E50914;text-shadow:0 0 18px rgba(229,9,20,0.55);
  line-height:1;user-select:none;flex-shrink:0;
}

/* ══════════════════════════════════════════
   DESKTOP: inline icon nav strip  (>900px)
══════════════════════════════════════════ */
.fp-desktop-nav{
  display:none;
  align-items:center;gap:1px;flex:1;overflow:hidden;
}
.fp-dn-item{
  cursor:pointer;
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  gap:2px;padding:5px 8px;border-radius:10px;
  border:1px solid transparent;
  transition:all 0.17s ease;
  color:rgba(255,255,255,0.48);
  flex-shrink:0;min-width:48px;
  font-family:'DM Sans',sans-serif;
  position:relative;
}
.fp-dn-item:hover{
  background:rgba(229,9,20,0.14);border-color:rgba(229,9,20,0.42);
  color:#fff;transform:translateY(-1px);
}
.fp-dn-item.fp-dn-active{
  background:rgba(229,9,20,0.20);border-color:rgba(229,9,20,0.80);
  color:#fff;box-shadow:0 0 12px rgba(229,9,20,0.22);
}
.fp-dn-icon{font-size:16px;line-height:1;}
.fp-dn-lbl{font-size:0.57rem;font-weight:700;letter-spacing:0.3px;white-space:nowrap;}
.fp-dn-dot{
  position:absolute;bottom:3px;left:50%;transform:translateX(-50%);
  width:4px;height:4px;border-radius:50%;background:#E50914;
}

/* Desktop right: user chip + sign out */
.fp-desktop-right{
  display:none;align-items:center;gap:8px;flex-shrink:0;margin-left:auto;
}
.fp-user-chip{
  display:flex;align-items:center;gap:6px;
  background:rgba(229,9,20,0.08);border:1px solid rgba(229,9,20,0.22);
  border-radius:20px;padding:4px 12px 4px 5px;
}
.fp-avatar{
  width:24px;height:24px;border-radius:50%;
  background:linear-gradient(135deg,#E50914,#8b0000);
  display:flex;align-items:center;justify-content:center;
  font-size:11px;font-weight:700;color:#fff;
  font-family:'DM Sans',sans-serif;flex-shrink:0;
}
.fp-uname{font-size:0.72rem;font-weight:600;color:rgba(255,255,255,0.75);font-family:'DM Sans',sans-serif;}
.fp-so-desk{
  cursor:pointer;background:rgba(50,4,4,0.60);border:1px solid rgba(229,9,20,0.22);
  border-radius:9px;padding:6px 12px;color:rgba(255,255,255,0.45);
  font-family:'DM Sans',sans-serif;font-size:0.72rem;font-weight:700;
  display:flex;align-items:center;gap:5px;transition:all 0.18s;white-space:nowrap;
}
.fp-so-desk:hover{background:rgba(130,0,6,0.70);border-color:rgba(229,9,20,0.65);color:#fff;}

/* ══════════════════════════════════════════
   MOBILE/TABLET: pill + hamburger  (<=900px)
══════════════════════════════════════════ */
.fp-mobile-right{
  display:none;align-items:center;gap:10px;margin-left:auto;flex-shrink:0;
}
.fp-pill{
  display:flex;align-items:center;gap:6px;
  background:rgba(229,9,20,0.10);border:1px solid rgba(229,9,20,0.28);
  border-radius:20px;padding:5px 13px 5px 9px;
}
.fp-pill-icon{font-size:15px;line-height:1;}
.fp-pill-lbl{
  font-family:'DM Sans',sans-serif;font-size:0.77rem;font-weight:700;
  color:rgba(255,255,255,0.90);letter-spacing:0.3px;
}
.fp-hamburger{
  cursor:pointer;background:rgba(255,255,255,0.05);border:1px solid rgba(229,9,20,0.30);
  border-radius:10px;padding:9px 11px;display:flex;flex-direction:column;gap:4px;
  transition:all 0.18s;flex-shrink:0;
}
.fp-hamburger:hover{background:rgba(229,9,20,0.20);border-color:rgba(229,9,20,0.65);}
.fp-bar{
  width:20px;height:2px;background:#E50914;border-radius:2px;
  transition:all 0.26s ease;transform-origin:center;display:block;
}

/* Overlay */
.fp-overlay{
  display:none;position:fixed;inset:0;background:rgba(0,0,0,0.55);
  z-index:998;backdrop-filter:blur(2px);
}

/* Drawer */
.fp-drawer{
  background:linear-gradient(160deg,rgba(10,4,2,0.99) 0%,rgba(16,6,2,0.99) 100%);
  border-bottom:1px solid rgba(229,9,20,0.18);
  box-shadow:0 12px 48px rgba(0,0,0,0.80);
  max-height:0;overflow:hidden;
  transition:max-height 0.38s cubic-bezier(0.4,0,0.2,1),opacity 0.25s ease;
  opacity:0;position:relative;z-index:999;
}
.fp-drawer-inner{padding:20px 20px 22px;}
.fp-d-header{
  display:flex;align-items:center;justify-content:space-between;
  margin-bottom:16px;padding-bottom:14px;
  border-bottom:1px solid rgba(255,255,255,0.06);
}
.fp-d-title{
  font-family:'Bebas Neue',sans-serif;font-size:1rem;
  letter-spacing:4px;color:rgba(229,9,20,0.65);
}
.fp-d-user{
  display:flex;align-items:center;gap:7px;
  background:rgba(229,9,20,0.08);border:1px solid rgba(229,9,20,0.20);
  border-radius:20px;padding:4px 12px 4px 5px;
}
.fp-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:16px;}
@media(max-width:600px){.fp-grid{grid-template-columns:repeat(3,1fr);}}
.fp-item{
  cursor:pointer;background:rgba(255,255,255,0.04);
  border:1px solid rgba(255,255,255,0.09);border-radius:14px;
  padding:14px 10px 12px;
  display:flex;flex-direction:column;align-items:center;gap:6px;
  transition:all 0.18s ease;color:rgba(255,255,255,0.72);
  font-family:'DM Sans',sans-serif;
}
.fp-item:hover{
  background:rgba(229,9,20,0.20);border-color:rgba(229,9,20,0.60);
  color:#fff;transform:translateY(-2px);box-shadow:0 6px 20px rgba(229,9,20,0.20);
}
.fp-item.fp-active{
  background:rgba(229,9,20,0.25);border:1.5px solid rgba(229,9,20,0.80);
  color:#fff;box-shadow:0 0 18px rgba(229,9,20,0.30);
}
.fp-ico-wrap{
  width:44px;height:44px;border-radius:12px;background:rgba(255,255,255,0.06);
  display:flex;align-items:center;justify-content:center;font-size:22px;
}
.fp-item.fp-active .fp-ico-wrap{background:rgba(229,9,20,0.22);}
.fp-item-lbl{font-size:0.72rem;font-weight:700;letter-spacing:0.4px;}
.fp-active-dot{width:5px;height:5px;border-radius:50%;background:#E50914;}
.fp-so-bar{
  display:flex;align-items:center;justify-content:flex-end;
  padding-top:12px;border-top:1px solid rgba(255,255,255,0.05);
}
.fp-so-btn{
  cursor:pointer;background:rgba(50,4,4,0.65);border:1px solid rgba(229,9,20,0.22);
  border-radius:10px;padding:7px 20px;color:rgba(255,255,255,0.45);
  font-family:'DM Sans',sans-serif;font-size:0.80rem;font-weight:700;
  display:flex;align-items:center;gap:8px;transition:all 0.18s;
}
.fp-so-btn:hover{background:rgba(130,0,6,0.70);border-color:rgba(229,9,20,0.60);color:#fff;}

/* ── Responsive switches ── */
@media(min-width:901px){
  .fp-desktop-nav{display:flex!important;}
  .fp-desktop-right{display:flex!important;}
  .fp-mobile-right{display:none!important;}
  .fp-drawer{display:none!important;}
  .fp-overlay{display:none!important;}
}
@media(max-width:900px){
  .fp-desktop-nav{display:none!important;}
  .fp-desktop-right{display:none!important;}
  .fp-mobile-right{display:flex!important;}
}
</style>
"""


def render_nav(current_page: str, username: str = None):
    if username is None:
        username = st.session_state.get("username", "Athlete")

    # Current page info for mobile pill
    cur_icon, cur_label = "⚡", "FitPlan Pro"
    for key, icon, label, _ in NAV_PAGES:
        if key == current_page:
            cur_icon, cur_label = icon, label
            break

    st.markdown(NAV_CSS, unsafe_allow_html=True)

    av = username[0].upper() if username else "A"

    # ── Build desktop inline icon strip ───────────────────────────────────
    desktop_html = ""
    for key, icon, label, _ in NAV_PAGES:
        is_active = (key == current_page)
        cls       = "fp-dn-item fp-dn-active" if is_active else "fp-dn-item"
        dot       = "<div class='fp-dn-dot'></div>" if is_active else ""
        onclick   = "document.getElementById('fpbtn_" + key + "').click()"
        desktop_html += (
            "<div class='" + cls + "' onclick=\"" + onclick + "\" title='" + label + "'>"
            "<div class='fp-dn-icon'>" + icon + "</div>"
            "<div class='fp-dn-lbl'>" + label + "</div>"
            + dot +
            "</div>"
        )

    # ── Build mobile drawer grid ───────────────────────────────────────────
    drawer_html = ""
    for key, icon, label, _ in NAV_PAGES:
        is_active = (key == current_page)
        cls       = "fp-item fp-active" if is_active else "fp-item"
        dot       = "<div class='fp-active-dot'></div>" if is_active else ""
        onclick   = "document.getElementById('fpbtn_" + key + "').click()"
        drawer_html += (
            "<div class='" + cls + "' onclick=\"" + onclick + "\">"
            "<div class='fp-ico-wrap'>" + icon + "</div>"
            "<div class='fp-item-lbl'>" + label + "</div>"
            + dot +
            "</div>"
        )

    # ── Full nav HTML ──────────────────────────────────────────────────────
    nav_html = (
        '<div class="fp-overlay" id="fp-ov" onclick="fpClose()"></div>'

        '<div class="fp-topbar">'

        # Logo — always visible
        '<div class="fp-logo">&#9889; FITPLAN PRO</div>'

        # DESKTOP: inline icon strip
        '<div class="fp-desktop-nav">' + desktop_html + '</div>'

        # DESKTOP: user chip + sign out (right side)
        '<div class="fp-desktop-right">'
        '<div class="fp-user-chip">'
        '<div class="fp-avatar">' + av + '</div>'
        '<span class="fp-uname">' + username + '</span>'
        '</div>'
        '<button class="fp-so-desk" onclick="document.getElementById(\'fpbtn_signout\').click()">'
        '&#128682; Sign Out'
        '</button>'
        '</div>'

        # MOBILE/TABLET: current page pill + hamburger
        '<div class="fp-mobile-right">'
        '<div class="fp-pill">'
        '<span class="fp-pill-icon">' + cur_icon + '</span>'
        '<span class="fp-pill-lbl">' + cur_label + '</span>'
        '</div>'
        '<button class="fp-hamburger" onclick="fpToggle()" id="fp-hbtn">'
        '<span class="fp-bar" id="fpb1"></span>'
        '<span class="fp-bar" id="fpb2"></span>'
        '<span class="fp-bar" id="fpb3"></span>'
        '</button>'
        '</div>'

        '</div>'  # end .fp-topbar

        # MOBILE/TABLET: slide-down drawer (hidden on desktop)
        '<div class="fp-drawer" id="fp-drawer">'
        '<div class="fp-drawer-inner">'
        '<div class="fp-d-header">'
        '<div class="fp-d-title">NAVIGATE</div>'
        '<div class="fp-d-user">'
        '<div class="fp-avatar">' + av + '</div>'
        '<span class="fp-uname">' + username + '</span>'
        '</div>'
        '</div>'
        '<div class="fp-grid">' + drawer_html + '</div>'
        '<div class="fp-so-bar">'
        '<button class="fp-so-btn" onclick="document.getElementById(\'fpbtn_signout\').click()">'
        '<span style="font-size:15px;">&#128682;</span><span>Sign Out</span>'
        '</button>'
        '</div>'
        '</div>'
        '</div>'

        # JS: hamburger toggle (only fires on mobile, desktop drawer is display:none)
        '<script>'
        '(function(){'
        'var _o=false;'
        'window.fpToggle=function(){'
        '_o=!_o;'
        'var d=document.getElementById("fp-drawer");'
        'var v=document.getElementById("fp-ov");'
        'var b1=document.getElementById("fpb1");'
        'var b2=document.getElementById("fpb2");'
        'var b3=document.getElementById("fpb3");'
        'if(_o){'
        'if(d){d.style.maxHeight="520px";d.style.opacity="1";}'
        'if(v){v.style.display="block";}'
        'if(b1){b1.style.transform="translateY(6px) rotate(45deg)";}'
        'if(b2){b2.style.opacity="0";}'
        'if(b3){b3.style.transform="translateY(-6px) rotate(-45deg)";}'
        '}else{fpClose();}'
        '};'
        'window.fpClose=function(){'
        '_o=false;'
        'var d=document.getElementById("fp-drawer");'
        'var v=document.getElementById("fp-ov");'
        'if(d){d.style.maxHeight="0";d.style.opacity="0";}'
        'if(v){v.style.display="none";}'
        'var b1=document.getElementById("fpb1");'
        'var b2=document.getElementById("fpb2");'
        'var b3=document.getElementById("fpb3");'
        'if(b1){b1.style.transform="none";}'
        'if(b2){b2.style.opacity="1";}'
        'if(b3){b3.style.transform="none";}'
        '};'
        '})();'
        '</script>'
    )

    st.markdown(nav_html, unsafe_allow_html=True)

    # ── Hidden Streamlit buttons (functional page-switch triggers) ─────────
    hide_id = "fp_nav_btns_wrapper"
    st.markdown(
        f"<div id='{hide_id}'></div>"
        "<style>"
        f"#{hide_id} + div,"
        f"#{hide_id} ~ div[data-testid='stHorizontalBlock']"
        "{position:absolute!important;left:-9999px!important;top:0!important;"
        "width:1px!important;height:1px!important;overflow:hidden!important;"
        "opacity:0!important;pointer-events:none!important;}"
        "</style>",
        unsafe_allow_html=True
    )

    cols = st.columns(len(NAV_PAGES) + 1)
    for i, (key, icon, label, path) in enumerate(NAV_PAGES):
        with cols[i]:
            if st.button(label, key=f"fpbtn_{key}"):
                try:
                    st.switch_page(path)
                except Exception:
                    pass
    with cols[-1]:
        if st.button("signout", key="fpbtn_signout"):
            logout(username)
            for k in _CLEAR_KEYS:
                st.session_state.pop(k, None)
            st.switch_page("app.py")

    # JS fallback — hides Streamlit button row after render
    st.markdown(
        "<script>"
        "(function(){"
        "function hide(){"
        "var el=document.getElementById('fp_nav_btns_wrapper');"
        "if(!el)return;"
        "var sib=el.nextElementSibling;"
        "while(sib){"
        "sib.style.cssText='position:absolute!important;left:-9999px!important;"
        "top:0!important;width:1px!important;height:1px!important;"
        "overflow:hidden!important;opacity:0!important;pointer-events:none!important;';"
        "sib=sib.nextElementSibling;}"
        "}"
        "setTimeout(hide,80);setTimeout(hide,400);setTimeout(hide,1200);"
        "})();"
        "</script>"
        "<div style='height:4px'></div>",
        unsafe_allow_html=True
    )