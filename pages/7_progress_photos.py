# -*- coding: utf-8 -*-
import streamlit as st
import os, sys, base64
from datetime import date
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth_token import logout

st.set_page_config(page_title="Progress Photos | FitPlan Pro", page_icon="📸",
                   layout="wide", initial_sidebar_state="collapsed")

if not st.session_state.get("logged_in"): st.switch_page("app.py")
if "user_data" not in st.session_state:   st.switch_page("pages/1_Profile.py")

uname = st.session_state.get("username", "Athlete")
data  = st.session_state.user_data

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow+Condensed:wght@700;800;900&family=DM+Sans:opsz,wght@9..40,400;9..40,600;9..40,700&display=swap');

[data-testid="stAppViewContainer"]::before{
  content:'';position:fixed;inset:0;z-index:0;
  background:url('https://images.unsplash.com/photo-1476480862126-209bfaa8edc8?fm=jpg&w=1600&q=80&fit=crop') center center/cover no-repeat;
  filter:blur(8px) brightness(0.20) saturate(0.45);
  transform:scale(1.06);
}
[data-testid="stAppViewContainer"]{
  background:linear-gradient(160deg,rgba(2,4,8,0.92) 0%,rgba(3,5,10,0.85) 50%,rgba(2,4,8,0.96) 100%)!important;
  position:relative;
}
[data-testid="stAppViewContainer"]>section>div.block-container{
  position:relative;z-index:2;max-width:1100px!important;margin:0 auto!important;padding:0 24px 80px!important;
}

#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stDecoration"],
[data-testid="stSidebarNav"],[data-testid="collapsedControl"],
section[data-testid="stSidebar"],button[kind="header"]{display:none!important;}

html,body,.stApp{background:#020408!important;color:#fff!important;font-family:'DM Sans',sans-serif!important;}

/* ── KILL WHITE BOXES — file uploader ── */
[data-testid="stFileUploader"]>div,
[data-testid="stFileUploadDropzone"],
[data-testid="stFileUploader"] section,
[data-testid="stFileUploader"] section>div,
[data-testid="stFileUploader"] section>div>div{
  background:rgba(4,8,18,0.88)!important;
  border:2px dashed rgba(99,102,241,0.50)!important;
  border-radius:16px!important;
  backdrop-filter:blur(20px)!important;
  color:#fff!important;
}
[data-testid="stFileUploader"]>div:hover,
[data-testid="stFileUploadDropzone"]:hover{
  border-color:rgba(99,102,241,0.90)!important;
  background:rgba(99,102,241,0.08)!important;
}
[data-testid="stFileUploader"] span,
[data-testid="stFileUploader"] p,
[data-testid="stFileUploader"] small,
[data-testid="stFileUploader"] div,
[data-testid="stFileUploader"] button{
  color:rgba(255,255,255,0.75)!important;
}
/* Override any internal white backgrounds */
[data-testid="stFileUploader"] *{
  background-color:transparent!important;
}
[data-testid="stFileUploadDropzone"] *{
  background-color:transparent!important;
}

/* ── SELECTBOX DARK ── */
[data-baseweb="select"]>div{
  background:rgba(4,8,18,0.88)!important;
  border:1.5px solid rgba(99,102,241,0.40)!important;
  border-radius:12px!important;backdrop-filter:blur(20px)!important;color:#fff!important;
}
[data-baseweb="select"] span,[data-baseweb="select"] div{color:#fff!important;}
[data-baseweb="popover"] [role="option"]{background:rgba(4,8,18,0.96)!important;color:#fff!important;}
[data-baseweb="popover"] [role="option"]:hover{background:rgba(99,102,241,0.25)!important;}

/* ── BUTTONS ── */
.stButton>button{
  background:linear-gradient(135deg,rgba(99,102,241,0.85),rgba(67,56,202,0.90))!important;
  border:2px solid rgba(99,102,241,0.65)!important;color:#fff!important;border-radius:10px!important;
  font-family:'DM Sans',sans-serif!important;font-size:1.0rem!important;font-weight:700!important;
  box-shadow:0 0 16px rgba(99,102,241,0.35)!important;transition:all 0.20s!important;
}
.stButton>button:hover{
  transform:translateY(-2px)!important;
  box-shadow:0 0 28px rgba(99,102,241,0.65)!important;
}
[data-testid="stFormSubmitButton"] button{
  background:linear-gradient(135deg,#6366f1,#4338ca)!important;border:none!important;
  color:#fff!important;border-radius:10px!important;font-weight:700!important;
  box-shadow:0 4px 20px rgba(99,102,241,0.45)!important;
}

/* ── NAV BUTTONS ── */
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"]>button{
  background:rgba(4,8,18,0.85)!important;border:2px solid rgba(99,102,241,0.50)!important;
  color:rgba(255,255,255,0.92)!important;border-radius:9px!important;
  font-size:0.85rem!important;font-weight:700!important;height:32px!important;
  min-height:32px!important;white-space:nowrap!important;
}
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"]>button:hover{
  background:rgba(99,102,241,0.28)!important;color:#fff!important;
}
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"]:last-child>button{
  background:linear-gradient(135deg,#c0000c,#8b0000)!important;
  border-color:rgba(229,9,20,0.80)!important;
}

/* ── WIDGET LABELS ── */
[data-testid="stWidgetLabel"],[data-testid="stWidgetLabel"] p{
  color:#fff!important;font-weight:700!important;text-shadow:0 2px 8px rgba(0,0,0,0.99)!important;
}

/* ── GLOBAL TEXT ── */
html,body,.stApp,.stMarkdown,p,div,span,label{text-shadow:0 2px 6px rgba(0,0,0,0.98)!important;}
.stMarkdown p,.stMarkdown li{color:#fff!important;}
.nav-logo{
  font-family:'Bebas Neue',sans-serif;font-size:1.4rem;letter-spacing:5px;
  color:#818cf8;text-shadow:0 0 18px rgba(99,102,241,0.55);line-height:1;
}
</style>
""", unsafe_allow_html=True)

# ── NAV ──────────────────────────────────────────────────────────────────────
st.markdown("<div style='background:rgba(2,4,10,0.97);backdrop-filter:blur(20px);"
            "border-bottom:1.5px solid rgba(99,102,241,0.25);padding:5px 0;margin-bottom:16px'>",
            unsafe_allow_html=True)
_n = st.columns([1.8,1,1,1,1,1,1,1.3])
with _n[0]: st.markdown("<div class='nav-logo'>FitPlan Pro</div>", unsafe_allow_html=True)
with _n[1]:
    if st.button("Home",     key="pp_db", use_container_width=True): st.switch_page("pages/2_Dashboard.py")
with _n[2]:
    if st.button("Workout",  key="pp_wp", use_container_width=True): st.switch_page("pages/3_Workout_Plan.py")
with _n[3]:
    if st.button("Diet",     key="pp_dp", use_container_width=True): st.switch_page("pages/4_Diet_Plan.py")
with _n[4]:
    if st.button("AI Coach", key="pp_ai", use_container_width=True):
        try: st.switch_page("pages/5_ai_coach.py")
        except Exception as e: st.warning(str(e))
with _n[5]:
    if st.button("Records",  key="pp_rc", use_container_width=True):
        try: st.switch_page("pages/6_records.py")
        except Exception as e: st.warning(str(e))
with _n[6]:
    if st.button("📸 Photos", key="pp_ph", use_container_width=True): st.switch_page("pages/7_progress_photos.py")
with _n[7]:
    if st.button("Sign Out", key="pp_so", use_container_width=True):
        logout(uname)
        for _k in ["logged_in","username","auth_token","user_data","workout_plan",
                   "structured_days","dietary_type","full_plan_data","plan_id","plan_start",
                   "plan_duration","plan_for","force_regen","tracking","_plan_checked",
                   "_db_loaded_dash","_auto_redirect","_diet_chosen","_needs_rerun",
                   "_db_streak","edit_profile_mode","_login_db_err","_notes_loaded"]:
            st.session_state.pop(_k, None)
        st.switch_page("app.py")
st.markdown("</div>", unsafe_allow_html=True)

# ── HERO — Catchy ─────────────────────────────────────────────────────────────
st.markdown(
    "<div style='background:linear-gradient(135deg,rgba(99,102,241,0.18),rgba(67,56,202,0.10) 50%,rgba(4,8,18,0.75));"
    "border:1.5px solid rgba(99,102,241,0.35);border-radius:20px;padding:32px 40px;margin-bottom:28px;"
    "position:relative;overflow:hidden'>"
    "<div style='position:absolute;top:0;left:0;right:0;height:2px;"
    "background:linear-gradient(90deg,transparent,#818cf8,#a5b4fc,transparent)'></div>"
    "<div style='position:absolute;bottom:-30px;right:-20px;font-size:8rem;opacity:0.06;line-height:1'>📸</div>"
    "<div style='font-size:0.75rem;font-weight:700;letter-spacing:4px;text-transform:uppercase;"
    "color:rgba(165,180,252,0.80);margin-bottom:8px'>📸 Visual Progress Tracker</div>"
    "<div style='font-family:Barlow Condensed,sans-serif;font-size:clamp(2rem,5vw,3.2rem);"
    "font-weight:900;text-transform:uppercase;color:#fff;line-height:1;margin-bottom:10px'>"
    "Progress <span style='color:#818cf8'>Photos</span></div>"
    "<div style='font-size:0.95rem;color:rgba(255,255,255,0.65);max-width:480px;line-height:1.6'>"
    "Document your transformation. Your body keeps the score — let the photos prove it.</div>"
    "<div style='display:flex;gap:16px;margin-top:16px;flex-wrap:wrap'>"
    "<div style='background:rgba(99,102,241,0.15);border:1px solid rgba(99,102,241,0.30);"
    "border-radius:20px;padding:5px 14px;font-size:0.80rem;font-weight:600;color:#a5b4fc'>"
    "📷 Before &amp; After</div>"
    "<div style='background:rgba(99,102,241,0.15);border:1px solid rgba(99,102,241,0.30);"
    "border-radius:20px;padding:5px 14px;font-size:0.80rem;font-weight:600;color:#a5b4fc'>"
    "🗂️ Timeline Gallery</div>"
    "<div style='background:rgba(99,102,241,0.15);border:1px solid rgba(99,102,241,0.30);"
    "border-radius:20px;padding:5px 14px;font-size:0.80rem;font-weight:600;color:#a5b4fc'>"
    "🔒 Private &amp; Secure</div>"
    "</div></div>",
    unsafe_allow_html=True
)

# ── Load photos ───────────────────────────────────────────────────────────────
if "progress_photos" not in st.session_state:
    try:
        from utils.db import get_progress_photos as _gpp
        _db_photos = _gpp(uname)
        st.session_state.progress_photos = _db_photos if _db_photos else []
    except Exception:
        st.session_state.progress_photos = []
photos = st.session_state.progress_photos

# ── Upload Section ────────────────────────────────────────────────────────────
st.markdown(
    "<div style='font-size:0.75rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;"
    "color:rgba(165,180,252,0.85);margin-bottom:12px;display:flex;align-items:center;gap:8px'>"
    "<span style='width:16px;height:1.5px;background:#818cf8;display:block'></span>"
    "📤 Upload Progress Photo</div>",
    unsafe_allow_html=True
)

upload_container = st.container()
with upload_container:
    uc1, uc2 = st.columns([3, 1])
    with uc1:
        uploaded = st.file_uploader(
            "Drop your photo here",
            type=["jpg","jpeg","png","webp"],
            key="photo_upload",
            label_visibility="collapsed"
        )
    with uc2:
        photo_label = st.selectbox(
            "Label",
            ["Current","Before","After","Week 1","Week 4","Week 8","Week 12","Month 1","Month 2","Month 3","Custom"],
            key="photo_label",
            label_visibility="collapsed"
        )

if uploaded:
    img_bytes = uploaded.read()
    img_b64   = base64.b64encode(img_bytes).decode()
    ext       = uploaded.name.split(".")[-1].lower()
    mime      = "image/jpeg" if ext in ["jpg","jpeg"] else ("image/" + ext)
    src       = "data:" + mime + ";base64," + img_b64

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    pc1, pc2 = st.columns([1, 2])
    with pc1:
        st.markdown(
            "<div style='border-radius:14px;overflow:hidden;border:2px solid rgba(99,102,241,0.45);"
            "box-shadow:0 8px 32px rgba(99,102,241,0.25)'>"
            "<img src='" + src + "' style='width:100%;display:block'></div>",
            unsafe_allow_html=True
        )
    with pc2:
        st.markdown(
            "<div style='background:rgba(4,8,18,0.88);border:1.5px solid rgba(99,102,241,0.30);"
            "border-radius:14px;padding:20px 24px;height:100%'>"
            "<div style='font-size:0.65rem;letter-spacing:3px;text-transform:uppercase;"
            "color:rgba(165,180,252,0.70);margin-bottom:12px'>Photo Details</div>"
            "<div style='display:grid;grid-template-columns:auto 1fr;gap:6px 14px;font-size:0.90rem'>"
            "<span style='color:rgba(255,255,255,0.45)'>File</span>"
            "<span style='color:#fff;font-weight:600'>" + uploaded.name + "</span>"
            "<span style='color:rgba(255,255,255,0.45)'>Size</span>"
            "<span style='color:#fff;font-weight:600'>" + str(len(img_bytes)//1024) + " KB</span>"
            "<span style='color:rgba(255,255,255,0.45)'>Label</span>"
            "<span style='color:#818cf8;font-weight:700'>" + photo_label + "</span>"
            "<span style='color:rgba(255,255,255,0.45)'>Date</span>"
            "<span style='color:#fff;font-weight:600'>" + date.today().isoformat() + "</span>"
            "</div></div>",
            unsafe_allow_html=True
        )
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        if st.button("💾 Save Photo", key="save_photo", use_container_width=True):
            new_photo = {
                "date":  date.today().isoformat(),
                "label": photo_label,
                "b64":   img_b64,
                "mime":  mime
            }
            photos.append(new_photo)
            st.session_state.progress_photos = photos
            try:
                from utils.db import save_progress_photo
                save_progress_photo(uname, new_photo)
            except Exception: pass
            st.toast("📸 Photo saved!", icon="✅")
            st.rerun()

st.markdown(
    "<div style='height:1px;background:linear-gradient(90deg,transparent,rgba(99,102,241,0.35),transparent);"
    "margin:20px 0'></div>",
    unsafe_allow_html=True
)

# ── Gallery ───────────────────────────────────────────────────────────────────
if not photos:
    st.markdown(
        "<div style='text-align:center;padding:70px 20px;"
        "background:rgba(4,8,18,0.80);border:1.5px dashed rgba(99,102,241,0.30);"
        "border-radius:20px;margin-top:8px'>"
        "<div style='font-size:4rem;margin-bottom:14px;filter:drop-shadow(0 0 20px rgba(99,102,241,0.50))'>📸</div>"
        "<div style='font-family:Bebas Neue,sans-serif;font-size:2rem;letter-spacing:2px;"
        "color:#818cf8;margin-bottom:8px'>No Photos Yet</div>"
        "<div style='font-size:0.90rem;color:rgba(255,255,255,0.50);max-width:360px;margin:0 auto;line-height:1.6'>"
        "Upload your first progress photo above to start documenting your transformation journey.</div>"
        "<div style='margin-top:20px;font-size:2rem;opacity:0.30'>→ 💪 → 🏆</div>"
        "</div>",
        unsafe_allow_html=True
    )
else:
    # ── Stats bar ─────────────────────────────────────────────────────────────
    d0   = date.fromisoformat(photos[0]["date"])
    d1   = date.fromisoformat(photos[-1]["date"])
    days = (d1 - d0).days

    st.markdown(
        "<div style='display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:24px'>"
        "<div style='background:rgba(4,8,18,0.85);border:1.5px solid rgba(99,102,241,0.28);"
        "border-radius:14px;padding:16px;text-align:center'>"
        "<div style='font-family:Bebas Neue,sans-serif;font-size:2.4rem;color:#818cf8;line-height:1'>" + str(len(photos)) + "</div>"
        "<div style='font-size:0.65rem;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.45);margin-top:4px'>Photos Taken</div></div>"
        "<div style='background:rgba(4,8,18,0.85);border:1.5px solid rgba(99,102,241,0.28);"
        "border-radius:14px;padding:16px;text-align:center'>"
        "<div style='font-family:Bebas Neue,sans-serif;font-size:2.4rem;color:#a5b4fc;line-height:1'>" + str(days) + "</div>"
        "<div style='font-size:0.65rem;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.45);margin-top:4px'>Days Tracked</div></div>"
        "<div style='background:rgba(4,8,18,0.85);border:1.5px solid rgba(99,102,241,0.28);"
        "border-radius:14px;padding:16px;text-align:center'>"
        "<div style='font-family:Bebas Neue,sans-serif;font-size:2.4rem;color:#c4b5fd;line-height:1'>" + photos[-1]["label"] + "</div>"
        "<div style='font-size:0.65rem;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.45);margin-top:4px'>Latest Label</div></div>"
        "</div>",
        unsafe_allow_html=True
    )

    # ── Before / After comparison ─────────────────────────────────────────────
    if len(photos) >= 2:
        st.markdown(
            "<div style='font-size:0.75rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;"
            "color:rgba(165,180,252,0.85);margin-bottom:12px;display:flex;align-items:center;gap:8px'>"
            "<span style='width:16px;height:1.5px;background:#818cf8;display:block'></span>"
            "🔄 Before / After Comparison</div>",
            unsafe_allow_html=True
        )
        ba1, ba2 = st.columns(2)
        pf    = photos[0]
        src_f = "data:" + pf["mime"] + ";base64," + pf["b64"]
        with ba1:
            st.markdown(
                "<div style='background:rgba(4,8,18,0.82);border:1.5px solid rgba(229,9,20,0.35);"
                "border-radius:16px;overflow:hidden;position:relative'>"
                "<div style='position:absolute;top:10px;left:10px;z-index:2;"
                "background:rgba(229,9,20,0.85);border-radius:6px;padding:3px 10px;"
                "font-size:0.70rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#fff'>"
                "BEFORE</div>"
                "<img src='" + src_f + "' style='width:100%;display:block'>"
                "<div style='padding:10px 14px;border-top:1px solid rgba(229,9,20,0.20)'>"
                "<div style='font-size:0.80rem;font-weight:600;color:rgba(255,255,255,0.80)'>"
                + pf["label"] + " &nbsp;·&nbsp; " + pf["date"] + "</div></div></div>",
                unsafe_allow_html=True
            )
        pl    = photos[-1]
        src_l = "data:" + pl["mime"] + ";base64," + pl["b64"]
        with ba2:
            st.markdown(
                "<div style='background:rgba(4,8,18,0.82);border:1.5px solid rgba(99,102,241,0.45);"
                "border-radius:16px;overflow:hidden;position:relative'>"
                "<div style='position:absolute;top:10px;left:10px;z-index:2;"
                "background:rgba(99,102,241,0.85);border-radius:6px;padding:3px 10px;"
                "font-size:0.70rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#fff'>"
                "LATEST</div>"
                "<img src='" + src_l + "' style='width:100%;display:block'>"
                "<div style='padding:10px 14px;border-top:1px solid rgba(99,102,241,0.20)'>"
                "<div style='font-size:0.80rem;font-weight:600;color:rgba(255,255,255,0.80)'>"
                + pl["label"] + " &nbsp;·&nbsp; " + pl["date"] + "</div></div></div>",
                unsafe_allow_html=True
            )

        st.markdown(
            "<div style='text-align:center;margin:14px 0;font-size:0.85rem;"
            "color:rgba(165,180,252,0.70);letter-spacing:1px'>"
            "🗓️ " + str(days) + " days between first and latest photo · " + str(len(photos)) + " total photos</div>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<div style='height:1px;background:linear-gradient(90deg,transparent,rgba(99,102,241,0.30),transparent);"
            "margin:16px 0'></div>",
            unsafe_allow_html=True
        )

    # ── Full gallery grid ─────────────────────────────────────────────────────
    st.markdown(
        "<div style='font-size:0.75rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;"
        "color:rgba(165,180,252,0.85);margin-bottom:12px;display:flex;align-items:center;gap:8px'>"
        "<span style='width:16px;height:1.5px;background:#818cf8;display:block'></span>"
        "🗂️ All Photos — Timeline</div>",
        unsafe_allow_html=True
    )
    gcols = st.columns(3)
    for i, p in enumerate(reversed(photos)):
        src_p = "data:" + p["mime"] + ";base64," + p["b64"]
        is_latest = (i == 0)
        border_col = "rgba(99,102,241,0.60)" if is_latest else "rgba(99,102,241,0.20)"
        badge_html = (
            "<div style='position:absolute;top:8px;right:8px;"
            "background:rgba(99,102,241,0.90);border-radius:6px;padding:2px 8px;"
            "font-size:0.60rem;font-weight:700;letter-spacing:1px;color:#fff'>LATEST</div>"
            if is_latest else ""
        )
        with gcols[i % 3]:
            st.markdown(
                f"<div style='background:rgba(4,8,18,0.82);border:1.5px solid {border_col};"
                f"border-radius:14px;overflow:hidden;margin-bottom:14px;position:relative'>"
                f"{badge_html}"
                f"<img src='{src_p}' style='width:100%;display:block'>"
                f"<div style='padding:10px 12px;background:rgba(4,8,18,0.90)'>"
                f"<div style='display:flex;justify-content:space-between;align-items:center'>"
                f"<span style='font-size:0.80rem;font-weight:700;color:#a5b4fc'>{p['label']}</span>"
                f"<span style='font-size:0.70rem;color:rgba(255,255,255,0.40)'>{p['date']}</span>"
                f"</div></div></div>",
                unsafe_allow_html=True
            )

    # ── Clear button ──────────────────────────────────────────────────────────
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    cl1, cl2, cl3 = st.columns([2,1,2])
    with cl2:
        if not st.session_state.get("_clear_confirm"):
            if st.button("🗑️ Clear All", key="clear_photos", use_container_width=True):
                st.session_state._clear_confirm = True
                st.rerun()
        else:
            st.markdown(
                "<div style='background:rgba(229,9,20,0.10);border:1px solid rgba(229,9,20,0.35);"
                "border-radius:10px;padding:10px;text-align:center;font-size:0.80rem;"
                "color:rgba(255,255,255,0.80);margin-bottom:8px'>"
                "⚠️ Delete all photos?</div>",
                unsafe_allow_html=True
            )
            yc, nc = st.columns(2)
            with yc:
                if st.button("✅ Yes", key="clear_yes", use_container_width=True):
                    st.session_state.progress_photos = []
                    st.session_state._clear_confirm  = False
                    st.rerun()
            with nc:
                if st.button("❌ No", key="clear_no", use_container_width=True):
                    st.session_state._clear_confirm = False
                    st.rerun()