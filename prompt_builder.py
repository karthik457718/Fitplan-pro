def calculate_bmi(weight, height):
    h = height / 100
    return weight / (h * h)

def bmi_category(bmi):
    if bmi < 18.5:  return "Underweight"
    elif bmi < 25:  return "Normal Weight"
    elif bmi < 30:  return "Overweight"
    else:           return "Obese"

def bmi_advice(category):
    return {
        "Underweight":   "focus on caloric surplus, compound lifts, and muscle building. Avoid excessive cardio.",
        "Normal Weight": "maintain current weight while building lean muscle and improving cardiovascular fitness.",
        "Overweight":    "incorporate cardio-strength circuits to burn fat while preserving muscle mass.",
        "Obese":         "prioritise low-impact cardio, mobility work, and progressive resistance training.",
    }.get(category, "train consistently and progressively.")


# ── Injury → forbidden movements mapping ──────────────────────────────────────
# For each injury, defines exercises/movements to AVOID and safe alternatives
INJURY_RESTRICTIONS = {
    "knee": {
        "avoid": [
            "squats", "lunges", "leg press", "jump", "plyometric",
            "running", "step-ups", "leg extension", "deep knee bend"
        ],
        "replace_with": [
            "seated leg curl", "hip thrust", "glute bridge", "upper body focus",
            "swimming", "seated calf raise", "lying leg curl"
        ],
        "note": "Avoid all deep knee flexion and high-impact lower body movements. "
                "Focus on hamstrings, glutes, and upper body. No jumping or running."
    },
    "shoulder": {
        "avoid": [
            "overhead press", "military press", "shoulder press", "lateral raise",
            "upright row", "behind neck press", "dips", "push press",
            "handstand", "overhead squat"
        ],
        "replace_with": [
            "face pull", "external rotation", "low cable row", "chest-supported row",
            "front raise (light)", "reverse fly", "lower body focus"
        ],
        "note": "Avoid all overhead pressing and upright rows. "
                "Focus on lower body, core, and horizontal pulling movements."
    },
    "back": {
        "avoid": [
            "deadlift", "barbell row", "good morning", "back squat",
            "hyperextension", "heavy carry", "jefferson curl", "stiff-leg deadlift"
        ],
        "replace_with": [
            "lat pulldown", "seated cable row", "leg press", "goblet squat",
            "plank", "bird dog", "cat-cow", "pallof press"
        ],
        "note": "Avoid all heavy spinal loading. Use braced core on every movement. "
                "Prefer machines over free weights for lower body."
    },
    "wrist": {
        "avoid": [
            "push-up", "barbell curl", "front rack", "handstand",
            "wrist curl", "clean", "snatch", "dumbbell press (grip-heavy)"
        ],
        "replace_with": [
            "cable curl", "hammer curl with neutral grip", "machine press",
            "tricep pushdown", "leg press", "lower body focus"
        ],
        "note": "Avoid any exercise that loads the wrist in extension or flexion. "
                "Use neutral grip or machine alternatives throughout."
    },
    "ankle": {
        "avoid": [
            "jump", "box jump", "running", "sprint", "calf raise",
            "agility drill", "lunge (walking)", "step-up"
        ],
        "replace_with": [
            "seated leg curl", "leg press", "hip thrust", "glute bridge",
            "upper body focus", "seated calf raise (light)"
        ],
        "note": "Avoid all weight-bearing dynamic lower body movements. "
                "Focus on seated and supine lower body exercises and upper body."
    },
    "elbow": {
        "avoid": [
            "tricep dip", "skull crusher", "close-grip bench", "preacher curl",
            "pull-up (if painful)", "push-up (if painful)", "barbell curl"
        ],
        "replace_with": [
            "cable tricep pushdown", "cable curl", "neutral grip row",
            "machine press", "leg press", "lower body focus"
        ],
        "note": "Avoid full elbow extension under load and deep elbow flexion. "
                "Use cables over free weights to reduce joint stress."
    },
    "hip": {
        "avoid": [
            "deep squat", "leg press (full range)", "hip flexor stretch",
            "lunge", "step-up", "running", "sprint", "jump"
        ],
        "replace_with": [
            "glute bridge", "clamshell", "side-lying abduction",
            "upper body focus", "seated leg curl", "light walking"
        ],
        "note": "Avoid deep hip flexion and high-impact movements. "
                "Focus on gentle hip strengthening and upper body work."
    },
    "neck": {
        "avoid": [
            "neck extension", "shrug", "overhead press", "behind-neck press",
            "upright row", "any exercise causing neck strain"
        ],
        "replace_with": [
            "face pull", "chest-supported row", "lower body focus",
            "plank", "dead bug", "pallof press"
        ],
        "note": "Avoid all cervical loading and overhead work. "
                "Keep head neutral on every exercise. No shrugs or overhead pressing."
    },
    "hamstring": {
        "avoid": [
            "deadlift", "stiff-leg deadlift", "leg curl (full range, high load)",
            "sprint", "running", "jump", "good morning"
        ],
        "replace_with": [
            "leg press", "goblet squat", "hip thrust", "glute bridge",
            "upper body focus", "light walking"
        ],
        "note": "Avoid high hamstring tension under load. "
                "Focus on quad-dominant lower body movements and upper body."
    },
    "calf": {
        "avoid": [
            "calf raise (heavy)", "jump", "box jump", "sprint",
            "running", "agility drill"
        ],
        "replace_with": [
            "leg press", "hip thrust", "upper body focus",
            "seated calf raise (very light)", "swimming"
        ],
        "note": "Avoid all explosive and heavy plantarflexion. "
                "Focus on upper body and non-impact lower body movements."
    },
    "rotator cuff": {
        "avoid": [
            "overhead press", "lateral raise (heavy)", "internal rotation under load",
            "behind-neck pull-down", "upright row", "dip", "bench press (wide grip)"
        ],
        "replace_with": [
            "external rotation (band/cable)", "face pull", "chest-supported row",
            "neutral grip row", "lower body focus", "light front raise"
        ],
        "note": "Avoid overhead and impingement-risk positions. "
                "Strengthen rotator cuff with low-load external rotation drills. "
                "No heavy pressing until cleared."
    },
    "achilles": {
        "avoid": [
            "calf raise", "jump", "box jump", "sprint", "running",
            "agility drill", "walking lunge", "step-up"
        ],
        "replace_with": [
            "seated leg curl", "leg press", "hip thrust",
            "upper body focus", "light cycling (seated)"
        ],
        "note": "Avoid all Achilles loading. Strictly no jumping, running, or calf work. "
                "Focus on seated/supine lower body and upper body movements."
    },
}


def build_injury_block(injuries):
    """
    Build the injury restriction block for the AI prompt.
    Returns empty string if no injuries.
    """
    if not injuries:
        return ""

    lines = ["━━━ INJURY & LIMITATION RESTRICTIONS ━━━"]
    lines.append(
        f"⚠️  The client has the following injuries/limitations: "
        f"{', '.join(i.upper() for i in injuries)}"
    )
    lines.append(
        "You MUST apply ALL of the rules below. This is non-negotiable for client safety.\n"
    )

    all_avoid = []
    all_replace = []

    for injury in injuries:
        key = injury.lower().strip()
        if key in INJURY_RESTRICTIONS:
            r = INJURY_RESTRICTIONS[key]
            lines.append(f"• {injury.upper()} injury:")
            lines.append(f"  - NEVER include: {', '.join(r['avoid'])}")
            lines.append(f"  - Safe alternatives: {', '.join(r['replace_with'])}")
            lines.append(f"  - Rule: {r['note']}")
            all_avoid.extend(r["avoid"])
            all_replace.extend(r["replace_with"])

    lines.append(
        f"\n⛔ GLOBAL FORBIDDEN EXERCISES (across ALL {len(injuries)} injuries): "
        + ", ".join(sorted(set(all_avoid)))
    )
    lines.append(
        "✅ Preferred safe alternatives pool: "
        + ", ".join(sorted(set(all_replace)))
    )
    lines.append(
        "\n🔒 INJURY COMPLIANCE RULES:"
        "\n  1. Scan every exercise in your plan against the forbidden list above before including it."
        "\n  2. If an exercise even partially loads the injured area, replace it."
        "\n  3. Never suggest the user 'try' or 'attempt' a forbidden movement."
        "\n  4. For warm-up and cool-down, also avoid stretches that stress the injured area."
        "\n  5. Label injury-adapted exercises with '(injury-safe)' so the user knows."
    )

    return "\n".join(lines)


def build_diet_block(diet_type, cuisine_preference, cuisine_label,
                     cuisine_icon, cuisine_notes):
    """
    Build the diet/cuisine/allergy block for the AI prompt.
    """
    diet_display = "Vegetarian (no meat, no fish, no eggs)" if diet_type == "veg" \
                   else "Non-Vegetarian (chicken, egg, and fish only — NO red meat, NO pork)"

    cuisine_str = f"{cuisine_icon} {cuisine_label}" if cuisine_label else "Standard"

    lines = [
        "━━━ DIET & MEAL PLAN REQUIREMENTS ━━━",
        f"Diet Type       : {diet_display}",
        f"Cuisine Style   : {cuisine_str}",
    ]

    if cuisine_notes and cuisine_notes.strip():
        lines.append(f"Allergies/Notes : {cuisine_notes.strip()}")
        lines.append(
            "\n⚠️  ALLERGY & PREFERENCE RULES (STRICT):"
            "\n  1. Read the Allergies/Notes above carefully."
            "\n  2. NEVER include any ingredient the user has flagged as an allergy or exclusion."
            "\n  3. If the user says 'no eggs' — zero egg-containing meals across all days."
            "\n  4. If the user says 'lactose intolerant' — no dairy in any meal."
            "\n  5. Treat every restriction as a hard medical requirement, not a preference."
            "\n  6. When in doubt, substitute with a safe alternative and note it."
        )

    lines += [
        "\nMEAL PLAN RULES:",
        "  • Every training day must include: Breakfast, Pre-Workout Snack, "
        "Lunch, Post-Workout Meal, Dinner.",
        "  • Every rest day must include: Breakfast, Mid-Morning Snack, "
        "Lunch, Afternoon Snack, Dinner.",
        f"  • All meals must match the {cuisine_str} cuisine style.",
        "  • Include approximate macros (protein / carbs / fat) for each meal.",
        "  • Include total daily calories.",
        "  • Meals must support the client's fitness goal (see CLIENT PROFILE).",
        "  • Do NOT suggest any ingredient excluded in Allergies/Notes above.",
    ]

    return "\n".join(lines)


def build_prompt(name, gender, height, weight, goal, fitness_level, equipment,
                 days_per_week=5, months=1,
                 injuries=None, diet_type="nonveg",
                 cuisine_preference="", cuisine_label="",
                 cuisine_icon="", cuisine_notes=""):
    """
    Build the full AI prompt for workout + diet plan generation.

    New parameters vs old version:
        injuries           : list of injury strings e.g. ["knee", "shoulder"]
        diet_type          : "veg" or "nonveg"
        cuisine_preference : cuisine id string e.g. "indian_nonveg"
        cuisine_label      : human-readable label e.g. "Indian"
        cuisine_icon       : emoji icon e.g. "🍛"
        cuisine_notes      : free-text allergies/preferences e.g. "no eggs, lactose intolerant"
    """
    if injuries is None:
        injuries = []

    bmi       = calculate_bmi(weight, height)
    bmi_cat   = bmi_category(bmi)
    eq_list   = ", ".join(equipment) if equipment else "Bodyweight only (no equipment)"
    advice    = bmi_advice(bmi_cat)
    total_days = days_per_week * 4 * months
    total_days = min(total_days, 30)

    intensity_map = {
        "Beginner":     "2–3 working sets, moderate weight, longer rest (90s). Prioritise form over load.",
        "Intermediate": "3–4 working sets, progressive overload, 60–75s rest.",
        "Advanced":     "4–5 working sets, heavy compound movements, 45–60s rest, supersets where appropriate.",
    }
    intensity = intensity_map.get(fitness_level, "3 sets, 60s rest.")

    # Build optional blocks
    injury_block = build_injury_block(injuries)
    diet_block   = build_diet_block(diet_type, cuisine_preference,
                                    cuisine_label, cuisine_icon, cuisine_notes)

    # Injury summary line for the rules section
    injury_rule = ""
    if injuries:
        injury_rule = (
            f"\n8. INJURIES: The client has {', '.join(injuries)} injuries. "
            f"STRICTLY follow the injury restrictions block above. "
            f"Mark every adapted exercise with '(injury-safe)'."
        )

    allergy_rule = ""
    if cuisine_notes and cuisine_notes.strip():
        allergy_rule = (
            f"\n9. ALLERGIES: '{cuisine_notes.strip()}' — "
            f"zero tolerance. Never include any flagged ingredient in any meal."
        )

    prompt = f"""You are an elite certified personal trainer, sports scientist, and registered nutritionist.
Create a complete, professional {total_days}-day personalised workout AND diet plan
({days_per_week} training days per week × {months} month{'s' if months > 1 else ''}).

━━━ CLIENT PROFILE ━━━
Name           : {name}
Gender         : {gender}
Height / Weight: {height} cm / {weight} kg
BMI            : {bmi:.1f} ({bmi_cat})
Primary Goal   : {goal}
Fitness Level  : {fitness_level}
Equipment      : {eq_list}
Plan Duration  : {days_per_week} days/week for {months} month{'s' if months > 1 else ''} = {total_days} workout days total

━━━ PROGRAMMING NOTES ━━━
• BMI guidance  : {advice}
• Intensity     : {intensity}
• Equipment     : Only use the equipment listed above. Substitute with bodyweight if needed.
• Progression   : Each week should slightly increase intensity, volume or complexity.
• Rest days     : Build rest days into the weekly cycle naturally ({days_per_week} days/week training).

{injury_block}

{diet_block}

━━━ REQUIRED OUTPUT FORMAT ━━━
Use EXACTLY this structure for ALL {total_days} days:

## Day 1 - [Muscle Group / Focus]

**Warm-Up (5 min)**
- Exercise 1: sets x reps
- Exercise 2: sets x reps

**Main Workout**
- Exercise 1 — sets x reps (rest 60s)
- Exercise 2 — sets x reps (rest 60s)
- Exercise 3 — sets x reps (rest 60s)
- Exercise 4 — sets x reps (rest 60s)
- Exercise 5 — sets x reps (rest 60s)

**Cool-Down (3 min)**
- Stretch 1
- Stretch 2

**Meals for the Day**
- Breakfast: [meal name] — [brief description] | Protein: Xg | Carbs: Xg | Fat: Xg
- Pre-Workout Snack: [meal] | Protein: Xg | Carbs: Xg | Fat: Xg
- Lunch: [meal] — [brief description] | Protein: Xg | Carbs: Xg | Fat: Xg
- Post-Workout Meal: [meal] | Protein: Xg | Carbs: Xg | Fat: Xg
- Dinner: [meal] — [brief description] | Protein: Xg | Carbs: Xg | Fat: Xg
- Daily Total: ~XXXX kcal | Protein: Xg | Carbs: Xg | Fat: Xg

[Continue this exact structure for Day 2 through Day {total_days}]

━━━ FINAL SECTION ━━━
End with ONE personalised motivational paragraph addressed directly to {name}.

━━━ RULES ━━━
1. Day headers must start with "## Day N -"
2. Include sets × reps for every exercise (e.g. 3 x 12 reps)
3. Rest periods in parentheses after each exercise
4. No exercises unsafe for {fitness_level} level
5. Ensure variety across all days — don't repeat same muscle groups back-to-back
6. Be specific — no vague instructions
7. Generate ALL {total_days} days — do not stop early{injury_rule}{allergy_rule}
"""
    return prompt, bmi, bmi_cat 