# -*- coding: utf-8 -*-
"""
FitPlan Pro — Main entry point (Login / Signup / Forgot Password)
Place this file at the root of your project alongside auth_token.py
"""
import streamlit as st
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from auth_token import (login, initiate_signup, complete_signup,
                        reset_password_request, reset_password_confirm,
                        verify_token)

st.set_page_config(
    page_title="FitPlan Pro",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ── GLOBAL CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700&display=swap');

[data-testid="stAppViewContainer"]::before{
  content:'';position:fixed;inset:0;z-index:0;
  background:url('https://images.unsplash.com/photo-1534438327276-14e5300c3a48?fm=jpg&w=1800&q=80&fit=crop')
    center center/cover no-repeat;
  filter:blur(10px) brightness(0.18) saturate(0.50);transform:scale(1.08);}
[data-testid="stAppViewContainer"]{
  background:radial-gradient(ellipse at 50% 0%,rgba(229,9,20,0.12) 0%,transparent 60%),
    linear-gradient(180deg,rgba(3,1,0,0.95) 0%,rgba(5,2,0,0.90) 100%)!important;
  position:relative;}
[data-testid="stAppViewContainer"]>section>div.block-container{
  position:relative;z-index:2;max-width:480px!important;
  margin:0 auto!important;padding:32px 20px 80px!important;}
#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stDecoration"],
[data-testid="stSidebarNav"],[data-testid="collapsedControl"],
section[data-testid="stSidebar"]{display:none!important;}
html,body,.stApp{background:#050202!important;color:#fff!important;font-family:'DM Sans',sans-serif!important;}

/* ── Inputs ── */
input,.stTextInput>div>div>input,[data-baseweb="input"] input{
  background:#0d0408!important;background-color:#0d0408!important;
  border:1.5px solid rgba(229,9,20,0.35)!important;color:#fff!important;
  border-radius:12px!important;font-family:'DM Sans',sans-serif!important;
  font-size:1rem!important;padding:13px 16px!important;
  box-shadow:inset 0 0 0 9999px #0d0408!important;
  -webkit-box-shadow:inset 0 0 0 9999px #0d0408!important;
  caret-color:#E50914!important;transition:all 0.22s!important;}
input:focus,[data-baseweb="input"] input:focus{
  border-color:rgba(229,9,20,0.75)!important;
  box-shadow:inset 0 0 0 9999px #0d0408,0 0 0 3px rgba(229,9,20,0.15)!important;
  -webkit-box-shadow:inset 0 0 0 9999px #0d0408!important;outline:none!important;}
[data-baseweb="input"]{background:#0d0408!important;border:1.5px solid rgba(229,9,20,0.35)!important;border-radius:12px!important;}
input:-webkit-autofill,input:-webkit-autofill:focus{
  -webkit-box-shadow:0 0 0 9999px #0d0408 inset!important;-webkit-text-fill-color:#fff!important;}
[data-testid="stWidgetLabel"],[data-testid="stWidgetLabel"] p{
  color:rgba(255,255,255,0.85)!important;font-weight:600!important;font-size:0.90rem!important;}

/* ── Buttons ── */
.stButton>button{
  background:linear-gradient(135deg,#E50914,#c0000c)!important;border:none!important;
  color:#fff!important;border-radius:12px!important;font-weight:700!important;
  font-size:1rem!important;height:52px!important;letter-spacing:0.5px!important;
  box-shadow:0 4px 20px rgba(229,9,20,0.45),0 0 0 1px rgba(229,9,20,0.20)!important;
  transition:all 0.22s cubic-bezier(0.34,1.56,0.64,1)!important;}
.stButton>button:hover{
  transform:translateY(-3px) scale(1.02)!important;
  box-shadow:0 8px 32px rgba(229,9,20,0.70),0 0 50px rgba(229,9,20,0.25)!important;}
.ghost-btn .stButton>button{
  background:transparent!important;border:1.5px solid rgba(255,255,255,0.18)!important;
  color:rgba(255,255,255,0.65)!important;height:auto!important;
  font-size:0.88rem!important;font-weight:500!important;padding:8px 16px!important;
  box-shadow:none!important;letter-spacing:0!important;}
.ghost-btn .stButton>button:hover{
  border-color:rgba(229,9,20,0.50)!important;color:#fff!important;
  background:rgba(229,9,20,0.10)!important;transform:none!important;box-shadow:none!important;}
.link-btn .stButton>button{
  background:transparent!important;border:none!important;
  color:rgba(229,9,20,0.85)!important;height:auto!important;
  font-size:0.88rem!important;font-weight:600!important;padding:4px 0!important;
  box-shadow:none!important;letter-spacing:0!important;text-decoration:underline!important;}
.link-btn .stButton>button:hover{color:#ff3333!important;transform:none!important;box-shadow:none!important;}

[data-testid="stForm"]{background:transparent!important;border:none!important;}
[data-testid="stFormSubmitButton"] button{
  background:linear-gradient(135deg,#E50914,#c0000c)!important;border:none!important;
  color:#fff!important;border-radius:12px!important;font-weight:700!important;
  font-size:1rem!important;height:52px!important;width:100%!important;
  box-shadow:0 4px 20px rgba(229,9,20,0.45)!important;
  transition:all 0.22s!important;letter-spacing:0.5px!important;}
[data-testid="stFormSubmitButton"] button:hover{
  box-shadow:0 8px 32px rgba(229,9,20,0.70)!important;transform:translateY(-2px)!important;}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"]{
  background:rgba(10,4,2,0.80)!important;border-radius:12px!important;
  padding:4px!important;border:1px solid rgba(229,9,20,0.18)!important;gap:4px!important;}
.stTabs [data-baseweb="tab"]{
  background:transparent!important;color:rgba(255,255,255,0.55)!important;
  border-radius:9px!important;font-weight:600!important;font-size:0.92rem!important;
  padding:8px 20px!important;transition:all 0.18s!important;}
.stTabs [aria-selected="true"]{
  background:linear-gradient(135deg,rgba(229,9,20,0.85),rgba(160,0,12,0.90))!important;
  color:#fff!important;box-shadow:0 2px 12px rgba(229,9,20,0.35)!important;}

html,body,.stApp,.stMarkdown,p,div,span,label{text-shadow:0 1px 4px rgba(0,0,0,0.95)!important;}
.stMarkdown p{color:rgba(255,255,255,0.75)!important;line-height:1.65!important;}

@keyframes fadeUp{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
@keyframes shimmer{0%,100%{opacity:0.85}50%{opacity:1}}
</style>
""", unsafe_allow_html=True)

# ── SESSION DEFAULTS ──────────────────────────────────────────────────────────
if "app_mode" not in st.session_state:
    st.session_state.app_mode = "auth"   # "auth" | "forgot_step1" | "forgot_step2"

# ── LOGO & HERO ───────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center;padding:32px 0 24px;animation:fadeUp 0.6s ease both'>
  <div style='font-family:Bebas Neue,sans-serif;font-size:3.2rem;letter-spacing:8px;
    color:#E50914;text-shadow:0 0 40px rgba(229,9,20,0.70),0 0 80px rgba(229,9,20,0.30);
    animation:shimmer 3s ease-in-out infinite;margin-bottom:4px'>
    ⚡ FITPLAN PRO
  </div>
  <div style='font-size:0.85rem;color:rgba(255,255,255,0.38);letter-spacing:3px;text-transform:uppercase'>
    AI-Powered Fitness Coach
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# FORGOT PASSWORD FLOW
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.app_mode == "forgot_step1":
    st.markdown("""
    <div style='background:rgba(8,4,2,0.85);border:1.5px solid rgba(229,9,20,0.28);
      border-radius:18px;padding:28px;margin-bottom:20px;animation:fadeUp 0.4s ease both;
      position:relative;overflow:hidden'>
      <div style='position:absolute;top:0;left:0;right:0;height:2px;
        background:linear-gradient(90deg,transparent,#E50914,transparent)'></div>
      <div style='font-family:Bebas Neue,sans-serif;font-size:1.8rem;letter-spacing:3px;
        color:#fff;margin-bottom:6px'>🔑 Reset Password</div>
      <div style='font-size:0.88rem;color:rgba(255,255,255,0.50)'>
        Enter your email or username. We'll send a 6-digit code to reset your password.
      </div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("forgot_step1_form"):
        fp_identity = st.text_input(
            "Email or Username",
            placeholder="your@email.com or your_username",
            key="fp_identity_inp"
        )
        fp_submit = st.form_submit_button("📧 Send Reset Code", use_container_width=True)
        if fp_submit:
            if not fp_identity.strip():
                st.error("Please enter your email or username.")
            else:
                with st.spinner("Sending reset code..."):
                    ok, msg = reset_password_request(fp_identity.strip())
                if ok:
                    st.session_state._fp_identity = fp_identity.strip()
                    if msg == "__NO_OTP__":
                        # Dev mode — no email service, skip OTP
                        st.session_state.app_mode = "forgot_step2"
                        st.session_state._fp_skip_otp = True
                    else:
                        st.success(msg)
                        st.session_state.app_mode = "forgot_step2"
                        st.session_state._fp_skip_otp = False
                    st.rerun()
                else:
                    st.error(msg)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='link-btn'>", unsafe_allow_html=True)
    if st.button("← Back to Login", key="fp1_back"):
        st.session_state.app_mode = "auth"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.app_mode == "forgot_step2":
    _skip_otp = st.session_state.get("_fp_skip_otp", False)
    _fp_id    = st.session_state.get("_fp_identity", "")

    st.markdown(f"""
    <div style='background:rgba(8,4,2,0.85);border:1.5px solid rgba(34,197,94,0.35);
      border-radius:18px;padding:28px;margin-bottom:20px;animation:fadeUp 0.4s ease both;
      position:relative;overflow:hidden'>
      <div style='position:absolute;top:0;left:0;right:0;height:2px;
        background:linear-gradient(90deg,transparent,#22c55e,transparent)'></div>
      <div style='font-family:Bebas Neue,sans-serif;font-size:1.8rem;letter-spacing:3px;
        color:#fff;margin-bottom:6px'>✅ New Password</div>
      <div style='font-size:0.88rem;color:rgba(255,255,255,0.50)'>
        {'Enter your new password below.' if _skip_otp else
         'Check your email for the 6-digit code, then set your new password.'}
      </div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("forgot_step2_form"):
        if not _skip_otp:
            fp_otp = st.text_input(
                "6-Digit Reset Code",
                placeholder="e.g. 482931",
                max_chars=6,
                key="fp_otp_inp"
            )
        else:
            fp_otp = "SKIP"

        fp_new_pw  = st.text_input("New Password", type="password",
                                    placeholder="Min 6 characters", key="fp_new_pw")
        fp_new_pw2 = st.text_input("Confirm New Password", type="password",
                                    placeholder="Repeat your password", key="fp_new_pw2")
        fp2_submit = st.form_submit_button("🔒 Update Password", use_container_width=True)

        if fp2_submit:
            if not fp_new_pw.strip():
                st.error("Please enter a new password.")
            elif len(fp_new_pw) < 6:
                st.error("Password must be at least 6 characters.")
            elif fp_new_pw != fp_new_pw2:
                st.error("Passwords don't match. Please try again.")
            else:
                otp_input = fp_otp if not _skip_otp else "000000"
                with st.spinner("Updating password..."):
                    ok, msg = reset_password_confirm(_fp_id, otp_input, fp_new_pw)
                if ok:
                    st.success("✅ " + msg)
                    # Clear forgot password state
                    for k in ["_fp_identity", "_fp_skip_otp"]:
                        st.session_state.pop(k, None)
                    st.session_state.app_mode = "auth"
                    st.session_state._reset_success = True
                    st.rerun()
                else:
                    st.error(msg)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    col_back, col_resend = st.columns(2)
    with col_back:
        st.markdown("<div class='link-btn'>", unsafe_allow_html=True)
        if st.button("← Back to Login", key="fp2_back"):
            st.session_state.app_mode = "auth"
            for k in ["_fp_identity", "_fp_skip_otp"]:
                st.session_state.pop(k, None)
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    if not _skip_otp:
        with col_resend:
            st.markdown("<div class='ghost-btn'>", unsafe_allow_html=True)
            if st.button("🔄 Resend Code", key="fp2_resend"):
                with st.spinner("Resending..."):
                    ok2, msg2 = reset_password_request(_fp_id)
                if ok2 and msg2 != "__NO_OTP__":
                    st.success(msg2)
                else:
                    st.info("Code resent.")
            st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# MAIN AUTH PAGE (Login + Signup tabs)
# ══════════════════════════════════════════════════════════════════════════════
else:
    # ── If already logged in, redirect ────────────────────────────────────────
    if st.session_state.get("logged_in"):
        uname = st.session_state.get("username", "")
        token = st.session_state.get("auth_token", "")
        if uname and token and verify_token(uname, token):
            if "user_data" in st.session_state:
                st.switch_page("pages/2_Dashboard.py")
            else:
                st.switch_page("pages/1_Profile.py")

    # ── Reset success toast ──────────────────────────────────────────────────
    if st.session_state.pop("_reset_success", False):
        st.success("✅ Password reset! Please sign in with your new password.")

    # ── Auth card ────────────────────────────────────────────────────────────
    st.markdown("""
    <div style='background:linear-gradient(135deg,rgba(10,4,2,0.94),rgba(6,3,8,0.92));
      border:1.5px solid rgba(229,9,20,0.22);border-radius:22px;
      padding:28px 28px 22px;margin-bottom:16px;animation:fadeUp 0.5s ease both;
      position:relative;overflow:hidden;
      box-shadow:0 20px 60px rgba(0,0,0,0.70),0 0 0 1px rgba(229,9,20,0.10)'>
      <div style='position:absolute;top:0;left:0;right:0;height:2.5px;
        background:linear-gradient(90deg,transparent,#E50914 35%,rgba(229,9,20,0.40) 65%,transparent)'></div>
    """, unsafe_allow_html=True)

    tab_login, tab_signup = st.tabs(["🔑 Sign In", "🚀 Sign Up"])

    # ── LOGIN ────────────────────────────────────────────────────────────────
    with tab_login:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        with st.form("login_form", clear_on_submit=False):
            lg_id  = st.text_input("Email or Username", placeholder="your@email.com",
                                    key="lg_id")
            lg_pw  = st.text_input("Password", type="password",
                                    placeholder="Your password", key="lg_pw")
            lg_sub = st.form_submit_button("⚡ Sign In", use_container_width=True)
            if lg_sub:
                if not lg_id.strip() or not lg_pw.strip():
                    st.error("Please enter your credentials.")
                else:
                    with st.spinner("Signing in..."):
                        ok, token, username, msg = login(lg_id.strip(), lg_pw)
                    if ok:
                        st.session_state.logged_in  = True
                        st.session_state.auth_token = token
                        st.session_state.username   = username
                        st.success("✅ Welcome back, " + username + "!")
                        if "user_data" in st.session_state:
                            st.switch_page("pages/2_Dashboard.py")
                        else:
                            st.switch_page("pages/1_Profile.py")
                    else:
                        st.error(msg)

        # ── Forgot password link ──────────────────────────────────────────
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        forgot_col1, forgot_col2 = st.columns([3, 2])
        with forgot_col2:
            st.markdown("<div class='link-btn' style='text-align:right'>", unsafe_allow_html=True)
            if st.button("Forgot Password?", key="goto_forgot"):
                st.session_state.app_mode = "forgot_step1"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    # ── SIGNUP ───────────────────────────────────────────────────────────────
    with tab_signup:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        # Two-step signup: initiate → OTP → complete
        if st.session_state.get("_signup_pending"):
            # Step 2: verify OTP
            _su_username = st.session_state.get("_su_username", "")
            _su_email    = st.session_state.get("_su_email", "")
            _su_pw       = st.session_state.get("_su_pw", "")

            st.markdown(
                f"<div style='background:rgba(34,197,94,0.08);border:1px solid rgba(34,197,94,0.28);"
                f"border-radius:12px;padding:12px 16px;margin-bottom:14px;font-size:0.88rem;"
                f"color:rgba(255,255,255,0.70)'>"
                f"📧 Code sent to <b>{_su_email}</b>. Check your inbox.</div>",
                unsafe_allow_html=True
            )
            with st.form("signup_otp_form"):
                su_otp = st.text_input("Verification Code", placeholder="6-digit code",
                                        max_chars=6, key="su_otp_inp")
                su_verify = st.form_submit_button("✅ Verify & Create Account", use_container_width=True)
                if su_verify:
                    if not su_otp.strip():
                        st.error("Please enter the verification code.")
                    else:
                        with st.spinner("Verifying..."):
                            ok, token, msg = complete_signup(_su_username, _su_email, _su_pw, su_otp.strip())
                        if ok:
                            for k in ["_signup_pending","_su_username","_su_email","_su_pw"]:
                                st.session_state.pop(k, None)
                            st.success("🎉 " + msg)
                        else:
                            st.error(msg)

            st.markdown("<div class='ghost-btn'>", unsafe_allow_html=True)
            if st.button("✕ Cancel Signup", key="cancel_signup"):
                for k in ["_signup_pending","_su_username","_su_email","_su_pw"]:
                    st.session_state.pop(k, None)
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        else:
            # Step 1: collect details
            with st.form("signup_form", clear_on_submit=False):
                su_uname = st.text_input("Username", placeholder="Choose a username",
                                          key="su_uname")
                su_email = st.text_input("Email", placeholder="your@email.com",
                                          key="su_email")
                su_pw    = st.text_input("Password", type="password",
                                          placeholder="Min 6 characters", key="su_pw")
                su_pw2   = st.text_input("Confirm Password", type="password",
                                          placeholder="Repeat password", key="su_pw2")
                su_sub   = st.form_submit_button("🚀 Create Account", use_container_width=True)
                if su_sub:
                    if not su_uname.strip() or not su_email.strip() or not su_pw.strip():
                        st.error("All fields are required.")
                    elif su_pw != su_pw2:
                        st.error("Passwords don't match.")
                    elif len(su_pw) < 6:
                        st.error("Password must be at least 6 characters.")
                    else:
                        with st.spinner("Creating account..."):
                            ok, msg = initiate_signup(su_uname.strip(), su_email.strip(), su_pw)
                        if ok:
                            if msg == "__NO_OTP__":
                                # Dev mode — no email service, account created directly
                                st.success("🎉 Account created! Please sign in.")
                            else:
                                st.session_state._signup_pending = True
                                st.session_state._su_username    = su_uname.strip()
                                st.session_state._su_email       = su_email.strip().lower()
                                st.session_state._su_pw          = su_pw
                                st.success(msg)
                                st.rerun()
                        else:
                            st.error(msg)

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Footer ───────────────────────────────────────────────────────────────
    st.markdown("""
    <div style='text-align:center;margin-top:20px;animation:fadeUp 0.7s ease 0.2s both'>
      <div style='font-size:0.72rem;color:rgba(255,255,255,0.22);letter-spacing:1px'>
        🔒 Secure · AI-Powered · Your data stays private
      </div>
    </div>
    """, unsafe_allow_html=True)