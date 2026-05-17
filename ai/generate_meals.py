# =========================================
# generate_meals.py
# Gemma AI Meal Generation Engine
# =========================================

import json
import re
from .run_ollama import run_ai, clean_text




# =========================================
# Build Prompt
# =========================================

def build_meal_prompt(pantry_context):
    return f"""
Task:
Generate 7 healthy meals.

Foods:
{json.dumps(pantry_context)}

Rules:
- reduce food waste
- prioritize urgent foods
- simple cooking
- affordable meals
- healthy whole foods
- concise steps

Return JSON only.

[
  {{
    "day":"Monday",
    "meal":"Dinner",
    "name":"Meal name",
    "ingredients":[
      "egg",
      "spinach"
    ],
    "steps":[
      "Cook eggs.",
      "Add spinach."
    ],
    "health_reason":"High protein and fiber.",
    "waste_reason":"Uses expiring spinach."
  }}
]
"""


# =========================================
# Main Generate Meals
# =========================================


def generate_meals(pantry_foods):
    """
    Main AI meal generation.

    Optimized for:
    - low-end PCs
    - local Gemma
    - low latency
    """

    try:
        pantry_context = build_pantry_context(pantry_foods)
        prompt = build_meal_prompt(pantry_context)

        options = {
            "temperature": 0.3,
            "top_p": 0.8,
            "top_k": 20,
            "max_output_tokens": 250
        }

        content = run_ai(prompt, options)
        meals = json.loads(content)

        if not meals:
            return generate_fallback_meals()

        meals = normalize_meals(meals)

        return meals

    except Exception as e:
        print("Meal generation error:", e)

        return generate_fallback_meals()


# =========================================
# Build Compact Pantry
# =========================================

def build_pantry_context(pantry_foods):
    """
    Keep prompt VERY small.
    """

    foods = []
    for food in pantry_foods:
        name = food.get("name", "")
        expiry_score = food.get("expiry_score", 0)
        priority_score = food.get("priority_score", 0)
        foods.append({
            "name": name,
            "urgent": expiry_score >= 8,
            "priority": priority_score >= 70
        })

    return foods[:20]


# =========================================
# Normalize Meals
# =========================================

def normalize_meals(meals):
    normalized = []
    for meal in meals:
        normalized.append({
            "day": meal.get("day", "Monday"),
            "meal": meal.get("meal", "Dinner"),
            "name": meal.get("name", "Healthy Meal"),
            "ingredients": meal.get("ingredients", []),
            "steps": meal.get("steps", []),
            "health_reason": meal.get("health_reason", ""),
            "waste_reason": meal.get("waste_reason", "")
        })

    return normalized

# =========================================
# Fallback Meals
# =========================================

def generate_fallback_meals():
    return [
        {
            "day": "Monday",
            "meal": "Dinner",
            "name": "Vegetable Rice Bowl",
            "ingredients": [
                "rice",
                "vegetables"
            ],
            "steps": [
                "Cook rice.",
                "Cook vegetables.",
                "Combine together."
            ],
            "health_reason": "Balanced healthy meal.",
            "waste_reason": "Uses pantry vegetables."
        },
        {
            "day": "Tuesday",
            "meal": "Lunch",
            "name": "Egg Spinach Scramble",
            "ingredients": [
                "egg",
                "spinach"
            ],
            "steps": [
                "Cook eggs.",
                "Add spinach."
            ],
            "health_reason": "High protein meal.",
            "waste_reason": "Uses fresh spinach."
        }
    ]
