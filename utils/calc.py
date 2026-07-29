"""Fitness & nutrition calculations (original implementation)."""

ACTIVITY_MULTIPLIERS = {
    "sedentary": 1.2,
    "light": 1.375,
    "moderate": 1.55,
    "active": 1.725,
    "very_active": 1.9,
}

GOAL_ADJUST = {
    "lose": -500,
    "maintain": 0,
    "gain": 300,
    "recomp": -200,
}


def calc_bmr(sex: str, weight_kg: float, height_cm: float, age: int) -> float:
    """Mifflin-St Jeor."""
    if sex == "male":
        return 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    return 10 * weight_kg + 6.25 * height_cm - 5 * age - 161


def calc_tdee(bmr: float, activity: str) -> float:
    return bmr * ACTIVITY_MULTIPLIERS.get(activity, 1.55)


def calc_target_calories(tdee: float, goal: str) -> float:
    return max(1200, tdee + GOAL_ADJUST.get(goal, 0))


def calc_macros(calories: float, goal: str, weight_kg: float) -> dict:
    """Simple macro split by goal."""
    if goal == "lose":
        protein_g = weight_kg * 2.2
        fat_g = weight_kg * 0.8
    elif goal == "gain":
        protein_g = weight_kg * 1.8
        fat_g = weight_kg * 1.0
    else:
        protein_g = weight_kg * 2.0
        fat_g = weight_kg * 0.9
    protein_cal = protein_g * 4
    fat_cal = fat_g * 9
    carb_cal = max(0, calories - protein_cal - fat_cal)
    return {
        "protein": round(protein_g, 1),
        "fat": round(fat_g, 1),
        "carb": round(carb_cal / 4, 1),
        "calories": round(calories),
    }


def estimate_1rm(weight: float, reps: int) -> float:
    """Epley formula."""
    if reps <= 0 or weight <= 0:
        return 0.0
    if reps == 1:
        return weight
    return round(weight * (1 + reps / 30), 1)


def bmi(weight_kg: float, height_cm: float) -> float:
    if height_cm <= 0:
        return 0.0
    h = height_cm / 100
    return round(weight_kg / (h * h), 1)


def volume(exercises: list) -> float:
    total = 0.0
    for e in exercises:
        total += (e.get("weight") or 0) * (e.get("sets") or 0) * (e.get("reps") or 0)
    return total
