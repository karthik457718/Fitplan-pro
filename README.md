<h1 align="center">⚡ FitPlan Pro</h1>

<p align="center">
  <strong>AI-Powered Fitness Tracking &amp; Planning System</strong><br/>
  Personalised workouts &middot; Smart diet plans &middot; Real-time tracking &middot; Context-aware AI coaching
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white" alt="Supabase"/>
  <img src="https://img.shields.io/badge/Groq_AI-F55036?style=for-the-badge&logo=lightning&logoColor=white" alt="Groq"/>
  <img src="https://img.shields.io/badge/HuggingFace_Spaces-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black" alt="HuggingFace"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/15_Pages_Built-blueviolet?style=flat-square" alt="pages"/>
  <img src="https://img.shields.io/badge/18_Achievement_Badges-gold?style=flat-square" alt="badges"/>
  <img src="https://img.shields.io/badge/Real--time_Data_Sync-brightgreen?style=flat-square" alt="sync"/>
  <img src="https://img.shields.io/badge/Mobile_%2B_Desktop_Nav-blue?style=flat-square" alt="nav"/>
  <img src="https://img.shields.io/badge/Context--Aware_AI_Coach-red?style=flat-square" alt="ai"/>
</p>

---

> **FitPlan Pro** is a complete AI fitness management system built in Python and Streamlit.
> It generates a personalised, day-by-day workout and diet plan for each user, then tracks their entire fitness journey across 15 pages in real time.

---

## Table of Contents

- [What is FitPlan Pro](#-what-is-fitplan-pro)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Pages Explained in Detail](#-pages-explained-in-detail)
- [Database Design](#-database-design)
- [Data Flow](#-data-flow)
- [All New Features](#-all-new-features)
- [Setup and Deployment](#-setup--deployment)
- [Environment Variables](#-environment-variables)
- [Known Limitations](#-known-limitations)

---

## What is FitPlan Pro

Most fitness apps give everyone the same generic plan. FitPlan Pro builds the plan around the user — not a template.

One profile setup. The AI reads age, weight, goal, equipment, diet preference, and weekly schedule. It generates a complete day-by-day plan. From that point, every page reads that data and updates dynamically as the user logs activity.

**Three questions the app answers every day:**

| Question | Where it is answered |
|---|---|
| Where am I in my plan? | Dashboard — stat cards, calendar, progress bar |
| What do I do today? | Workout Plan — exercises, sets, reps, timer |
| How consistent have I been? | Streaks, History, Progress Charts |

---

## Tech Stack

| Technology | Why this and not the alternative |
|---|---|
| **Python 3.10** | Fastest path from AI/ML logic to a working web app. No context switching between backend and frontend languages. |
| **Streamlit** | Converts Python scripts directly into interactive web pages with no HTML or JavaScript required. Saved weeks of frontend scaffolding. Trade-off: re-runs the full script on every interaction, managed using `session_state` caching. |
| **Groq AI (Llama 3)** | Runs Llama 3 on custom LPU hardware. Response time is 200-400ms vs 2-4 seconds for GPT-4. For a fitness coach that needs to feel like a real conversation, that speed difference is very noticeable. Free tier supports the volume needed. |
| **Supabase** | Built on PostgreSQL — a real relational database with proper SQL, foreign keys, and structured schema. Firebase was considered but its document model does not suit structured fitness data with table relationships. |
| **SQLite fallback** | If Supabase is unreachable the app automatically switches to local SQLite. The app never crashes due to a network issue during a demo. |
| **HuggingFace Spaces** | Free deployment platform that supports Python/Streamlit natively. Gives a public URL that works on any device with zero server configuration. |
| **Brevo API** | Sends OTP emails and daily/weekly notifications via a REST API with one API key. Gmail SMTP was ruled out — unreliable in cloud deployments and requires OAuth setup. |

---

## Project Structure

```
fitplan-pro/
|
+-- app.py                      Entry point — login, signup, OTP reset
+-- auth_token.py               Session tokens, login state, logout
+-- nav_component.py            Responsive nav bar (desktop + mobile)
|
+-- utils/
|   +-- db.py                   All 60+ database functions in one file
|   +-- model_api.py            Groq API wrapper with retry logic
|   +-- prompt_builder.py       Prompt construction and BMI calculator
|   +-- streak_manager.py       Streak calculation and milestone detection
|   +-- achievements.py         18 badge definitions and unlock logic
|
+-- pages/
|   +-- 1_Profile.py            User profile setup and plan generation trigger
|   +-- 2_Dashboard.py          Command centre — overview of everything
|   +-- 3_Workout_Plan.py       Day-by-day workout with timer and swap
|   +-- 4_Diet_Plan.py          AI meals, water tracker, grocery list
|   +-- 5_ai_coach.py           Context-aware AI coaching chat
|   +-- 6_records.py            Personal records, measurements, 1RM calculator
|   +-- 7_progress_photos.py    Upload and compare transformation photos
|   +-- 9_history.py            Full workout log with consistency score
|   +-- 11_meal_planner.py      On-demand custom meal plan generator
|   +-- 12_sleep_tracker.py     Sleep hours and quality logging
|   +-- 13_cardio_tracker.py    Cardio sessions — run, cycle, swim etc
|   +-- 14_streaks.py           Streak counter and GitHub-style heatmap
|   +-- 15_progress_charts.py   Weight, sleep, cardio, measurements charts
|
+-- weekly_email.py             Sunday summary email sender
+-- daily_reminder.py           Daily workout reminder email
```

---

## Pages Explained in Detail

---

### 1 - Login - `app.py`

Three functions in one screen — no separate pages for signup vs login.

**What it does:**
- New users sign up with username and password. Password is hashed with SHA-256 before storing.
- Returning users log in. A session token is stored in Supabase so the session persists across browser refreshes.
- Forgot password sends a 6-digit OTP to the registered email via Brevo API. OTP expires after 10 minutes.

**Why SHA-256 and not bcrypt:**
SHA-256 is in Python's standard `hashlib` — no extra dependency. For a project running on HuggingFace's free tier where package control is limited, reliability matters more than the marginal security improvement of bcrypt.

---

### 2 - Profile - `1_Profile.py`

The foundation of the entire system. Everything the AI generates depends on what is entered here.

**Data collected:**

| Field | Why it matters |
|---|---|
| Age, weight, height | BMI calculation and calorie targets |
| Fitness goal | Determines rep ranges, rest periods, and the entire calorie structure |
| Days per week | Controls how many workout days are generated |
| Equipment available | Ensures exercises only use what the user actually has |
| Diet preference | Veg / non-veg / flexible — changes every meal, every day |
| Display name | Shown across all pages instead of the raw username or email |

**Key behaviour:** When the goal changes and the profile is saved, the existing active plan is deleted. This is intentional — a changed goal means the old plan is completely wrong for the new target. A confirmation dialog warns the user before this happens.

**New features:**
- **3-step onboarding banner** — guides first-time users through: fill profile, generate plan, start tracking. Dismissable and never shown again after dismissed.
- **Live BMI display** — calculated instantly on save, shown with the category label.

---

### 3 - Dashboard - `2_Dashboard.py`

The command centre. Designed to answer three questions the moment the app opens.

**Layout:**

```
+--------------------------------------------------------------+
| Streak | Done | Progress % | Total Days                      | <- stat cards
+--------------------------------------------------------------+
|       TODAY: DAY 3 - UPPER BODY PULL   | Not Done Yet        | <- hero bar
+--------------------+-------------------+-----------------+
| Today's Exercises  | This Week Chart   | Profile Card    |
| Mark Complete      | Weight Log        | Calendar        |
| Plan Progress Bar  | Done/Skip/Left    |                 |
| Motivational Quote |                   |                 |
+--------------------+-------------------+-----------------+
| Up Next (upcoming workout days)                           |
| Quick Access links  |  View Full Plan button              |
+-----------------------------------------------------------+
```

**Dynamic updates:** Marking a day complete updates the streak counter, the calendar cell, the stat cards, and the database — all in one rerun without navigating away.

**Missed day logging:** If past-due days are still pending, a section appears listing each with two buttons — mark done or skip — for retroactive logging.

**18 achievement badges:** Unlock automatically based on activity. When a new badge unlocks, a toast notification appears. Badge count and icons are shown in a compact banner below the stat cards.

---

### 4 - Workout Plan - `3_Workout_Plan.py`

The largest page at 1,400 lines. Shows the full AI-generated plan and handles all workout logging.

**Plan generation:**

```
User presses Generate Plan
    |
    v
Groq (Llama 3) receives structured prompt with:
    - Age, weight, height, goal
    - Days per week, equipment available
    - Diet preference, cuisine preference
    |
    v
Returns JSON with every day:
    - Exercise name, sets, reps, rest time, form tip
    - Meals for each day (breakfast, lunch, dinner, snacks)
    |
    v
Saved to Supabase active_plans table
Loaded into session_state.structured_days
```

**Persistent timer — how it actually works:**

Streamlit re-runs the entire Python script on every button press. A normal `time.sleep()` timer resets on every interaction. The solution: the timer start timestamp is stored in JavaScript's `sessionStorage` — in the browser, not on the server. On every render, JavaScript reads the stored start time and calculates elapsed time from the wall clock. Accurate to the millisecond, survives all Streamlit re-runs.

**Exercise swap:**

```
User clicks Swap on any exercise
    |
    v
App calls Groq with: exercise name + muscle group + user's equipment
    |
    v
Groq returns a replacement exercise for the same muscle
    |
    v
Updates session_state immediately
Writes change to database for persistence
```

**RPE logging:** Rate of Perceived Exertion slider (1-10) below each exercise. Saved per exercise per day. Helps track whether exercises are getting easier over time.

**Workout completion:** When all exercises for a day are checked, a confetti animation triggers, a streak toast notification appears, and completion is saved to two tables — `progress` (plan-linked) and `workout_history` (global, needed for streak calculation).

**Spotify music player:** 9 genre options, embedded player, no user login required. Genre choice is saved per user.

---

### 5 - Diet Plan - `4_Diet_Plan.py`

Shows the AI-generated meal plan per day with full switching, swapping, and automation.

**Diet type switching:** Changing Vegetarian to Non-Vegetarian triggers a full Groq regeneration with meals that are actually appropriate for that diet type — not just relabelling.

**AI meal swap:**

```
User presses Swap on any meal
    |
    v
Groq receives: meal name + diet type + cuisine preference + calorie target
    |
    v
Returns 2-3 alternatives matching the nutritional profile
    |
    v
User picks one. Saved to database immediately.
```

**Why meals and workouts use the same API call:**
Context. When the AI generates both together, it knows the training load for each day and can match calories accordingly — harder days get more carbohydrates, rest days get lower calories. Two separate calls would lose this context.

**Smart grocery list:** One button reads the next 7 days of meal data, sends it to Groq, and returns a categorised shopping list — Vegetables, Proteins, Grains, Dairy, Condiments.

---

### 6 - AI Coach - `5_ai_coach.py`

Not a generic chatbot. Every response is grounded in the user's actual data.

**Context injection before every message:**

```python
context_block = f"""
User: {username}
Current streak: {streak} days
This week: {done_this_week} / 7 workouts completed
Last workout: {last_workout_title}
7-day average sleep: {avg_sleep} hours
Diet adherence: {diet_pct}%
Recent personal records: {recent_prs}
"""
# Prepended to every message as a system prompt prefix
# The AI knows the user's real situation before it answers
```

The coach responds with "I see you only completed 3 of 7 workouts this week — what is getting in the way?" rather than generic advice.

**Chat history:** Last 30 messages stored in database and loaded on open. 30-message limit controls token costs while keeping enough context for coherent conversation.

---

### 7 - Records - `6_records.py`

Three sections: Personal Records, Body Measurements, and 1RM Calculator.

**1RM Calculator — Epley formula:**

```
1RM = weight_lifted x (1 + reps / 30)
```

User enters the weight lifted and the rep count. Estimated one-rep maximum appears instantly. No API call — pure Python math. Standard formula used by every serious strength tracking application.

**Illustrated empty states:** Instead of a blank page for new users, each section shows a clear description and a call-to-action button guiding the first entry. Added because early users did not understand what the page was for when it was empty.

---

### 8 - Progress Photos - `7_progress_photos.py`

Upload transformation photos with a label (Front, Side, Back, Custom) and compare any two side by side.

**Why base64 in the database instead of a file server:**
No separate object storage service needed — no S3 bucket, no CDN, no Supabase Storage bucket policies. Photos travel with the database and work out of the box. Trade-off: base64 is approximately 33% larger than binary. Acceptable at this scale. For a production system, object storage would be used.

---

### 9 - History - `9_history.py`

Chronological log of all completed workouts across all plans.

**Consistency score:**

```
Consistency % = completed_days / total_past_due_days x 100
```

Only counts days that have already passed — not future days. A user who missed one day but completed everything else gets a fair score based on what they actually had the opportunity to do.

**Save-on-load sync:** When History loads, it checks if completed workouts from the current session have been saved to `workout_history`. If any are missing, it saves them. This was the fix for the streak page showing incorrect counts for users who never visited History.

---

### 10 - AI Meal Planner - `11_meal_planner.py`

On-demand meal plan generator separate from the main Diet Plan page.

The Diet Plan page shows meals tied to the workout plan for the plan duration. The Meal Planner is for custom on-demand requests: "Give me a high-protein vegetarian plan under 1800 calories for today." Users specify exact macro targets in grams. The last 10 generated plans are saved and reloadable with one click.

---

### 11 - Sleep Tracker - `12_sleep_tracker.py`

Log hours slept and a quality score (1-5) for any day in the last 30 days.

**Dynamic update — the 5-step pattern:**

```
Step 1  save_sleep()               writes entry to database
Step 2  _load_sleep.clear()        invalidates the page cache
Step 3  get_sleep() to session_state    reloads fresh data
Step 4  st.cache_data.clear()      clears the Charts page cache too
Step 5  st.rerun()                 page refreshes with new data
```

The bar chart, stat cards, and history table all update immediately after saving.

---

### 12 - Cardio Tracker - `13_cardio_tracker.py`

12 activity types: Running, Cycling, Swimming, HIIT, Walking, Rowing, Jump Rope, Boxing, Yoga, Elliptical, Stair Climber, Custom.

Cardio is tracked separately from the workout plan because they serve different purposes — the plan covers structured strength training, cardio covers supplemental sessions. Users can track cardio regardless of whether they have an active plan.

Each activity has automatic calorie estimation using standard MET values. Users can override with their actual device reading.

---

### 13 - Streaks and Heatmap - `14_streaks.py`

Current streak, longest streak, 12-week activity heatmap, and milestone badges.

**Streak calculation:**

```python
workout_dates = all dates from workout_history table

count = 0
check_date = today
while check_date in workout_dates:
    count += 1
    check_date = check_date - one day
```

**Session state merge:** If the user marked today as done earlier in the same session, `session_state.tracking` is merged into `workout_dates` before calculation. The streak is accurate immediately without waiting for the 60-second cache.

**18 milestone badges:**

| Days | Badge | Name |
|---|---|---|
| 7 | Bronze | Week Warrior |
| 14 | Lightning | Fortnight |
| 21 | Fire | 3-Week Fire |
| 30 | Silver | Month Beast |
| 60 | Diamond | Diamond |
| 90 | Gold | Legend |
| 180 | Crown | Elite |

---

### 14 - Progress Charts - `15_progress_charts.py`

Four tabs: Weight trend, Sleep history, Cardio calories, Body measurements.

All four data loaders use `@st.cache_data(ttl=60)`. Sleep and Cardio pages call `st.cache_data.clear()` after every save so new data appears in Charts within seconds.

**Weight chart — goal-aware colouring:** A downward trend is green for fat loss goal but red for muscle gain goal. An upward trend is green for muscle gain but red for fat loss. Same data, different interpretation based on the user's target.

---

### 15 - Navigation - `nav_component.py`

One file controls navigation for all 15 pages. Called with a single line on every page:

```python
from nav_component import render_nav
render_nav("dashboard", uname)
```

**Desktop (wider than 900px):**
All 12 page icons are always visible in a persistent top bar. Active page is highlighted. User chip and Sign Out on the right. No click needed to see all pages.

**Mobile and tablet (900px or narrower):**
Logo, current page pill, and hamburger button. Hamburger animates to X when open. Drawer slides down with 4-column grid on tablet or 3-column on phone.

**How the hidden button trick works:**
Streamlit requires real `st.button()` elements for `st.switch_page()` to work. Rendering 12 visible buttons would break the layout. The solution: buttons are rendered but pushed off-screen with CSS (`left: -9999px`). The visible nav icons call `document.getElementById('fpbtn_X').click()` via JavaScript to trigger them. Three hide layers fire at 80ms, 400ms, and 1200ms to catch buttons exposed by late Streamlit re-renders.

---

## Database Design

14 tables, all keyed on username:

```sql
users                  username, password_hash, email, created_at
user_profiles          username, age, weight, height, goal, equipment, diet_type, display_name
active_plans           plan_id, username, days[], dietary_type, created_at
progress               username, plan_id, day_number, workout_checks, dietary_checks
workout_history        username, date, day, muscle_group, exercises, status
streaks                username, current_streak, longest_streak, last_completed_date
sleep_logs             username, date, hours, quality, notes
cardio_logs            username, date, activity, duration, distance, calories
weight_logs            username, date, weight_kg
personal_records       username, exercise, weight, reps, date
body_measurements      username, date, chest, waist, hips, arms, thighs
progress_photos        username, date, label, image_base64
chat_history           username, messages_json, updated_at
water_intake           username, date, glasses
```

**Why `progress` and `workout_history` are two separate tables:**

`progress` is tied to a specific `plan_id`. Generating a new plan archives old progress under the old plan ID. `workout_history` is plan-independent — it records every workout ever completed across all plans. The Streak page needs all historical workout dates regardless of which plan they belonged to. These are two different questions that require two different data sources.

---

## Data Flow

```
User marks a workout as complete
          |
          v
   save_progress()  ─────────────────────────── progress table (plan-linked)
   save_workout_history()  ────────────────────  workout_history table (global)
   update_streak()  ───────────────────────────  streaks table
          |
          v
   session_state.tracking updated in memory
          |
          v
   st.rerun() triggered
          |
     +----+------------------------------------------+
     v                                               v
Dashboard re-reads session_state          Streak page merges session_state
Stat cards update instantly               Streak number accurate immediately
          |
          v
Charts page cache cleared via st.cache_data.clear()
New data visible in Charts within 60 seconds
```

---

## All New Features

| Feature | Page | What it does |
|---|---|---|
| OTP password reset | Login | 6-digit code via Brevo email, expires in 10 minutes |
| Onboarding banner | Profile | 3-step guide for first-time users, dismissable |
| Live BMI display | Profile | Calculated on save with category label |
| Persistent workout timer | Workout | JavaScript sessionStorage survives all Streamlit re-runs |
| Exercise swap with AI | Workout | Groq replaces any exercise with an equipment-appropriate alternative |
| RPE logging | Workout | Effort score per exercise, saved to database |
| Spotify music player | Workout | 9 genres, embedded player, no user login needed |
| Workout completion celebration | Workout | Confetti animation and streak toast on day complete |
| AI meal swap | Diet | Replace any meal with AI-suggested alternatives |
| Smart grocery list | Diet | Auto-generated and categorised from next 7 days of meals |
| Supplement guide | Diet | Goal-specific content, instant, no API call |
| Water tracker | Diet and Workout | 8-glass daily goal, resets at midnight |
| Context-aware AI coach | Coach | Real user data injected into every message |
| 1RM calculator | Records | Epley formula, instant result, no API call |
| Illustrated empty states | Records, History, Photos | Guides new users with no data yet |
| Progress photo comparison | Photos | Side-by-side comparison of any two uploaded photos |
| Activity heatmap | Streaks | 12-week GitHub-style workout frequency grid |
| 18 achievement badges | Streaks and Dashboard | Auto-unlock with toast notification |
| Session state streak merge | Streaks | Streak accurate immediately without cache wait |
| Responsive navigation | All pages | Desktop persistent bar, mobile hamburger drawer |
| Daily reminder email | Automation | Only fires if today's workout is still pending |
| Weekly progress email | Automation | Sunday summary with real data for that week |
| Consistency score | History | Based on past-due days only — fair measurement |
| Save-on-load history sync | History | Fixes streak gap for users who skip History page |

---

## Setup and Deployment

### Local development

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/fitplan-pro.git
cd fitplan-pro

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate        # Linux or Mac
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add environment variables
cp .env.example .env
# Edit .env with your API keys

# 5. Run the app
streamlit run app.py
```

### HuggingFace Spaces deployment

```
1. Create a new Space on HuggingFace
2. Select SDK: Streamlit
3. Upload all files keeping the same folder structure
4. Add all environment variables in Settings > Repository Secrets
5. The app deploys automatically on every push to main
```

---

## Environment Variables

```env
# Groq API — AI plan generation and coaching
GROQ_API_KEY=your_groq_api_key_here

# Supabase — primary cloud database
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key

# Brevo — email notifications and OTP reset
BREVO_API_KEY=your_brevo_api_key
BREVO_SENDER_EMAIL=noreply@yourapp.com
```

If `SUPABASE_URL` and `SUPABASE_KEY` are not set, the app automatically falls back to SQLite. All core features work. Email features require Brevo keys.

---

## Known Limitations

| Limitation | Impact | Fix for production |
|---|---|---|
| No automated tests | All testing was manual | Add pytest for db.py and streak_manager.py |
| Base64 photo storage | Not scalable past a few hundred photos per user | Move to Supabase Storage or Amazon S3 |
| Single server on HuggingFace | No horizontal scaling | Containerised deployment with load balancing |
| Measurements tab has no save button | Users must go to Records page to log measurements | Add save form directly to Charts measurements tab |
| 60-second streak cache | Other sessions see old streak for up to 60s | Reduce TTL or use websocket update |

---

## Page Reference

| Page | File | Lines | Key feature |
|---|---|---|---|
| Login | `app.py` | 896 | OTP reset, SHA-256 auth, Brevo email |
| Profile | `1_Profile.py` | 791 | BMI calculator, onboarding, plan reset on change |
| Dashboard | `2_Dashboard.py` | 657 | Live calendar, missed day logging, 18 achievements |
| Workout Plan | `3_Workout_Plan.py` | 1,410 | JS timer, exercise swap, RPE, Spotify |
| Diet Plan | `4_Diet_Plan.py` | 829 | AI meal swap, grocery list, water tracker |
| AI Coach | `5_ai_coach.py` | 483 | Context injection, 30-message history cap |
| Records | `6_records.py` | 525 | Epley 1RM, illustrated empty states |
| Progress Photos | `7_progress_photos.py` | 412 | Base64 storage, side-by-side comparison |
| History | `9_history.py` | 322 | Consistency score, save-on-load sync |
| Meal Planner | `11_meal_planner.py` | 751 | Custom macro targets, saved plan history |
| Sleep Tracker | `12_sleep_tracker.py` | 419 | 5-step dynamic update pattern |
| Cardio Tracker | `13_cardio_tracker.py` | 464 | 12 activity types, calorie estimation, delete |
| Streaks | `14_streaks.py` | 378 | Heatmap, 18 milestones, session_state merge |
| Progress Charts | `15_progress_charts.py` | 435 | 4-tab charts, cross-page cache clearing |
| Navigation | `nav_component.py` | 417 | Responsive nav, hidden button JS technique |

---

<p align="center">
  <strong>FitPlan Pro</strong> — built with Python, Streamlit, Supabase, and Groq AI
  <br/>
  <img src="https://img.shields.io/badge/Deployed_on-HuggingFace_Spaces-FFD21E?style=flat-square&logo=huggingface&logoColor=black" alt="deployed"/>
  <img src="https://img.shields.io/badge/Status-Live-brightgreen?style=flat-square" alt="status"/></p>
