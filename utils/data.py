"""Curated exercise library and sample foods (original lists for WOS4E)."""

EXERCISES = [
    # Strength
    {"id": "sq", "name": "Back Squat", "cat": "strength", "equip": "Barbell", "muscles": "Quads, Glutes"},
    {"id": "bp", "name": "Bench Press", "cat": "strength", "equip": "Barbell", "muscles": "Chest, Triceps"},
    {"id": "dl", "name": "Conventional Deadlift", "cat": "strength", "equip": "Barbell", "muscles": "Posterior chain"},
    {"id": "ohp", "name": "Overhead Press", "cat": "strength", "equip": "Barbell", "muscles": "Shoulders, Triceps"},
    {"id": "row", "name": "Barbell Row", "cat": "strength", "equip": "Barbell", "muscles": "Back, Biceps"},
    {"id": "pullup", "name": "Pull-Up", "cat": "strength", "equip": "Bodyweight", "muscles": "Lats, Biceps"},
    {"id": "rdl", "name": "Romanian Deadlift", "cat": "strength", "equip": "Barbell", "muscles": "Hamstrings, Glutes"},
    {"id": "lunge", "name": "Walking Lunge", "cat": "strength", "equip": "Dumbbell", "muscles": "Quads, Glutes"},
    {"id": "dip", "name": "Dip", "cat": "strength", "equip": "Bodyweight", "muscles": "Chest, Triceps"},
    {"id": "curl", "name": "Barbell Curl", "cat": "strength", "equip": "Barbell", "muscles": "Biceps"},
    {"id": "triceps", "name": "Tricep Pushdown", "cat": "strength", "equip": "Cable", "muscles": "Triceps"},
    {"id": "legpress", "name": "Leg Press", "cat": "strength", "equip": "Machine", "muscles": "Quads, Glutes"},
    {"id": "latpd", "name": "Lat Pulldown", "cat": "strength", "equip": "Cable", "muscles": "Lats"},
    {"id": "facepull", "name": "Face Pull", "cat": "strength", "equip": "Cable", "muscles": "Rear delts"},
    {"id": "hipthrust", "name": "Hip Thrust", "cat": "strength", "equip": "Barbell", "muscles": "Glutes"},
    # Olympic / Power
    {"id": "pc", "name": "Power Clean", "cat": "power", "equip": "Barbell", "muscles": "Full body"},
    {"id": "snatch", "name": "Hang Snatch", "cat": "power", "equip": "Barbell", "muscles": "Full body"},
    {"id": "pushj", "name": "Push Jerk", "cat": "power", "equip": "Barbell", "muscles": "Shoulders, Legs"},
    # Aerobic
    {"id": "run", "name": "Running / Jog", "cat": "aerobic", "equip": "None", "muscles": "Cardio"},
    {"id": "bike", "name": "Cycling", "cat": "aerobic", "equip": "Bike", "muscles": "Cardio, Legs"},
    {"id": "rowm", "name": "Rowing Machine", "cat": "aerobic", "equip": "Machine", "muscles": "Cardio, Back"},
    {"id": "swim", "name": "Swimming", "cat": "aerobic", "equip": "Pool", "muscles": "Full body"},
    {"id": "walk", "name": "Brisk Walk", "cat": "aerobic", "equip": "None", "muscles": "Cardio"},
    # Plyo / Bodyweight
    {"id": "boxjump", "name": "Box Jump", "cat": "plyo", "equip": "Box", "muscles": "Legs, Power"},
    {"id": "burpee", "name": "Burpee", "cat": "plyo", "equip": "Bodyweight", "muscles": "Full body"},
    {"id": "pushup", "name": "Push-Up", "cat": "strength", "equip": "Bodyweight", "muscles": "Chest, Triceps"},
    {"id": "plank", "name": "Plank", "cat": "strength", "equip": "Bodyweight", "muscles": "Core"},
    {"id": "mountain", "name": "Mountain Climber", "cat": "plyo", "equip": "Bodyweight", "muscles": "Core, Cardio"},
]

CATS = {
    "strength": "Strength",
    "power": "Power / Olympic",
    "aerobic": "Aerobic / Cardio",
    "plyo": "Plyometric",
}

PROGRAMS = {
    "beginner_full": {
        "label": "Beginner Full Body (3x/week)",
        "type": "strength",
        "items": [
            {"ex": "sq", "sets": 3, "reps": 8, "rest": 90},
            {"ex": "bp", "sets": 3, "reps": 8, "rest": 90},
            {"ex": "row", "sets": 3, "reps": 8, "rest": 90},
            {"ex": "ohp", "sets": 2, "reps": 10, "rest": 60},
            {"ex": "plank", "sets": 3, "reps": 30, "rest": 45},
        ],
    },
    "upper_lower": {
        "label": "Upper / Lower Split",
        "type": "strength",
        "items": [
            {"ex": "bp", "sets": 4, "reps": 6, "rest": 120},
            {"ex": "row", "sets": 4, "reps": 6, "rest": 120},
            {"ex": "ohp", "sets": 3, "reps": 8, "rest": 90},
            {"ex": "pullup", "sets": 3, "reps": 8, "rest": 90},
            {"ex": "curl", "sets": 3, "reps": 12, "rest": 60},
            {"ex": "triceps", "sets": 3, "reps": 12, "rest": 60},
        ],
    },
    "strength_focus": {
        "label": "Strength Focus (5x5 style)",
        "type": "strength",
        "items": [
            {"ex": "sq", "sets": 5, "reps": 5, "rest": 180},
            {"ex": "bp", "sets": 5, "reps": 5, "rest": 180},
            {"ex": "dl", "sets": 1, "reps": 5, "rest": 180},
            {"ex": "ohp", "sets": 5, "reps": 5, "rest": 150},
            {"ex": "row", "sets": 5, "reps": 5, "rest": 150},
        ],
    },
    "cardio_base": {
        "label": "Aerobic Base Builder",
        "type": "aerobic",
        "items": [
            {"ex": "run", "sets": 1, "reps": 30, "rest": 0},
            {"ex": "bike", "sets": 1, "reps": 20, "rest": 0},
            {"ex": "rowm", "sets": 1, "reps": 15, "rest": 0},
        ],
    },
    "power_day": {
        "label": "Power & Explosiveness",
        "type": "power",
        "items": [
            {"ex": "pc", "sets": 5, "reps": 3, "rest": 120},
            {"ex": "boxjump", "sets": 4, "reps": 5, "rest": 90},
            {"ex": "pushj", "sets": 4, "reps": 3, "rest": 120},
            {"ex": "burpee", "sets": 3, "reps": 10, "rest": 60},
        ],
    },
}

FOODS = [
    {"id": "chicken", "name": "Chicken Breast (cooked)", "cal": 165, "protein": 31, "carb": 0, "fat": 3.6},
    {"id": "rice", "name": "White Rice (cooked)", "cal": 130, "protein": 2.7, "carb": 28, "fat": 0.3},
    {"id": "oats", "name": "Oats (dry)", "cal": 389, "protein": 17, "carb": 66, "fat": 7},
    {"id": "egg", "name": "Whole Egg", "cal": 155, "protein": 13, "carb": 1.1, "fat": 11},
    {"id": "salmon", "name": "Salmon (cooked)", "cal": 208, "protein": 20, "carb": 0, "fat": 13},
    {"id": "broccoli", "name": "Broccoli", "cal": 34, "protein": 2.8, "carb": 7, "fat": 0.4},
    {"id": "banana", "name": "Banana", "cal": 89, "protein": 1.1, "carb": 23, "fat": 0.3},
    {"id": "milk", "name": "Milk (2%)", "cal": 50, "protein": 3.3, "carb": 4.8, "fat": 2},
    {"id": "greek", "name": "Greek Yogurt (plain)", "cal": 59, "protein": 10, "carb": 3.6, "fat": 0.4},
    {"id": "almond", "name": "Almonds", "cal": 579, "protein": 21, "carb": 22, "fat": 50},
    {"id": "sweetpotato", "name": "Sweet Potato (baked)", "cal": 90, "protein": 2, "carb": 21, "fat": 0.2},
    {"id": "beef", "name": "Lean Ground Beef (90%)", "cal": 176, "protein": 20, "carb": 0, "fat": 10},
    {"id": "whey", "name": "Whey Protein Scoop", "cal": 120, "protein": 24, "carb": 3, "fat": 1},
    {"id": "avocado", "name": "Avocado", "cal": 160, "protein": 2, "carb": 9, "fat": 15},
    {"id": "oliveoil", "name": "Olive Oil (tbsp)", "cal": 119, "protein": 0, "carb": 0, "fat": 13.5},
]


def ex_by_id(eid: str):
    for e in EXERCISES:
        if e["id"] == eid:
            return e
    return None


def food_by_id(fid: str):
    for f in FOODS:
        if f["id"] == fid:
            return f
    return None
