<div align="center">

<!-- Animated title banner -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=220&section=header&text=FitPlan%20Pro&fontSize=80&fontColor=fff&animation=twinkling&fontAlignY=38&desc=AI-Powered%20Fitness%20Tracking%20%26%20Planning%20System&descAlignY=60&descColor=ccc&descSize=20" width="100%"/>

<!-- Badges row -->
<p>
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white"/>
  <img src="https://img.shields.io/badge/Groq_AI-F55036?style=for-the-badge&logo=groq&logoColor=white"/>
  <img src="https://img.shields.io/badge/HuggingFace-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black"/>
</p>

<p>
  <img src="https://img.shields.io/badge/Pages-15%20Built-blueviolet?style=flat-square"/>
  <img src="https://img.shields.io/badge/Badges-18%20Achievements-gold?style=flat-square"/>
  <img src="https://img.shields.io/badge/Data-Real--time%20Sync-brightgreen?style=flat-square"/>
  <img src="https://img.shields.io/badge/Nav-Mobile%20%2B%20Desktop-blue?style=flat-square"/>
  <img src="https://img.shields.io/badge/AI-Context--Aware%20Coach-red?style=flat-square"/>
</p>

<br/>

> **FitPlan Pro** is a complete AI fitness management system.  
> It generates a personalised workout and diet plan for each user, then tracks every aspect of their fitness journey — workouts, sleep, cardio, streaks, weight, records, and progress photos — all in real time.

<br/>

</div>

---

## 📋 Table of Contents

- [What is FitPlan Pro](#-what-is-fitplan-pro)
- [Tech Stack](#-tech-stack--why-each-was-chosen)
- [Project Structure](#-project-structure)
- [Pages Overview](#-pages-overview)
  - [Login](#1-login--apppy)
  - [Profile](#2-profile--1_profilepy)
  - [Dashboard](#3-dashboard--2_dashboardpy)
  - [Workout Plan](#4-workout-plan--3_workout_planpy)
  - [Diet Plan](#5-diet-plan--4_diet_planpy)
  - [AI Coach](#6-ai-coach--5_ai_coachpy)
  - [Records](#7-records--6_recordspy)
  - [Progress Photos](#8-progress-photos--7_progress_photospy)
  - [History](#9-history--9_historypy)
  - [Meal Planner](#10-ai-meal-planner--11_meal_plannerpy)
  - [Sleep Tracker](#11-sleep-tracker--12_sleep_trackerpy)
  - [Cardio Tracker](#12-cardio-tracker--13_cardio_trackerpy)
  - [Streaks](#13-streaks--heatmap--14_streakspy)
  - [Progress Charts](#14-progress-charts--15_progress_chartspy)
  - [Navigation](#15-navigation--nav_componentpy)
- [Database Design](#-database-design)
- [Data Flow](#-data-flow)
- [New Features](#-new-features-added)
- [Setup and Deployment](#-setup--deployment)
- [Environment Variables](#-environment-variables)
- [Known Limitations](#-known-limitations)

---

## 🏋️ What is FitPlan Pro

```
Most fitness apps give everyone the same generic plan.
FitPlan Pro builds the plan around the user — not a template.
```

One profile setup. The AI reads your age, weight, goal, equipment, diet preference, and weekly schedule. It generates a complete day-by-day plan. From that point, every page reads that data and updates dynamically as you log your activity.

**The three questions the app answers every day:**

| Question | Where it is answered |
|---|---|
| Where am I in my plan? | Dashboard — stat cards, calendar, progress bar |
| What do I do today? | Workout Plan — exercises, sets, reps, timer |
| How consistent have I been? | Streaks, History, Charts |

---

## 🛠 Tech Stack & Why Each Was Chosen

<table>
<tr>
<td width="140"><b>Technology</b></td>
<td><b>Why this and not the alternative</b></td>
</tr>
<tr>
<td><img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white&style=flat-square"/> Python</td>
<td>Fastest path from AI/ML logic to a working web app. The entire team knew it. No context switching between backend and frontend languages.</td>
</tr>
<tr>
<td><img src="https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white&style=flat-square"/> Streamlit</td>
<td>Converts Python scripts directly into interactive web pages — no HTML, no JavaScript, no React setup. Saved weeks of frontend scaffolding. Trade-off: re-runs the full script on each interaction, managed with <code>session_state</code> caching.</td>
</tr>
<tr>
<td><img src="https://img.shields.io/badge/Groq_Llama3-F55036?style=flat-square"/> Groq AI</td>
<td>Groq runs Llama 3 on custom LPU hardware. Response time is 200-400ms vs 2-4 seconds for GPT-4. For a fitness coach that needs to feel like a conversation, that speed difference is very noticeable. Free tier supports our volume.</td>
</tr>
<tr>
<td><img src="https://img.shields.io/badge/Supabase-3ECF8E?logo=supabase&logoColor=white&style=flat-square"/> Supabase</td>
<td>Built on PostgreSQL — a real relational database with proper SQL, foreign keys, and structured schema. Firebase was considered but its document model is not ideal for structured fitness data with relationships.</td>
</tr>
<tr>
<td>🗄️ SQLite fallback</td>
<td>If Supabase is unreachable, the app automatically falls back to local SQLite. The app never crashes due to a network issue during demo or evaluation.</td>
</tr>
<tr>
<td><img src="https://img.shields.io/badge/HuggingFace-FFD21E?logo=huggingface&logoColor=black&style=flat-square"/> HuggingFace</td>
<td>Free deployment platform that supports Python/Streamlit natively. Gives a public URL that works on any device with zero server configuration.</td>
</tr>
<tr>
<td>📧 Brevo API</td>
<td>Sends OTP emails and daily/weekly notifications via REST API. Gmail SMTP was ruled out — unreliable in cloud deployments and requires OAuth setup. Brevo works with a single API key and has 300 free emails/day.</td>
</tr>
</table>

---

## 📁 Project Structure

```
fitplan-pro/
│
├── app.py                      # Entry point — login, signup, OTP reset
├── auth_token.py               # Session tokens, login state, logout
├── nav_component.py            # Responsive nav bar (desktop + mobile)
│
├── utils/
│   ├── db.py                   # All 60+ database functions — one file
│   ├── model_api.py            # Groq API wrapper with retry logic
│   ├── prompt_builder.py       # Prompt construction + BMI calculator
│   ├── streak_manager.py       # Streak calculation + milestone detection
│   └── achievements.py         # 18 badge definitions and unlock logic
│
├── pages/
│   ├── 1_Profile.py            # User profile + plan generation trigger
│   ├── 2_Dashboard.py          # Command centre — overview of everything
│   ├── 3_Workout_Plan.py       # Day-by-day workout with timer + swap
│   ├── 4_Diet_Plan.py          # AI meals + water + grocery list
│   ├── 5_ai_coach.py           # Context-aware AI coaching chat
│   ├── 6_records.py            # PRs, measurements, 1RM calculator
│   ├── 7_progress_photos.py    # Upload + compare transformation photos
│   ├── 9_history.py            # Full workout log + consistency score
│   ├── 11_meal_planner.py      # On-demand custom meal plan generator
│   ├── 12_sleep_tracker.py     # Sleep hours + quality logging
│   ├── 13_cardio_tracker.py    # Cardio sessions — run, cycle, swim etc
│   ├── 14_streaks.py           # Streak counter + GitHub-style heatmap
│   └── 15_progress_charts.py   # Weight, sleep, cardio, measurements charts
│
├── weekly_email.py             # Sunday summary email sender
├── daily_reminder.py           # Daily workout reminder email
└── streak_manager.py           # (also at root for direct import)
```

---

## 📄 Pages Overview

---

### 1. Login — `app.py`

The entry point. Handles three functions in one screen using tabs — no separate pages for signup vs login.

**What it does:**
- New users sign up with username + password (SHA-256 hashed)
- Returning users log in — token stored in Supabase for session persistence
- Forgot password triggers a 6-digit OTP sent via Brevo email API, valid for 10 minutes

**Why SHA-256 over bcrypt:**  
SHA-256 is in Python's standard `hashlib` — no extra dependency. For a student project on HuggingFace's free tier where package control is limited, reliability matters more than the marginal security improvement of bcrypt (which is more important for financial systems).

---

### 2. Profile — `1_Profile.py`

The foundation of the entire system. Everything the AI generates depends on what is entered here.

**Data collected:**

| Field | Why it matters |
|---|---|
| Age, weight, height | BMI calculation and calorie targets |
| Fitness goal | Determines rep ranges, rest periods, and calorie structure |
| Days per week | Controls how many workout days are generated |
| Equipment available | Ensures exercises match what the user actually has |
| Diet preference | Veg / non-veg / flexible — changes every meal, every day |
| Display name | Shown across all pages instead of raw username or email |

**Key behaviour:** When the profile is saved, any existing active plan is deleted. This is intentional — a changed goal means the old plan is completely wrong for the new target. A confirmation dialog warns the user before this happens.

**New features:**
- `3-step onboarding banner` — guides first-time users through Profile > Generate Plan > Start Tracking
- `Live BMI display` — calculated instantly on save using the standard formula, shown with category label

---

### 3. Dashboard — `2_Dashboard.py`

The command centre. Designed to answer three questions the moment the app opens: Where am I? What is today? How consistent have I been?

**Layout:**

```
[ Streak ] [ Done ] [ Progress % ] [ Total Days ]     <- stat cards

[ TODAY: DAY 3 - UPPER BODY PULL ]  [ Not Done Yet ]  <- hero bar

[ Today's Exercises ] | [ This Week Chart ] | [ Profile Card ]
[ Mark Complete / Skip ] | [ Weight Log    ] | [ Calendar     ]
[ Plan Progress Bar   ] | [ Done/Skip/Left ] |                 
[ Motivational Quote  ] |                    |                 

[ Up Next — upcoming days ]  |  [ Quick Access links ]
                             |  [ View Full Plan button ]
```

**Dynamic updates:** Marking a day complete updates the streak counter, the calendar cell, the stat cards, and the database — all in the same rerun without navigating away.

**Missed day logging:** If past-due days are still pending, a section appears below with each missed workout and two buttons — mark done or skip — for retroactive logging.

**Achievements:** 18 badges unlock automatically. When a new one unlocks, a toast notification appears in the top-right corner.

---

### 4. Workout Plan — `3_Workout_Plan.py`

The largest page — 1,400 lines. Shows the full AI-generated plan and handles all workout logging.

**Core features:**

```
Plan generation  ->  Groq (Llama 3) receives full profile as structured prompt
                     Returns JSON: exercises, sets, reps, rest, form tips, meals
                     Stored in Supabase and session_state

Day navigation   ->  Click any day card to expand it
                     Today's card is highlighted automatically

Exercise logging ->  Checkbox per exercise
                     When all are checked -> celebration animation + streak update
                     Saves to: progress table (plan-linked) AND workout_history table (global)

RPE slider       ->  Rate of Perceived Exertion 1-10
                     Saved per exercise per day
                     Helps track whether exercises are getting easier over time
```

**Persistent timer — how it actually works:**

> Streamlit re-runs the entire Python script on every button press. A normal `time.sleep()` timer would reset on every interaction. The solution: the timer start timestamp is stored in JavaScript's `sessionStorage` — in the browser, not on the server. On every render, JavaScript reads the stored start time and calculates elapsed time from the wall clock. Accurate to the millisecond, survives infinite Streamlit re-runs.

**Exercise swap:**

```
User clicks Swap on any exercise
  -> App calls Groq with: exercise name + muscle group + user equipment
  -> Groq returns: replacement exercise targeting same muscle
  -> Updates session_state immediately
  -> Writes to database for persistence
```

**Spotify music player:** 9 genre options (Workout, Bollywood, Pop, Rock, Hip-Hop, Tollywood, Classical, Jazz, Electronic). Uses Spotify's embed API — no user login required. Genre choice is saved per user.

---

### 5. Diet Plan — `4_Diet_Plan.py`

Shows the AI-generated meal plan per day, with full switching and automation features.

**Diet type switching:** Changing from Vegetarian to Non-Vegetarian does not just change labels — it triggers a full Groq regeneration with meals that are actually appropriate for that diet type.

**AI meal swap:**
```
User presses Swap on any meal
  -> Groq receives: meal name + diet type + cuisine preference + calorie target
  -> Returns: 2-3 alternatives that match the nutritional profile
  -> User picks one -> saved to database
```

**Grocery list generation:** Presses one button. The app reads the next 7 days of meal data, sends the ingredient list to Groq, and gets back a categorised shopping list (Vegetables, Proteins, Grains, Dairy, Condiments).

**Why meals and workouts are generated in the same API call:**  
Context. When the AI generates both together, it knows the training load for each day and can match calories accordingly — harder days get more carbohydrates, rest days get lower calories. Two separate calls would lose this context.

---

### 6. AI Coach — `5_ai_coach.py`

Not a generic chatbot. Every response is grounded in the user's actual data.

**How context injection works:**

```python
context_block = f"""
User: {username}
Current streak: {streak} days
This week: {done_this_week}/7 workouts completed
Last workout: {last_workout_title}
7-day avg sleep: {avg_sleep}h
Diet adherence: {diet_pct}%
Recent PRs: {recent_prs}
"""
# This is prepended to EVERY message sent to Groq
# The AI knows the user's situation before answering
```

The coach can say "I see you only completed 3 of 7 workouts this week — what is getting in the way?" rather than generic advice.

**Chat history:** Last 30 messages stored in database, loaded on open. The 30-message limit controls token costs while keeping enough context for coherent conversation.

---

### 7. Records — `6_records.py`

Three sections: Personal Records, Body Measurements, and 1RM Calculator.

**1RM Calculator uses the Epley formula:**
```
1RM = weight_lifted x (1 + reps / 30)
```
The user enters what they lifted and how many reps. The estimated 1-rep maximum appears instantly. No API call — pure Python math. Standard formula used by every serious gym tracking app.

**Illustrated empty states:** Instead of a blank page for new users, each section shows an icon, a description, and a clear call-to-action button guiding them to log their first entry.

---

### 8. Progress Photos — `7_progress_photos.py`

Upload transformation photos with a label (Front, Side, Back, Custom) and compare any two side by side.

**Why base64 storage in the database instead of a file server:**  
No separate object storage service needed. No S3 bucket, no CDN configuration, no Supabase Storage bucket policies. Photos stored as base64 strings travel with the database and work out of the box. Trade-off: base64 is ~33% larger than binary. Acceptable for a project of this scale. For production, object storage would be used.

---

### 9. History — `9_history.py`

Chronological log of all completed workouts across all plans.

**Consistency score formula:**
```
Consistency % = completed_days / total_past_due_days x 100
```
This only counts days that have already passed — not future days. A user who missed day 5 but completed everything else is scored on what they had the chance to do, not penalised for the future.

**Save-on-load sync:** When History loads, it checks if today's completed workouts are in the `workout_history` table. If any are missing (because the user completed a workout but had not yet visited History), it saves them. This was the fix for the streak page showing incorrect counts.

---

### 10. AI Meal Planner — `11_meal_planner.py`

On-demand meal plan generator separate from the main Diet Plan page.

**The difference:**
- Diet Plan page shows meals tied to the workout plan — same meals for the plan duration
- Meal Planner is for custom on-demand plans — "give me a high-protein vegetarian plan under 1800 calories for today"

Users can specify exact macro targets (protein, carbs, fat in grams). The last 10 generated plans are saved and can be reloaded with one click.

---

### 11. Sleep Tracker — `12_sleep_tracker.py`

Log hours slept and a quality score (1-5) for any day in the last 30 days.

**Dynamic update — 5-step pattern:**

```
1. save_sleep()              -> writes to database
2. _load_sleep.clear()       -> invalidates the page cache
3. get_sleep() -> session_state  -> reloads fresh data
4. st.cache_data.clear()     -> clears Charts page cache too
5. st.rerun()                -> page refreshes with new data
```

The 7-night bar chart, stat cards, and history table all show updated data immediately after saving — not after a 2-minute cache expiry.

---

### 12. Cardio Tracker — `13_cardio_tracker.py`

Separate from the structured workout plan. Tracks supplemental cardio activity.

**12 activity types:** Running, Cycling, Swimming, HIIT, Walking, Rowing, Jump Rope, Boxing, Yoga, Elliptical, Stair Climber, Custom.

Each activity has automatic calorie estimation based on body weight and duration using standard MET (Metabolic Equivalent of Task) values. Users can override the estimate with their actual calorie burn from a device.

**Delete functionality:** Each entry has a delete button. After delete, the same 5-step pattern runs — cache clear, reload, rerun — so the entry disappears from the list immediately.

---

### 13. Streaks & Heatmap — `14_streaks.py`

Shows current streak, longest streak, a 12-week activity heatmap, and milestone badges.

**Streak calculation:**
```python
workout_dates = set of all dates with completed workouts
# Count backwards from today
# Each consecutive day increments the streak
# First gap stops the count
```

**Session state merge:** If a user just marked today as done on the Dashboard in the same session, `session_state.tracking` is merged into `workout_dates` before calculation. The streak number is accurate immediately — does not wait for the 60-second database cache to refresh.

**18 milestone badges:**

| Days | Badge | Title |
|---|---|---|
| 7 | 🥉 | Week Warrior |
| 14 | ⚡ | Fortnight |
| 21 | 🔥 | 3-Week Fire |
| 30 | 🥈 | Month Beast |
| 60 | 💎 | Diamond |
| 90 | 🥇 | Legend |
| 180 | 👑 | Elite |

---

### 14. Progress Charts — `15_progress_charts.py`

Four tabs: Weight trend, Sleep history, Cardio calories, Body measurements.

**Cache strategy:**
- All four data loaders use `@st.cache_data(ttl=60)`
- Sleep and Cardio pages call `st.cache_data.clear()` after every save
- This means new data logged on those pages appears in Charts within seconds — not minutes

**Weight chart:** Goal-aware colouring. A downward trend is green for fat loss goal, red for muscle gain goal. An upward trend is green for muscle gain, red for fat loss. The chart reads the user's goal from their profile and colours accordingly.

---

### 15. Navigation — `nav_component.py`

One file. Controls navigation for all 15 pages. Called with a single line on every page:
```python
from nav_component import render_nav
render_nav("dashboard", uname)
```

**Desktop (wider than 900px):**
- Persistent slim top bar with all 12 page icons always visible
- Active page highlighted with a border and dot indicator
- User chip (avatar + name) and Sign Out button on the right
- No click needed to see all pages

**Mobile and tablet (900px or narrower):**
- Logo + current page pill + hamburger button
- Hamburger animates to X when open
- Drawer slides down with 4-column grid (tablet) or 3-column (phone)
- Dark overlay appears behind drawer — clicking it closes the drawer

**How hidden Streamlit buttons work:**

> Streamlit requires real `st.button()` + `st.switch_page()` for navigation. But 12 visible buttons would break the layout. The solution: buttons are rendered but pushed off-screen with CSS (`left: -9999px`). The visible icon elements call `document.getElementById('fpbtn_X').click()` in JavaScript. Three hide layers run at 80ms, 400ms, and 1200ms after render to catch any late Streamlit re-renders that might expose the buttons.

---

## 🗄 Database Design

**14 tables, all keyed on username:**

```
users                 -> username, password_hash, email, created_at
user_profiles         -> username, age, weight, height, goal, equipment, diet_type, display_name
active_plans          -> plan_id, username, days[], dietary_type, created_at
progress              -> username, plan_id, day_number, workout_checks, dietary_checks
workout_history       -> username, date, day, muscle_group, exercises, status
streaks               -> username, current_streak, longest_streak, last_completed_date
sleep_logs            -> username, date, hours, quality, notes
cardio_logs           -> username, date, activity, duration, distance, calories
weight_logs           -> username, date, weight_kg
personal_records      -> username, exercise, weight, reps, date
body_measurements     -> username, date, chest, waist, hips, arms, thighs
progress_photos       -> username, date, label, image_base64
chat_history          -> username, messages_json, updated_at
water_intake          -> username, date, glasses
```

**Why two separate tables for progress and workout_history:**

`progress` is tied to a specific plan. If you generate a new plan, old progress is archived under the old `plan_id`. `workout_history` is plan-independent — it records every workout ever completed across all plans. The Streak page needs all historical workout dates regardless of which plan they belonged to. These are two different questions requiring two different data sources.

---

## 🔄 Data Flow

```
User logs a workout
       |
       v
save_progress()  ─────────────────> progress table (plan-linked)
save_workout_history()  ──────────> workout_history table (global)
update_streak()  ─────────────────> streaks table
       |
       v
session_state.tracking updated
       |
       v
st.rerun() triggered
       |
       v
Dashboard re-reads session_state  -> stat cards update instantly
Streak page merges session_state  -> streak number accurate immediately
Charts page cache cleared         -> new data visible within 60 seconds
```

---

## ✨ New Features Added

Beyond the core plan and tracking, the following features were built and are fully working:

| Feature | Page | Description |
|---|---|---|
| OTP password reset | Login | 6-digit code via Brevo email, expires in 10 min |
| Onboarding banner | Profile | 3-step guide for first-time users, dismissable |
| Live BMI display | Profile | Calculated on save, shown with category label |
| Persistent workout timer | Workout | JavaScript sessionStorage — survives Streamlit re-runs |
| Exercise swap with AI | Workout | Groq replaces any exercise with an equipment-appropriate alternative |
| RPE logging | Workout | Effort score per exercise, saved to database |
| Spotify music player | Workout | 9 genres, embedded player, no login needed |
| Workout completion celebration | Workout | Confetti animation + streak toast on day complete |
| AI meal swap | Diet | Replace any meal with AI-suggested alternatives |
| Smart grocery list | Diet | Auto-generated from next 7 days of meals |
| Supplement guide | Diet | Goal-specific, instant, no API call |
| Water tracker | Diet + Workout | 8-glass daily goal, resets at midnight |
| Context-aware AI coach | Coach | Injects real user data into every message |
| 1RM calculator | Records | Epley formula, instant, no API call |
| Illustrated empty states | Records, History, Photos | Guides users with no data yet |
| Progress photo comparison | Photos | Side-by-side comparison of any two uploaded photos |
| Activity heatmap | Streaks | 12-week GitHub-style workout frequency grid |
| 18 achievement badges | Streaks + Dashboard | Auto-unlock with toast notifications |
| Session state streak merge | Streaks | Streak accurate immediately without cache wait |
| Responsive navigation | All pages | Desktop persistent bar, mobile hamburger drawer |
| Daily reminder email | Automation | Fires only if today's workout is still pending |
| Weekly progress email | Automation | Sunday summary with real data for that week |
| Consistency score | History | Based on past-due days only — fair measurement |
| Save-on-load history sync | History | Fixes streak data gap for users who skip History page |

---

## 🚀 Setup & Deployment

### Local development

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/fitplan-pro.git
cd fitplan-pro

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # Linux / Mac
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set environment variables (see below)
cp .env.example .env
# Edit .env with your keys

# 5. Run the app
streamlit run app.py
```

### HuggingFace Spaces deployment

```
1. Create a new Space on HuggingFace
2. Select SDK: Streamlit
3. Upload all files maintaining the same folder structure
4. Add all environment variables in Settings > Repository Secrets
5. The app deploys automatically on every push
```

---

## 🔐 Environment Variables

Create a `.env` file in the root directory with the following:

```env
# Groq API — for AI plan generation and coaching
GROQ_API_KEY=your_groq_api_key_here

# Supabase — primary database
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key

# Brevo — email notifications and OTP
BREVO_API_KEY=your_brevo_api_key
BREVO_SENDER_EMAIL=noreply@yourapp.com

# Optional — if not set, app falls back to SQLite automatically
# SUPABASE_URL and SUPABASE_KEY absence triggers SQLite mode
```

> **Note:** The app is designed to work without any environment variables using the SQLite fallback. For full functionality including email features, all keys are required.

---

## ⚠️ Known Limitations

| Limitation | Impact | Production fix |
|---|---|---|
| No automated tests | All testing was manual | Add pytest for db.py and streak_manager.py |
| Base64 photo storage | Not scalable past a few hundred photos | Move to Supabase Storage or S3 |
| Single server (HuggingFace) | No horizontal scaling | Move to a containerised deployment with load balancing |
| Measurements tab has no save button | Users must go to Records page to log measurements | Add save form directly to the Charts measurements tab |
| 60-second streak cache | Other sessions see old streak for up to 60s after workout | Reduce TTL or implement websocket update |

---

## 📊 Page Summary

| # | Page | Lines | Key technical feature |
|---|---|---|---|
| - | app.py | 896 | OTP login, SHA-256 auth, Brevo email |
| 1 | Profile | 791 | BMI calculator, onboarding, plan reset |
| 2 | Dashboard | 657 | Live calendar, missed day logging, achievements |
| 3 | Workout Plan | 1,410 | JS timer, exercise swap, RPE, Spotify |
| 4 | Diet Plan | 829 | AI meal swap, grocery list, water tracker |
| 5 | AI Coach | 483 | Context injection, 30-msg history cap |
| 6 | Records | 525 | Epley 1RM, empty states, ttl=180 cache |
| 7 | Progress Photos | 412 | Base64 storage, side-by-side comparison |
| 9 | History | 322 | Consistency score, save-on-load sync |
| 11 | Meal Planner | 751 | Custom macros, saved history, on-demand plans |
| 12 | Sleep Tracker | 419 | 5-step dynamic update, quality chart |
| 13 | Cardio Tracker | 464 | 12 activity types, calorie estimation, delete |
| 14 | Streaks | 378 | Heatmap, 18 milestones, session_state merge |
| 15 | Progress Charts | 435 | 4-tab charts, cross-page cache clear |
| - | nav_component.py | 417 | Responsive nav, hidden button JS trick |

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=120&section=footer&animation=twinkling" width="100%"/>

<p>
  <b>FitPlan Pro</b> — Built with Python, Streamlit, Supabase, and Groq AI
</p>

<p>
  <img src="https://img.shields.io/badge/Status-Live%20on%20HuggingFace-brightgreen?style=for-the-badge"/>
</p>

</div>


