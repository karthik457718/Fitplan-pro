"""
model_api.py — Fast AI plan generation for FitPlan Pro.
Single API call — no chunking. Instant generation, no broken flow.
"""

import os, time, json, re


# ══════════════════════════════════════════════════════════════════════════════
# Groq API call
# ══════════════════════════════════════════════════════════════════════════════

def query_model(prompt, max_tokens=8000, model="llama-3.1-8b-instant"):
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY not set.\n"
            "1. Go to https://console.groq.com\n"
            "2. Create API Key (gsk_...)\n"
            "3. HuggingFace > Settings > Secrets > GROQ_API_KEY"
        )
    try:
        from groq import Groq
        client = Groq(api_key=GROQ_API_KEY)
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": (
                    "You are a certified personal trainer and nutritionist. "
                    "Output ONLY valid JSON arrays. No text before or after. "
                    "Be specific with exercise names, quantities, and food items."
                )},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7,
        )
        return resp.choices[0].message.content
    except Exception as e:
        err = str(e)
        if "401" in err or "invalid_api_key" in err.lower():
            raise ValueError("Invalid Groq API key. Check https://console.groq.com/keys") from None
        if "429" in err or "rate_limit" in err.lower():
            raise ValueError("Rate limit hit. Wait 30s and retry.") from None
        if "model_not_found" in err.lower() or "model" in err.lower():
            raise ValueError(f"Model error: {err}") from None
        raise


# ══════════════════════════════════════════════════════════════════════════════
# JSON repair
# ══════════════════════════════════════════════════════════════════════════════

def _repair_json(text):
    if not text:
        return None
    text = re.sub(r"```(?:json)?\s*", "", text)
    text = re.sub(r"```", "", text).strip()
    try:
        return json.loads(text)
    except Exception:
        pass
    m = re.search(r"(\[.*\])", text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1))
        except Exception:
            text = m.group(1)
    stack, in_str, escape, result = [], False, False, []
    for ch in text:
        if escape:
            escape = False; result.append(ch); continue
        if ch == "\\" and in_str:
            escape = True; result.append(ch); continue
        if ch == '"' and not escape:
            in_str = not in_str; result.append(ch); continue
        if in_str:
            result.append(ch); continue
        if ch in "{[":
            stack.append(ch); result.append(ch)
        elif ch in "}]":
            if stack: stack.pop()
            result.append(ch)
        else:
            result.append(ch)
    if in_str: result.append('"')
    joined = "".join(result).rstrip().rstrip(",")
    for opener in reversed(stack):
        joined += "}" if opener == "{" else "]"
    try:
        return json.loads(joined)
    except Exception:
        return None


# ══════════════════════════════════════════════════════════════════════════════
# Defaults
# ══════════════════════════════════════════════════════════════════════════════

_PRE_VIDEOS = [
    "https://www.youtube.com/embed/HDiHMHBpHBQ",
    "https://www.youtube.com/embed/nHHiMrYHmmE",
    "https://www.youtube.com/embed/R0mMyV5OtcM",
]
_POST_VIDEOS = [
    "https://www.youtube.com/embed/R56k41NLIoI",
    "https://www.youtube.com/embed/R56k41NLIoI",
    "https://www.youtube.com/embed/R56k41NLIoI",
]

def _default_dietary(dtype):
    if dtype == "veg":
        return {
            "breakfast": "Oats with banana, chia seeds and honey (1 cup oats)",
            "lunch":     "Brown rice (1 cup) with mixed dal and seasonal vegetables",
            "dinner":    "Paneer curry (100g) with 2 multigrain rotis and salad",
            "snacks":    "Handful mixed nuts, 1 fruit and green tea"
        }
    return {
        "breakfast": "3 boiled eggs with 2 whole wheat toast and black coffee",
        "lunch":     "Grilled chicken breast (150g) with brown rice and salad",
        "dinner":    "Baked fish (150g) with steamed broccoli and sweet potato",
        "snacks":    "Boiled eggs (2) and 20 almonds"
    }

def _default_pre(day_num):
    v = _PRE_VIDEOS[day_num % len(_PRE_VIDEOS)]
    return [
        {"name": "Arm Circles",   "duration": "30s", "video_url": v},
        {"name": "Leg Swings",    "duration": "30s", "video_url": v},
        {"name": "Hip Circles",   "duration": "30s", "video_url": v},
        {"name": "Jumping Jacks", "duration": "30s", "video_url": v},
    ]

def _default_post(day_num):
    v = _POST_VIDEOS[day_num % len(_POST_VIDEOS)]
    return [
        {"name": "Quad Stretch",      "duration": "40s", "video_url": v},
        {"name": "Hamstring Stretch", "duration": "40s", "video_url": v},
        {"name": "Child's Pose",      "duration": "45s", "video_url": v},
        {"name": "Chest Stretch",     "duration": "30s", "video_url": v},
    ]

_FALLBACK_WORKOUTS = [
    [{"name":"Push-ups","sets":3,"reps":"12","rest":"60s","timer":60,"notes":"Elbows at 45 deg"},
     {"name":"Tricep Dips","sets":3,"reps":"10","rest":"60s","timer":60,"notes":"Elbows close"},
     {"name":"Shoulder Taps","sets":3,"reps":"20","rest":"45s","timer":45,"notes":"Hips stable"},
     {"name":"Pike Push-ups","sets":3,"reps":"8","rest":"60s","timer":60,"notes":"Hips high"},
     {"name":"Plank","sets":3,"reps":"30s","rest":"45s","timer":30,"notes":"Straight line"}],
    [{"name":"Squats","sets":4,"reps":"15","rest":"60s","timer":60,"notes":"Knees over toes"},
     {"name":"Reverse Lunges","sets":3,"reps":"12","rest":"60s","timer":60,"notes":"90 degree knee"},
     {"name":"Glute Bridges","sets":3,"reps":"20","rest":"45s","timer":45,"notes":"Squeeze at top"},
     {"name":"Jump Squats","sets":3,"reps":"12","rest":"75s","timer":60,"notes":"Soft landing"},
     {"name":"Calf Raises","sets":3,"reps":"25","rest":"30s","timer":30,"notes":"Full ROM"}],
    [{"name":"Burpees","sets":3,"reps":"10","rest":"75s","timer":75,"notes":"Controlled drop"},
     {"name":"High Knees","sets":3,"reps":"30s","rest":"45s","timer":30,"notes":"Drive knees high"},
     {"name":"Mountain Climbers","sets":3,"reps":"30","rest":"45s","timer":45,"notes":"Fast alt"},
     {"name":"Box Jumps","sets":3,"reps":"8","rest":"75s","timer":60,"notes":"Soft landing"},
     {"name":"Jumping Jacks","sets":3,"reps":"40","rest":"30s","timer":30,"notes":"Full ext"}],
    [{"name":"Bicycle Crunches","sets":3,"reps":"20","rest":"45s","timer":45,"notes":"Exhale twist"},
     {"name":"Leg Raises","sets":3,"reps":"15","rest":"45s","timer":45,"notes":"Lower back flat"},
     {"name":"Russian Twists","sets":3,"reps":"20","rest":"45s","timer":45,"notes":"Feet off floor"},
     {"name":"Plank","sets":3,"reps":"45s","rest":"45s","timer":45,"notes":"Hollow body"},
     {"name":"Dead Bug","sets":3,"reps":"12","rest":"30s","timer":30,"notes":"Slow extend"}],
]
_MUSCLE_GROUPS = [
    "Upper Body Push", "Lower Body", "Upper Body Pull",
    "Core & Cardio", "Full Body Compound", "Shoulders & Arms",
    "Lower Body Posterior",
]

def _fallback_day(dn, dtype):
    is_rest = (dn % 7 == 0)
    return {
        "day":          dn,
        "is_rest_day":  is_rest,
        "muscle_group": "Rest & Recovery" if is_rest else _MUSCLE_GROUPS[(dn-1) % len(_MUSCLE_GROUPS)],
        "workout":      [] if is_rest else _FALLBACK_WORKOUTS[(dn-1) % len(_FALLBACK_WORKOUTS)],
        "dietary":      _default_dietary(dtype),
        "pre_stretch":  _default_pre(dn),
        "post_stretch": _default_post(dn),
    }


# ══════════════════════════════════════════════════════════════════════════════
# Validation
# ══════════════════════════════════════════════════════════════════════════════

def _validate_day(day, dn, dtype):
    day["day"] = dn
    day.setdefault("is_rest_day",  False)
    day.setdefault("muscle_group", _MUSCLE_GROUPS[(dn-1) % len(_MUSCLE_GROUPS)])
    if not isinstance(day.get("workout"), list):
        day["workout"] = []
    for ex in day["workout"]:
        if not isinstance(ex, dict): continue
        ex.setdefault("name",  "Exercise")
        ex.setdefault("sets",  3)
        ex.setdefault("reps",  "12")
        ex.setdefault("rest",  "60s")
        ex.setdefault("notes", "Maintain form")
        try:
            ex["timer"] = int(str(ex.get("timer", ex.get("rest", "60").replace("s", ""))).replace("s", ""))
        except Exception:
            ex["timer"] = 60
    if not isinstance(day.get("dietary"), dict) or not any(day.get("dietary", {}).values()):
        day["dietary"] = _default_dietary(dtype)
    for m in ["breakfast", "lunch", "dinner", "snacks"]:
        day["dietary"].setdefault(m, "Balanced nutritious meal")
    if not isinstance(day.get("pre_stretch"), list) or not day.get("pre_stretch"):
        day["pre_stretch"] = _default_pre(dn)
    if not isinstance(day.get("post_stretch"), list) or not day.get("post_stretch"):
        day["post_stretch"] = _default_post(dn)
    for s in day.get("pre_stretch", []):
        s.setdefault("video_url", _PRE_VIDEOS[dn % len(_PRE_VIDEOS)])
    for s in day.get("post_stretch", []):
        s.setdefault("video_url", _POST_VIDEOS[dn % len(_POST_VIDEOS)])
    return day


def _to_text(days):
    lines = []
    for d in days:
        dn = d.get("day", 1)
        mg = d.get("muscle_group", "Full Body")
        if d.get("is_rest_day"):
            lines.append(f"## Day {dn} - Rest Day\n\nRest and recover.\n")
            continue
        lines.append(f"## Day {dn} - {mg}")
        for ex in d.get("workout", []):
            lines.append(f"- {ex.get('name')} - {ex.get('sets')}x{ex.get('reps')} (rest {ex.get('rest')})")
        diet = d.get("dietary", {})
        for meal in ["breakfast", "lunch", "dinner", "snacks"]:
            if diet.get(meal):
                lines.append(f"  {meal.title()}: {diet[meal]}")
        lines.append("")
    return "\n".join(lines)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN — Single fast API call, no chunking
# ══════════════════════════════════════════════════════════════════════════════

def query_model_chunked(name, gender, height, weight, goal, fitness_level,
                        equipment, days_per_week=5, months=1,
                        dietary_type="veg", progress_callback=None,
                        injuries=None,
                        cuisine_preference="", cuisine_label="",
                        cuisine_icon="", cuisine_notes=""):
    """
    Generate complete workout + diet plan in ONE fast API call.
    No chunking — instant single response, clean flow.
    Returns: (full_plan_text, structured_days_list, bmi, bmi_cat)
    """
    if injuries is None:
        injuries = []

    from prompt_builder import calculate_bmi, bmi_category, build_injury_block, build_diet_block

    bmi        = calculate_bmi(weight, height)
    bmi_cat    = bmi_category(bmi)
    total_days = days_per_week * 4 * months

    eq_str     = ", ".join(equipment) if equipment else "Bodyweight only"
    diet_label = "Vegetarian" if dietary_type == "veg" else "Non-Vegetarian"
    diet_rule  = "NO meat/fish/eggs" if dietary_type == "veg" else "Include chicken/fish/eggs"

    # Build injury + allergy one-liners for the prompt
    injury_oneliner = ""
    if injuries:
        from prompt_builder import INJURY_RESTRICTIONS
        forbidden_all = []
        for inj in injuries:
            r = INJURY_RESTRICTIONS.get(inj.lower(), {})
            forbidden_all.extend(r.get("avoid", []))
        if forbidden_all:
            injury_oneliner = (
                f"\nINJURY RULES — Client has {', '.join(injuries)} injuries. "
                f"NEVER include: {', '.join(sorted(set(forbidden_all)))}. "
                f"Mark safe alternatives with (injury-safe)."
            )

    allergy_oneliner = ""
    if cuisine_notes and cuisine_notes.strip():
        allergy_oneliner = (
            f"\nALLERGY — Zero tolerance: '{cuisine_notes.strip()}'. "
            f"Never include flagged ingredients in any meal."
        )

    cuisine_oneliner = ""
    if cuisine_label:
        cuisine_oneliner = f"\nCUISINE: All meals must follow {cuisine_icon} {cuisine_label} style."

    # Which days are rest days
    rest_days = set()
    for week in range(months * 4 + 1):
        for offset in range(days_per_week + 1, 8):
            d = week * 7 + offset
            if 1 <= d <= total_days:
                rest_days.add(d)

    muscles = [
        "Upper Body Push", "Lower Body", "Upper Body Pull",
        "Core & Cardio", "Full Body Compound", "Shoulders & Arms",
        "Lower Body Posterior",
    ]

    intensity = {
        "Beginner":     "2-3 sets, 90s rest, basic moves only",
        "Intermediate": "3-4 sets, 60s rest, progressive overload",
        "Advanced":     "4-5 sets, 45s rest, supersets allowed",
    }.get(fitness_level, "3 sets, 60s rest")

    goal_tip = {
        "Weight Loss":     "high reps 15-20, short rest, cardio circuits",
        "Build Muscle":    "moderate reps 8-12, compound lifts, protein surplus",
        "General Fitness": "balanced 10-15 reps, mix strength and cardio",
    }.get(goal, "balanced training")

    # Build day specs list
    day_specs = []
    for d in range(1, total_days + 1):
        if d in rest_days:
            day_specs.append(f"{d}:REST")
        else:
            day_specs.append(f"{d}:{muscles[(d-1) % len(muscles)]}")

    if progress_callback:
        progress_callback(1, 1, 0, total_days,
                          status=f"Generating your {total_days}-day plan...")

    # ── Single prompt ─────────────────────────────────────────────────────────
    prompt = f"""Generate a {total_days}-day personalised fitness plan as a JSON array.

User: {name},{gender},{height}cm,{weight}kg,BMI:{bmi:.1f}({bmi_cat}),Goal:{goal}({goal_tip}),Level:{fitness_level}({intensity}),Equipment:{eq_str},Diet:{diet_label}({diet_rule})

Days: {", ".join(day_specs)}
REST days: is_rest_day=true, empty workout array but include dietary plan.{injury_oneliner}{allergy_oneliner}{cuisine_oneliner}

Return a JSON array of exactly {total_days} objects. Each object:
{{"day":N,"is_rest_day":false,"muscle_group":"...","workout":[{{"name":"ExerciseName","sets":3,"reps":"12","rest":"60s","timer":60,"notes":"form tip"}},...5 exercises],"dietary":{{"breakfast":"food+qty","lunch":"food+qty","dinner":"food+qty","snacks":"food"}},"pre_stretch":[{{"name":"stretch","duration":"30s","video_url":"https://www.youtube.com/embed/R0mMyV5OtcM"}}],"post_stretch":[{{"name":"stretch","duration":"40s","video_url":"https://www.youtube.com/embed/R56k41NLIoI"}}]}}

Rules:
- Use ONLY equipment: {eq_str}
- {diet_rule} — specific food names and quantities
- Vary exercises every day, no repeats
- Adjust sets/reps/rest for {fitness_level} level
- Output ONLY the JSON array, nothing else"""

    # ── Try fast model first, fallback to powerful model ──────────────────────
    parsed = None
    models_to_try = [
        ("llama-3.1-8b-instant",    8000),
        ("llama-3.3-70b-versatile", 8000),
    ]

    for model_name, max_tok in models_to_try:
        for attempt in range(2):
            try:
                if progress_callback:
                    progress_callback(1, 1, 0, total_days,
                                      status=f"AI is generating your plan...")
                raw    = query_model(prompt, max_tokens=max_tok, model=model_name)
                parsed = _repair_json(raw)
                if parsed and isinstance(parsed, list) and len(parsed) > 0:
                    break
                if attempt == 0:
                    time.sleep(1)
            except ValueError as e:
                if "rate_limit" in str(e).lower():
                    if progress_callback:
                        progress_callback(1, 1, 0, total_days,
                                          status="Rate limit — waiting 30s...")
                    time.sleep(30)
                if attempt == 0:
                    time.sleep(2)
                    continue
                break
            except Exception:
                if attempt == 0:
                    time.sleep(2)
                    continue
                break
        if parsed and isinstance(parsed, list) and len(parsed) > 0:
            break

    # ── Build final structured days ───────────────────────────────────────────
    parsed_map = {}
    if parsed:
        for p in parsed:
            if isinstance(p, dict) and p.get("day"):
                parsed_map[int(p["day"])] = p

    all_days = []
    for dn in range(1, total_days + 1):
        raw_day = (
            parsed_map.get(dn) or
            (parsed[dn - 1] if parsed and (dn - 1) < len(parsed) else None) or
            _fallback_day(dn, dietary_type)
        )
        if not isinstance(raw_day, dict):
            raw_day = _fallback_day(dn, dietary_type)
        if dn in rest_days:
            raw_day["is_rest_day"]  = True
            raw_day["workout"]      = []
            raw_day["muscle_group"] = "Rest & Recovery"
        all_days.append(_validate_day(raw_day, dn, dietary_type))

    if progress_callback:
        progress_callback(1, 1, total_days, total_days, status="✅ Plan Ready!")

    return _to_text(all_days), all_days, bmi, bmi_cat