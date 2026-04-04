# -*- coding: utf-8 -*-
import streamlit as st
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth_token import logout
from bg_utils import apply_bg

st.set_page_config(page_title="AI Coach | FitPlan Pro", page_icon="🤖",
                   layout="wide", initial_sidebar_state="collapsed")

if not st.session_state.get("logged_in"): st.switch_page("app.py")
if "user_data" not in st.session_state:   st.switch_page("pages/1_Profile.py")

uname = st.session_state.get("username", "Athlete")
data  = st.session_state.user_data

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Syne:wght@600;700;800&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600&display=swap');

[data-testid="stAppViewContainer"]::before{
  content:'';position:fixed;inset:0;z-index:0;
  background:url('https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?fm=jpg&w=1920&q=80&fit=crop') center/cover no-repeat;
  filter:blur(12px) brightness(0.15) saturate(0.35);transform:scale(1.10);}
[data-testid="stAppViewContainer"]{
  background:radial-gradient(ellipse at 20% 50%,rgba(229,9,20,0.08) 0%,transparent 60%),
             radial-gradient(ellipse at 80% 20%,rgba(99,60,220,0.06) 0%,transparent 50%),
             linear-gradient(160deg,rgba(2,2,8,0.97) 0%,rgba(5,3,12,0.95) 100%)!important;
  position:relative;}
[data-testid="stAppViewContainer"]>section>div.block-container{
  position:relative;z-index:2;max-width:940px!important;
  margin:0 auto!important;padding:0 20px 120px!important;}

#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stDecoration"],
[data-testid="stSidebarNav"],[data-testid="collapsedControl"],
section[data-testid="stSidebar"],button[kind="header"]{display:none!important;}
html,body,.stApp{background:#020208!important;color:#fff!important;font-family:'DM Sans',sans-serif!important;}

div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"]>button{
  background:rgba(8,6,18,0.80)!important;border:1px solid rgba(229,9,20,0.28)!important;
  color:rgba(255,255,255,0.70)!important;border-radius:8px!important;
  font-size:0.80rem!important;font-weight:600!important;height:30px!important;
  min-height:30px!important;white-space:nowrap!important;transition:all 0.16s!important;}
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"]>button:hover{
  background:rgba(229,9,20,0.18)!important;border-color:rgba(229,9,20,0.60)!important;color:#fff!important;}
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stButton"]:last-child>button{
  background:rgba(229,9,20,0.22)!important;border-color:rgba(229,9,20,0.50)!important;}

.stButton>button{
  background:linear-gradient(135deg,#E50914 0%,#b0000a 100%)!important;
  border:none!important;color:#fff!important;border-radius:12px!important;
  font-family:'DM Sans',sans-serif!important;font-size:1rem!important;font-weight:700!important;
  box-shadow:0 4px 20px rgba(229,9,20,0.48),0 0 0 1px rgba(229,9,20,0.18)!important;
  transition:all 0.22s cubic-bezier(0.34,1.56,0.64,1)!important;}
.stButton>button:hover{
  transform:translateY(-3px) scale(1.03)!important;
  box-shadow:0 10px 32px rgba(229,9,20,0.70),0 0 50px rgba(229,9,20,0.22)!important;}

[data-testid="stForm"]{background:transparent!important;border:none!important;}
[data-testid="stFormSubmitButton"] button,.stFormSubmitButton>button{
  background:linear-gradient(135deg,#E50914,#8b0000)!important;border:none!important;
  color:#fff!important;border-radius:14px!important;font-weight:800!important;
  font-size:1rem!important;letter-spacing:1px!important;height:56px!important;
  box-shadow:0 6px 24px rgba(229,9,20,0.55),0 0 50px rgba(229,9,20,0.12)!important;}

input,textarea,.stTextInput>div>div>input,
[data-baseweb="input"] input,[data-testid="stTextInput"] input{
  background:#0a0814!important;background-color:#0a0814!important;
  border:1.5px solid rgba(229,9,20,0.28)!important;color:#fff!important;
  border-radius:14px!important;font-family:'DM Sans',sans-serif!important;font-size:1rem!important;
  box-shadow:inset 0 0 0 9999px #0a0814!important;
  -webkit-box-shadow:inset 0 0 0 9999px #0a0814!important;
  caret-color:#E50914!important;transition:border-color 0.25s!important;}
input:focus,[data-baseweb="input"] input:focus{
  border-color:rgba(229,9,20,0.72)!important;
  box-shadow:inset 0 0 0 9999px #0a0814,0 0 0 3px rgba(229,9,20,0.14)!important;
  -webkit-box-shadow:inset 0 0 0 9999px #0a0814!important;outline:none!important;}
[data-baseweb="input"]{background:#0a0814!important;background-color:#0a0814!important;
  border:1.5px solid rgba(229,9,20,0.28)!important;border-radius:14px!important;}
input:-webkit-autofill,input:-webkit-autofill:focus{
  -webkit-box-shadow:0 0 0 9999px #0a0814 inset!important;-webkit-text-fill-color:#fff!important;}

.quick-btn .stButton>button{
  background:rgba(255,255,255,0.03)!important;border:1px solid rgba(255,255,255,0.09)!important;
  color:rgba(255,255,255,0.62)!important;font-size:0.80rem!important;font-weight:500!important;
  text-transform:none!important;border-radius:22px!important;padding:6px 14px!important;
  height:auto!important;min-height:auto!important;box-shadow:none!important;
  letter-spacing:0!important;font-style:italic!important;animation:none!important;
  transition:all 0.18s ease!important;}
.quick-btn .stButton>button:hover{
  background:rgba(229,9,20,0.12)!important;border-color:rgba(229,9,20,0.42)!important;
  color:#fff!important;transform:translateY(-2px)!important;
  box-shadow:0 4px 14px rgba(229,9,20,0.18)!important;}

html,body,.stApp,.stMarkdown,p,div,span,label{text-shadow:0 1px 4px rgba(0,0,0,0.95)!important;}
[data-testid="stWidgetLabel"],[data-testid="stWidgetLabel"] p{color:#fff!important;font-weight:600!important;}
.stMarkdown p,.stMarkdown li{color:#fff!important;line-height:1.75!important;}

@keyframes fadeSlideUp{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}
@keyframes fadeSlideRight{from{opacity:0;transform:translateX(-14px)}to{opacity:1;transform:translateX(0)}}
@keyframes fadeSlideLeft{from{opacity:0;transform:translateX(14px)}to{opacity:1;transform:translateX(0)}}
@keyframes pulseRing{0%{transform:scale(1);opacity:0.70}100%{transform:scale(1.80);opacity:0}}
@keyframes onlineBlink{0%,100%{opacity:1;box-shadow:0 0 8px #22c55e}50%{opacity:0.35;box-shadow:0 0 3px #22c55e}}
@keyframes typing{0%,100%{transform:translateY(0);opacity:0.90}50%{transform:translateY(-5px);opacity:0.40}}
@keyframes borderPulse{0%,100%{box-shadow:0 0 0 1px rgba(229,9,20,0.18),0 8px 32px rgba(0,0,0,0.60)}
  50%{box-shadow:0 0 0 1px rgba(229,9,20,0.42),0 8px 40px rgba(229,9,20,0.10)}}
@keyframes scanLine{0%{top:-2px;opacity:0}10%{opacity:1}90%{opacity:1}100%{top:102%;opacity:0}}
</style>
""", unsafe_allow_html=True)

apply_bg(
    "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?fm=jpg&w=1920&q=80&fit=crop",
    overlay="rgba(2,2,10,0.85)"
)

# ── NAV ───────────────────────────────────────────────────────────────────────
st.markdown("<div style='padding:6px 0;margin-bottom:12px'>", unsafe_allow_html=True)
_n = st.columns([1.6,1,1,1,1,1,1,1.2])
with _n[0]:
    st.markdown(
        "<div style='font-family:Bebas Neue,sans-serif;font-size:1.4rem;letter-spacing:5px;"
        "color:#E50914;text-shadow:0 0 24px rgba(229,9,20,0.60);line-height:1;padding-top:4px'>"
        "&#9889; FITPLAN PRO</div>", unsafe_allow_html=True)
nav_pages = [
    ("🏠 Home",    "pages/2_Dashboard.py",    "ac_db"),
    ("⚡ Workout", "pages/3_Workout_Plan.py",  "ac_wp"),
    ("🥗 Diet",    "pages/4_Diet_Plan.py",     "ac_dp"),
    ("🤖 Coach",   "pages/5_ai_coach.py",      "ac_ai"),
    ("🏆 Records", "pages/6_records.py",       "ac_rc"),
    ("📸 Photos",  "pages/7_progress_photos.py","ac_ph"),
]
for i,(lbl,path,key) in enumerate(nav_pages):
    with _n[i+1]:
        if st.button(lbl, key=key, use_container_width=True):
            st.switch_page(path)
with _n[7]:
    if st.button("🚪 Sign Out", key="ac_so", use_container_width=True):
        logout(uname)
        for _k in ["logged_in","username","auth_token","user_data","workout_plan","structured_days",
                   "dietary_type","full_plan_data","plan_id","plan_start","plan_duration","plan_for",
                   "force_regen","tracking","_plan_checked","_db_loaded_dash","_auto_redirect",
                   "_diet_chosen","_needs_rerun","_db_streak","edit_profile_mode"]:
            st.session_state.pop(_k, None)
        st.switch_page("app.py")
st.markdown("</div>", unsafe_allow_html=True)

# ── CONTEXT ───────────────────────────────────────────────────────────────────
sdays    = st.session_state.get("structured_days", [])
diet_lbl = ("Vegetarian" if st.session_state.get("dietary_type")=="veg"
            else ("Non-Veg" if st.session_state.get("dietary_type")=="nonveg" else "Flexible"))
plan_ctx = (str(len(sdays)) + "-day fitness plan. Diet: " + diet_lbl + ". ") if sdays else ""

system_prompt = (
    "You are ATLAS, a professional AI fitness coach inside FitPlan Pro. "
    "Warm, motivating, direct. Speak like a real coach. "
    "User: " + uname + ", Age=" + str(data.get("age","?")) +
    ", Weight=" + str(data.get("weight","?")) + "kg"
    ", Height=" + str(data.get("height","?")) + "cm"
    ", Goal=" + data.get("goal","Fitness") +
    ", Level=" + data.get("level","Beginner") +
    ", Equipment=" + (", ".join(data.get("equipment",[])) or "Bodyweight") + ". " + plan_ctx +
    "RULES: Only answer fitness, gym, nutrition, body, health, lifestyle, motivation, sleep, recovery. "
    "Redirect off-topic warmly. NO JSON/code blocks. Max 130 words. "
    "Dash (-) for lists, max 4 items. Don't start with 'Assistant:' or 'ATLAS:'. "
    "Reference earlier conversation. End with short motivational line when fitting."
)

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown(
    "<div style='position:relative;overflow:hidden;border-radius:22px;margin-bottom:16px;"
    "background:linear-gradient(135deg,rgba(18,6,6,0.94) 0%,rgba(8,4,20,0.90) 60%,rgba(18,6,6,0.94) 100%);"
    "border:1px solid rgba(229,9,20,0.22);animation:borderPulse 4s ease-in-out infinite;"
    "padding:20px 26px'>"
    # Scan line
    "<div style='position:absolute;left:0;right:0;height:1px;"
    "background:linear-gradient(90deg,transparent,rgba(229,9,20,0.35),transparent);"
    "animation:scanLine 4s linear infinite;pointer-events:none;z-index:1'></div>"
    # Top line
    "<div style='position:absolute;top:0;left:0;right:0;height:2px;"
    "background:linear-gradient(90deg,transparent,#E50914 35%,rgba(229,9,20,0.35) 65%,transparent)'></div>"
    # Glow orb
    "<div style='position:absolute;top:-50px;right:-50px;width:200px;height:200px;border-radius:50%;"
    "background:radial-gradient(circle,rgba(229,9,20,0.16) 0%,transparent 70%);pointer-events:none'></div>"
    "<div style='display:flex;align-items:center;gap:18px;position:relative;z-index:2'>"
    # Avatar
    "<div style='position:relative;flex-shrink:0;width:60px;height:60px'>"
    "<div style='width:60px;height:60px;border-radius:50%;"
    "background:linear-gradient(135deg,#E50914 0%,#5c000a 100%);"
    "display:flex;align-items:center;justify-content:center;font-size:1.7rem;"
    "box-shadow:0 0 0 3px rgba(229,9,20,0.28),0 0 28px rgba(229,9,20,0.42)'>🤖</div>"
    "<div style='position:absolute;inset:-6px;border-radius:50%;"
    "border:2px solid rgba(229,9,20,0.45);animation:pulseRing 2s ease-out infinite'></div>"
    "<div style='position:absolute;inset:-12px;border-radius:50%;"
    "border:1px solid rgba(229,9,20,0.20);animation:pulseRing 2s ease-out infinite 0.6s'></div>"
    "</div>"
    # Title
    "<div style='flex:1'>"
    "<div style='font-family:Syne,sans-serif;font-size:1.55rem;font-weight:800;"
    "background:linear-gradient(90deg,#ffffff 55%,rgba(229,9,20,0.85));background-size:200% auto;"
    "-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;"
    "line-height:1.1;margin-bottom:6px'>ATLAS &mdash; Your AI Fitness Coach</div>"
    "<div style='display:flex;flex-wrap:wrap;gap:6px;align-items:center'>"
    + " ".join([
        f"<span style='font-size:0.76rem;color:rgba(255,255,255,0.40)'>{t}</span>"
        + (f"<span style='color:rgba(229,9,20,0.40);font-size:0.76rem'>&middot;</span>" if i<3 else "")
        for i,t in enumerate([
            f"Trained on your profile",
            f"{len(sdays)}-day plan",
            f"{diet_lbl} diet",
            data.get("goal","Fitness")
        ])
    ]) +
    "</div></div>"
    # Online
    "<div style='display:flex;align-items:center;gap:6px;background:rgba(34,197,94,0.09);"
    "border:1px solid rgba(34,197,94,0.25);border-radius:20px;padding:5px 12px;flex-shrink:0'>"
    "<div style='width:7px;height:7px;border-radius:50%;background:#22c55e;"
    "animation:onlineBlink 2s ease-in-out infinite'></div>"
    "<span style='font-size:0.70rem;font-weight:700;letter-spacing:2px;"
    "color:rgba(34,197,94,0.88);text-transform:uppercase'>ONLINE</span>"
    "</div></div></div>",
    unsafe_allow_html=True
)

# ── CHAT HISTORY ──────────────────────────────────────────────────────────────
if "chat_messages" not in st.session_state:
    try:
        from utils.db import get_chat_history
        _hist = get_chat_history(uname, limit=30)
        st.session_state.chat_messages = _hist if _hist else []
    except Exception:
        st.session_state.chat_messages = []

# ── QUICK QUESTIONS ───────────────────────────────────────────────────────────
st.markdown(
    "<div style='font-size:0.66rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;"
    "color:rgba(229,9,20,0.58);margin-bottom:7px;display:flex;align-items:center;gap:8px'>"
    "<span style='width:12px;height:1px;background:#E50914;display:block'></span>Quick Ask</div>",
    unsafe_allow_html=True)
quick_qs = [("💪","Best post-workout meal?"),("🔥","How to lose fat faster?"),
            ("😴","How much sleep do I need?"),("🥩","Daily protein target?"),
            ("⚡","How to boost energy?"),("🧘","Recovery tips for soreness?")]
qc = st.columns(3)
for i,(emoji,q) in enumerate(quick_qs):
    with qc[i%3]:
        st.markdown("<div class='quick-btn'>", unsafe_allow_html=True)
        if st.button(f"{emoji} {q}", key=f"qq_{i}", use_container_width=True):
            st.session_state.chat_messages.append({"role":"user","content":q})
            st.session_state._atlas_needs_reply = True
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ── CHAT MESSAGES ─────────────────────────────────────────────────────────────
if not st.session_state.chat_messages:
    st.markdown(
        f"<div style='text-align:center;padding:52px 20px;animation:fadeSlideUp 0.6s ease both'>"
        f"<div style='font-size:3.8rem;margin-bottom:14px;"
        f"filter:drop-shadow(0 0 24px rgba(229,9,20,0.65))'>🤖</div>"
        f"<div style='font-family:Syne,sans-serif;font-size:1.5rem;font-weight:800;"
        f"background:linear-gradient(135deg,#fff 40%,#E50914);"
        f"-webkit-background-clip:text;-webkit-text-fill-color:transparent;"
        f"background-clip:text;letter-spacing:0.5px;margin-bottom:10px'>"
        f"Hey {uname}, I'm ATLAS</div>"
        f"<div style='font-size:0.92rem;color:rgba(255,255,255,0.42);max-width:420px;"
        f"margin:0 auto;line-height:1.75'>"
        f"Your personal AI fitness coach. Ask me anything about workouts, "
        f"nutrition, recovery — I know your full {len(sdays)}-day plan.</div>"
        f"<div style='margin-top:22px;display:flex;justify-content:center;gap:10px;flex-wrap:wrap'>"
        f"<div style='background:rgba(229,9,20,0.09);border:1px solid rgba(229,9,20,0.22);"
        f"border-radius:20px;padding:5px 14px;font-size:0.76rem;color:rgba(255,255,255,0.50)'>💬 Ongoing conversations</div>"
        f"<div style='background:rgba(229,9,20,0.09);border:1px solid rgba(229,9,20,0.22);"
        f"border-radius:20px;padding:5px 14px;font-size:0.76rem;color:rgba(255,255,255,0.50)'>🧠 Knows your full plan</div>"
        f"<div style='background:rgba(229,9,20,0.09);border:1px solid rgba(229,9,20,0.22);"
        f"border-radius:20px;padding:5px 14px;font-size:0.76rem;color:rgba(255,255,255,0.50)'>⚡ Instant answers</div>"
        f"</div></div>",
        unsafe_allow_html=True)
else:
    for mi, msg in enumerate(st.session_state.chat_messages):
        delay = f"{min(mi*0.04,0.30):.2f}s"
        if msg["role"] == "user":
            st.markdown(
                f"<div style='display:flex;justify-content:flex-end;margin:8px 0;"
                f"animation:fadeSlideLeft 0.32s ease {delay} both'>"
                f"<div style='max-width:76%'>"
                f"<div style='text-align:right;font-size:0.60rem;font-weight:700;letter-spacing:2px;"
                f"text-transform:uppercase;color:rgba(229,9,20,0.60);margin-bottom:4px;padding-right:6px'>YOU</div>"
                f"<div style='background:linear-gradient(135deg,rgba(229,9,20,0.22),rgba(140,0,8,0.16));"
                f"border:1.5px solid rgba(229,9,20,0.35);border-radius:18px 18px 4px 18px;"
                f"padding:13px 17px;box-shadow:0 4px 20px rgba(229,9,20,0.16)'>"
                f"<div style='font-size:0.95rem;color:#fff;line-height:1.65'>{msg['content']}</div>"
                f"</div></div>"
                f"<div style='width:34px;height:34px;border-radius:50%;"
                f"background:rgba(229,9,20,0.14);border:1.5px solid rgba(229,9,20,0.32);"
                f"display:flex;align-items:center;justify-content:center;"
                f"margin-left:9px;flex-shrink:0;align-self:flex-end;font-size:1rem'>👤</div>"
                f"</div>",
                unsafe_allow_html=True)
        else:
            _lines = []
            for _ln in msg["content"].splitlines():
                _s = _ln.strip()
                if _s.startswith("- ") or _s.startswith("• "):
                    _lines.append(
                        f"<div style='display:flex;gap:9px;margin:5px 0;align-items:flex-start'>"
                        f"<span style='color:#E50914;font-size:0.68rem;margin-top:4px;flex-shrink:0;"
                        f"text-shadow:0 0 8px rgba(229,9,20,0.55)'>▶</span>"
                        f"<span style='font-size:0.95rem;color:rgba(255,255,255,0.88);line-height:1.62'>{_s[2:]}</span></div>")
                elif _s:
                    _lines.append(
                        f"<div style='font-size:0.95rem;color:rgba(255,255,255,0.88);"
                        f"line-height:1.68;margin-bottom:3px'>{_s}</div>")
                else:
                    _lines.append("<div style='height:4px'></div>")

            st.markdown(
                f"<div style='display:flex;margin:8px 0;"
                f"animation:fadeSlideRight 0.32s ease {delay} both'>"
                f"<div style='width:34px;height:34px;border-radius:50%;"
                f"background:linear-gradient(135deg,#E50914,#7c000a);"
                f"display:flex;align-items:center;justify-content:center;font-size:1rem;"
                f"flex-shrink:0;align-self:flex-end;margin-right:9px;"
                f"box-shadow:0 0 16px rgba(229,9,20,0.40)'>🤖</div>"
                f"<div style='max-width:80%'>"
                f"<div style='font-size:0.60rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;"
                f"color:rgba(229,9,20,0.60);margin-bottom:4px;padding-left:4px'>ATLAS</div>"
                f"<div style='background:rgba(12,10,24,0.90);"
                f"border:1px solid rgba(255,255,255,0.08);border-radius:18px 18px 18px 4px;"
                f"padding:14px 18px;backdrop-filter:blur(24px);"
                f"box-shadow:0 4px 24px rgba(0,0,0,0.45),inset 0 1px 0 rgba(255,255,255,0.04)'>"
                + "".join(_lines) +
                f"</div></div></div>",
                unsafe_allow_html=True)

# ── TYPING DOTS ───────────────────────────────────────────────────────────────
if st.session_state.get("_atlas_needs_reply", False):
    st.markdown(
        "<div style='display:flex;align-items:center;gap:10px;margin:8px 0;padding-left:43px'>"
        "<div style='display:flex;gap:5px;align-items:center;"
        "background:rgba(12,10,24,0.85);border:1px solid rgba(255,255,255,0.07);"
        "border-radius:20px;padding:9px 16px'>"
        "<div style='width:7px;height:7px;border-radius:50%;background:#E50914;"
        "animation:typing 1.1s ease-in-out infinite 0s'></div>"
        "<div style='width:7px;height:7px;border-radius:50%;background:#E50914;"
        "animation:typing 1.1s ease-in-out infinite 0.22s'></div>"
        "<div style='width:7px;height:7px;border-radius:50%;background:#E50914;"
        "animation:typing 1.1s ease-in-out infinite 0.44s'></div>"
        "<span style='font-size:0.76rem;color:rgba(255,255,255,0.38);margin-left:8px;"
        "font-style:italic'>ATLAS is thinking...</span>"
        "</div></div>",
        unsafe_allow_html=True)

# ── PROCESS AI REPLY ──────────────────────────────────────────────────────────
# Only process if the trigger flag is set — prevents nav buttons from triggering AI
_needs_ai = st.session_state.get("_atlas_needs_reply", False)
if _needs_ai:
    st.session_state._atlas_needs_reply = False
    try:
        from model_api import query_model
        import re as _re
        history = st.session_state.chat_messages[-10:]
        conv    = "".join(
            ("User" if m["role"]=="user" else "Coach") + ": " + m["content"] + "\n"
            for m in history[:-1])
        full_prompt = (system_prompt + "\n\nConversation:\n" + conv +
                       "\nUser: " + history[-1]["content"] + "\nCoach:")
        reply = query_model(full_prompt, max_tokens=320).strip()
        for _pfx in ["Assistant:","ATLAS:","AI Coach:","Coach:"]:
            if reply.startswith(_pfx): reply = reply[len(_pfx):].strip()
        _clean = [ln for ln in reply.splitlines()
                  if not (ln.strip().startswith("{") or ln.strip().startswith("[")
                          or (ln.strip().startswith('"') and ln.strip().endswith('",')))]
        reply = _re.sub(r"\{[^}]*\}","","\n".join(_clean))
        reply = _re.sub(r"\[[^\]]*\]","",reply)
        reply = _re.sub(r"\n{3,}","\n\n",reply).strip()
        if not reply: reply = "Great question! Try asking me again."
        st.session_state.chat_messages.append({"role":"assistant","content":reply})
        try:
            from utils.db import save_chat_history
            save_chat_history(uname, st.session_state.chat_messages[-30:])
        except Exception: pass
        st.rerun()
    except Exception as e:
        st.error("ATLAS error: " + str(e))

st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

# ── INPUT BAR ─────────────────────────────────────────────────────────────────
st.markdown(
    "<div style='background:linear-gradient(135deg,rgba(10,8,22,0.94),rgba(14,6,8,0.90));"
    "border:1.5px solid rgba(229,9,20,0.20);border-radius:18px;"
    "padding:13px 16px;backdrop-filter:blur(28px);"
    "box-shadow:0 8px 36px rgba(0,0,0,0.55),inset 0 1px 0 rgba(255,255,255,0.03)'>",
    unsafe_allow_html=True)
with st.form("chat_form", clear_on_submit=True):
    inp_col, btn_col = st.columns([5,1])
    with inp_col:
        user_input = st.text_input(
            "", placeholder="Ask ATLAS about workouts, nutrition, recovery, goals...",
            key="chat_input_field", label_visibility="collapsed")
    with btn_col:
        send = st.form_submit_button("Send ➤", use_container_width=True)
    if send and user_input.strip():
        st.session_state.chat_messages.append({"role":"user","content":user_input.strip()})
        st.session_state._atlas_needs_reply = True
        st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

# ── BOTTOM BAR ────────────────────────────────────────────────────────────────
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
ba1, ba2, ba3 = st.columns([2,3,5])
with ba1:
    if st.session_state.chat_messages:
        if st.button("🗑️ Clear Chat", key="clear_chat", use_container_width=True):
            st.session_state.chat_messages = []
            st.rerun()
with ba2:
    mc = len(st.session_state.chat_messages)
    if mc > 0:
        ai_c = sum(1 for m in st.session_state.chat_messages if m["role"]=="assistant")
        st.markdown(
            f"<div style='background:rgba(229,9,20,0.06);border:1px solid rgba(229,9,20,0.15);"
            f"border-radius:10px;padding:8px 14px;text-align:center;font-size:0.76rem;"
            f"color:rgba(255,255,255,0.40)'>💬 {mc} messages &nbsp;·&nbsp; 🤖 {ai_c} replies</div>",
            unsafe_allow_html=True)

# ── WHAT ATLAS KNOWS (empty state only) ───────────────────────────────────────
if not st.session_state.chat_messages:
    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
    caps = [("🏋️","Workout Plan",f"{len(sdays)}-day personalised"),
            ("🥗","Your Diet",f"{diet_lbl} · {data.get('goal','Fitness')}"),
            ("📊","Body Stats",f"{data.get('weight','?')}kg · {data.get('height','?')}cm"),
            ("⚙️","Equipment",", ".join(data.get("equipment",[])) if data.get("equipment") else "Bodyweight")]
    cc = st.columns(4)
    for i,(icon,title,sub) in enumerate(caps):
        with cc[i]:
            st.markdown(
                f"<div style='background:rgba(10,8,20,0.68);border:1px solid rgba(229,9,20,0.12);"
                f"border-radius:14px;padding:14px 14px;text-align:center;"
                f"animation:fadeSlideUp 0.5s ease {0.08*i:.2f}s both'>"
                f"<div style='font-size:1.5rem;margin-bottom:6px'>{icon}</div>"
                f"<div style='font-size:0.66rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;"
                f"color:rgba(229,9,20,0.60);margin-bottom:4px'>{title}</div>"
                f"<div style='font-size:0.74rem;color:rgba(255,255,255,0.38);line-height:1.4'>{sub}</div>"
                f"</div>",
                unsafe_allow_html=True)