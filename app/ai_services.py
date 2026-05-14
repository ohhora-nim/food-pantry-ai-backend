import os
import json
from ollama import Client
from datetime import date, datetime

from .prompts import (
    CLASSIFY_FOOD_PROMPT, 
    WEEKLY_PLAN_PROMPT,
    WASTE_FORECAST,
    BUDGET_PROMPT,
    HEALTH_COACH,
    GROCERY_PROMPT,
    RECOMMENDATION_PROMPT
)


# ============================
# AI Settings
# ============================


AI_MODEL = 'gemma4'
OLLAMA_HOST = os.getenv("OLLAMA_HOST")

client = Client(
    host=f'{OLLAMA_HOST}:11434'
)


# ============================
# Main
# ============================


def classify_food(food_name):
    prompt = CLASSIFY_FOOD_PROMPT.format(food_name)

    content = run_ai(prompt)

    try:
        return json.loads(content)

    except:
        return {
            "category": "vegetable",
            "processing_level": "fresh",
            "nutrition_tags": ["fiber"],
            "nutrition_score": 7
        }


def generate_structured_meals(ranked_foods):
    if not ranked_foods:
        return []

    food_summary = []
    for food in ranked_foods:
        food_summary.append({
            "name": food["name"],
            "category": food["category"],
            "processing_level": food["processing_level"],
            "nutrition_tags": food["nutrition_tags"],
            "nutrition_score": food["nutrition_score"],
            "priority_score": food["priority_score"],
            "expiry_date": str(food["expiry_date"])
        })

    prompt = WEEKLY_PLAN_PROMPT.format(json.dumps(food_summary, indent=2))

    content = run_ai(prompt)

    try:
        meals = json.loads(content)

        # ======================================
        # Safety Validation
        # ======================================

        validated = []

        for day in meals:

            if "day" not in day or "meals" not in day:
                continue

            meal_obj = day["meals"]

            for meal_type in ["breakfast", "lunch", "dinner"]:
                if meal_type not in meal_obj:
                    meal_obj[meal_type] = {
                        "name": "Missing Meal",
                        "ingredients": [],
                        "steps": [],
                        "reason": "AI failed to generate meal.",
                        "score": 50
                    }
            validated.append({
                "day": day["day"],
                "meals": meal_obj
            })

        return validated

    # ==========================================
    # Fallback
    # ==========================================

    except Exception as e:
        print("Meal Generation Error:", e)

        fallback = []

        days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
        ]

        for i, day in enumerate(days):

            food = ranked_foods[
                i % len(ranked_foods)
            ]

            fallback.append({

                "day": day,

                "meals": {

                    "breakfast": {

                        "name":
                            f"{food['name']} Breakfast Bowl",

                        "ingredients": [

                            {
                                "name":
                                    food["name"],

                                "category":
                                    food["category"],

                                "processing_level":
                                    food[
                                        "processing_level"
                                    ],

                                "nutrition_tags":
                                    food[
                                        "nutrition_tags"
                                    ]
                            }
                        ],

                        "steps": [

                            "Prepare ingredients carefully.",

                            "Cook over medium heat.",

                            "Serve warm."
                        ],

                        "reason":

                            "Fallback AI breakfast meal.",

                        "score": 80
                    },

                    "lunch": {

                        "name":
                            f"{food['name']} Lunch Plate",

                        "ingredients": [

                            {
                                "name":
                                    food["name"],

                                "category":
                                    food["category"],

                                "processing_level":
                                    food[
                                        "processing_level"
                                    ],

                                "nutrition_tags":
                                    food[
                                        "nutrition_tags"
                                    ]
                            }
                        ],

                        "steps": [

                            "Prepare ingredients carefully.",

                            "Cook over medium heat.",

                            "Serve warm."
                        ],

                        "reason":

                            "Fallback AI lunch meal.",

                        "score": 82
                    },

                    "dinner": {

                        "name":
                            f"{food['name']} Dinner Plate",

                        "ingredients": [

                            {
                                "name":
                                    food["name"],

                                "category":
                                    food["category"],

                                "processing_level":
                                    food[
                                        "processing_level"
                                    ],

                                "nutrition_tags":
                                    food[
                                        "nutrition_tags"
                                    ]
                            }
                        ],

                        "steps": [

                            "Prepare ingredients carefully.",

                            "Cook over medium heat.",

                            "Serve warm."
                        ],

                        "reason":

                            "Fallback AI dinner meal.",

                        "score": 85
                    }
                }
            })

        return fallback


def generate_waste_forecast( ranked_foods, weekly_plan=None):

    if not ranked_foods:
        return []

    # ==========================================
    # Prepare Food Data
    # ==========================================

    foods_data = []

    for food in ranked_foods:
        days_left = calculate_days_left(food["expiry_date"])
        foods_data.append({
            "name": food["name"],
            "quantity": food["quantity"],
            "category": food["category"],
            "processing_level": food["processing_level"],
            "nutrition_score": food["nutrition_score"],
            "priority_score": food["priority_score"],
            "expiry_score": food["expiry_score"],
            "days_left": days_left,
            "expiry_date": str(food["expiry_date"])
        })

    # ==========================================
    # Weekly Plan Summary
    # ==========================================

    weekly_summary = []

    if weekly_plan:
        weekly_summary = get_weekly_summary(weekly_plan)

    prompt = WASTE_FORECAST.format(
        json.dumps(foods_data, indent=2),
        json.dumps(weekly_summary, indent=2)
    )

    content = run_ai(prompt)

    try:
        forecast = json.loads(content)

        validated = []

        for item in forecast:
            validated.append({
                "name": item.get("name", "Unknown"),
                "days_left": int(item.get("days_left", 0)),
                "risk_level": item.get("risk_level", "Medium"),
                "recommendation": item.get("recommendation", "Use soon to reduce food waste.")
            })

        return validated

    # ==========================================
    # Fallback System
    # ==========================================

    except Exception as e:

        print(
            "Waste Forecast Error:",
            e
        )

        fallback = []

        for food in ranked_foods:

            days_left = calculate_days_left(

                food["expiry_date"]
            )

            # ==================================
            # Risk Level
            # ==================================

            if days_left <= 2:

                risk = "High"

                recommendation = (

                    f"Use {food['name']} immediately "
                    "or freeze portions today "
                    "to avoid food waste."
                )

            elif days_left <= 5:

                risk = "Medium"

                recommendation = (

                    f"Plan meals using "
                    f"{food['name']} within "
                    "the next few days."
                )

            else:

                risk = "Low"

                recommendation = (

                    f"{food['name']} is stable "
                    "for now, but rotate pantry "
                    "items regularly for freshness."
                )

            fallback.append({

                "name":
                    food["name"],

                "days_left":
                    days_left,

                "risk_level":
                    risk,

                "recommendation":
                    recommendation
            })

        # ======================================
        # Sort Highest Risk First
        # ======================================

        risk_order = {

            "High": 0,

            "Medium": 1,

            "Low": 2
        }

        fallback.sort(

            key=lambda x: (

                risk_order[
                    x["risk_level"]
                ],

                x["days_left"]
            )
        )

        return fallback



def generate_budget_analysis(ranked_foods, weekly_plan=None):

    if not ranked_foods:

        return {

            "estimated_savings": 0,

            "waste_reduction_percent": 0,

            "budget_score": 0,

            "monthly_projection": 0,

            "high_value_foods": [],

            "waste_risk_foods": [],

            "optimization_tips": [

                "Add pantry foods to receive AI budget analysis."
            ],

            "shopping_strategy":

                "No pantry data available.",

            "summary":

                "Budget analysis unavailable."
        }

    # ==========================================
    # Prepare Food Data
    # ==========================================

    foods_data = []

    for food in ranked_foods:
        foods_data.append({
            "name": food["name"],
            "quantity": food["quantity"],
            "category": food["category"],
            "processing_level": food["processing_level"],
            "nutrition_score": food["nutrition_score"],
            "priority_score": food["priority_score"],
            "expiry_score": food["expiry_score"],
            "expiry_date": str(food["expiry_date"])
        })

    # ==========================================
    # Weekly Plan Summary
    # ==========================================

    weekly_summary = []
    if weekly_plan:
        for plan in weekly_plan:
            meals = plan["meals"]
            meal_names = []
            for m in ["breakfast", "lunch", "dinner"]:
                meal = meals[m]
                meal_names.append(meal["name"])

            weekly_summary.append({
                "day": plan["day"],
                "meals": meal_names
            })
    
    # ==========================================
    # GEMMA AI PROMPT
    # ==========================================

    prompt = BUDGET_PROMPT.format(json.dumps(foods_data, indent=2), json.dumps(weekly_summary, indent=2))

    response = ollama.chat(
        model=f'{AI_MODEL}',
        messages=[{"role": "user", "content": prompt}]
    )

    content = clean_json(response["message"]["content"])

    try:
        analysis = json.loads(content)

        # ======================================
        # Safety Defaults
        # ======================================

        analysis.setdefault("estimated_savings", 0)
        analysis.setdefault("waste_reduction_percent", 0)
        analysis.setdefault("budget_score", 70)
        analysis.setdefault("monthly_projection", 0)
        analysis.setdefault("high_value_foods", [])
        analysis.setdefault("waste_risk_foods", [])
        analysis.setdefault("optimization_tips", [])
        analysis.setdefault("shopping_strategy", "No strategy generated.")
        analysis.setdefault("summary", "No summary generated.")

        return analysis

    # ==========================================
    # Fallback System
    # ==========================================

    except Exception as e:

        print(
            "Budget Analysis Error:",
            e
        )

        # ======================================
        # Manual AI-like Analysis
        # ======================================

        high_value = []

        waste_risk = []

        estimated_savings = 0

        for food in ranked_foods:

            if (
                food[
                    "nutrition_score"
                ] >= 8
            ):

                high_value.append(
                    food["name"]
                )

            if (
                food[
                    "expiry_score"
                ] >= 8
            ):

                waste_risk.append(
                    food["name"]
                )

            estimated_savings += 4

        monthly_projection = (
            estimated_savings * 4
        )

        waste_reduction = min(

            85,

            len(ranked_foods) * 6
        )

        budget_score = min(

            95,

            60 +

            len(high_value) * 5
        )

        return {

            "estimated_savings":

                round(
                    estimated_savings,
                    1
                ),

            "waste_reduction_percent":

                round(
                    waste_reduction,
                    1
                ),

            "budget_score":

                round(
                    budget_score,
                    1
                ),

            "monthly_projection":

                round(
                    monthly_projection,
                    1
                ),

            "high_value_foods":

                high_value,

            "waste_risk_foods":

                waste_risk,

            "optimization_tips": [

                "Use high-priority foods earlier in the week.",

                "Freeze meats before expiry dates.",

                "Plan meals around expiring vegetables.",

                "Avoid duplicate grocery purchases.",

                "Use pantry-first meal planning before shopping."
            ],

            "shopping_strategy":

                "Prioritize fresh whole foods, "
                "buy proteins in bulk when discounted, "
                "and reduce ultra-processed food purchases "
                "to maximize long-term savings.",

            "summary":

                "AI analysis predicts meaningful "
                "budget savings through waste reduction, "
                "smarter pantry rotation, and improved "
                "meal planning efficiency."
        }


def generate_health_coaching(analytics, ranked_foods=None, weekly_plan=None):
    if not analytics:

        return {

            "health_score": 0,

            "strengths": [],

            "risks": [],

            "recommendations": [],

            "nutrition_focus": "",

            "fitness_tip": "",

            "longevity_tip": "",

            "hydration_tip": "",

            "meal_balance_feedback": "",

            "summary": "No analytics data available."
        }

    # ==========================================
    # Prepare Analytics Data
    # ==========================================

    analytics_data = {
        "total_calories": analytics.get("total_calories", 0),
        "total_protein": analytics.get("total_protein", 0),
        "total_carbs": analytics.get("total_carbs", 0),
        "total_fat": analytics.get("total_fat", 0),
        "total_fiber": analytics.get("total_fiber", 0),
        "total_sugar": analytics.get("total_sugar", 0),
        "total_sodium": analytics.get("total_sodium", 0),
        "average_nutrition_score": analytics.get("average_nutrition_score", 0),
        "fresh_percent": analytics.get("fresh_percent", 0),
        "processed_percent": analytics.get("processed_percent", 0),
        "ultra_processed_percent": analytics.get("ultra_processed_percent", 0)
    }

    # ==========================================
    # Food Summary
    # ==========================================

    food_summary = []

    if ranked_foods:
        for food in ranked_foods:
            food_summary.append({
                "name": food["name"],
                "category": food["category"],
                "processing_level": food["processing_level"],
                "nutrition_tags": food["nutrition_tags"],
                "nutrition_score": food["nutrition_score"]
            })

    # ==========================================
    # Weekly Plan Summary
    # ==========================================

    weekly_summary = []

    if weekly_plan:
        weekly_summary = get_weekly_summary(weekly_plan)

    prompt = HEALTH_COACH.format(
        json.dumps(analytics_data, indent=2),
        json.dumps(food_summary, indent=2),
        json.dumps(weekly_summary, indent=2)
    )

    content = run_ai(prompt)

    try:
        coaching = json.loads(content)

        # ======================================
        # Safety Defaults
        # ======================================

        coaching.setdefault("health_score", 70)
        coaching.setdefault("strengths", [])
        coaching.setdefault("risks", [])
        coaching.setdefault("recommendations", [])
        coaching.setdefault("nutrition_focus", "")
        coaching.setdefault("fitness_tip", "")
        coaching.setdefault("longevity_tip", "")
        coaching.setdefault("hydration_tip", "")
        coaching.setdefault("meal_balance_feedback", "")
        coaching.setdefault("summary", "")

        return coaching

    # ==========================================
    # Fallback System
    # ==========================================

    except Exception as e:

        print(
            "Health Coaching Error:",
            e
        )

        strengths = []

        risks = []

        recommendations = []

        # ======================================
        # Health Score
        # ======================================

        health_score = 70

        if (
            analytics[
                "fresh_percent"
            ] > 60
        ):

            strengths.append(
                "High fresh food intake."
            )

            health_score += 10

        if (
            analytics[
                "ultra_processed_percent"
            ] > 40
        ):

            risks.append(
                "High ultra-processed food intake."
            )

            health_score -= 10

        if (
            analytics[
                "total_fiber"
            ] < 25
        ):

            risks.append(
                "Low dietary fiber intake."
            )

            recommendations.append(
                "Increase vegetables, legumes, and oats."
            )

        if (
            analytics[
                "total_sodium"
            ] > 3000
        ):

            risks.append(
                "High sodium intake."
            )

            recommendations.append(
                "Reduce processed foods and salty snacks."
            )

        if (
            analytics[
                "total_sugar"
            ] > 50
        ):

            risks.append(
                "Elevated sugar intake."
            )

            recommendations.append(
                "Reduce sugary drinks and desserts."
            )

        recommendations.append(
            "Drink water consistently throughout the day."
        )

        recommendations.append(
            "Maintain regular meal timing."
        )

        recommendations.append(
            "Aim for balanced meals with protein and vegetables."
        )

        return {

            "health_score":

                max(
                    1,
                    min(
                        100,
                        health_score
                    )
                ),

            "strengths":

                strengths,

            "risks":

                risks,

            "recommendations":

                recommendations,

            "nutrition_focus":

                "Increase whole foods and reduce ultra-processed foods.",

            "fitness_tip":

                "Combine strength training with daily walking for long-term health benefits.",

            "longevity_tip":

                "Prioritize consistent healthy eating habits over extreme diets.",

            "hydration_tip":

                "Drink water regularly and reduce sugary beverages.",

            "meal_balance_feedback":

                "Meals should consistently include protein, vegetables, and fiber-rich foods.",

            "summary":

                "AI health analysis suggests focusing on whole foods, improving nutrient balance, and reducing processed food intake for long-term wellness."
        }








# =========================================
# Generate Smart Grocery List
# =========================================

import json
import re

# =========================================
# Helpers
# =========================================

def safe_json_loads(text):

    """
    Safely extract JSON from Gemma output
    """

    try:

        # remove markdown blocks
        text = re.sub(
            r"```json|```",
            "",
            text
        ).strip()

        # find first json array
        match = re.search(
            r"\[.*\]",
            text,
            re.DOTALL
        )

        if match:

            return json.loads(
                match.group(0)
            )

        return []

    except Exception as e:

        print(
            "JSON Parse Error:",
            e
        )

        return []


# =========================================
# Generate Grocery List
# =========================================

def generate_grocery_list(weekly_plan, recommendations, pantry_foods):

    pantry_names = []
    for food in pantry_foods:
        pantry_names.append(
            food.get("name","").lower()
        )

    # =====================================
    # Build Meal Summary
    # =====================================

    meal_summary = []

    for day_data in weekly_plan:
        day_name = day_data.get("day", "")
        meals = day_data.get("meals", {})

        for meal_type, meal in meals.items():
            if not meal:
                continue

            meal_summary.append({
                "day": day_name,
                "meal_type": meal_type,
                "meal_name": meal.get("name", ""),
                "ingredients": [ingredient.get("name", "") for ingredient in meal.get("ingredients",[])]
            })

    # =====================================
    # Recommendation Summary
    # =====================================

    recommendation_summary = []
    for item in recommendations:
        recommendation_summary.append({
            "name": item.get("name", ""),
            "category": item.get("category", ""),
            "nutrition_tags": item.get("nutrition_tags", []),
            "reason": item.get("reason", "")
        })

    prompt = GROCERY_PROMPT.format(
        json.dumps(pantry_names, indent=2),
        json.dumps(meal_summary, indent=2),
        json.dumps(recommendation_summary, indent=2)
    )

    content = run_ai(prompt)

    try:
        grocery_list = json.loads(content)

    except Exception as e:

        print(
            "Gemma Grocery Error:",
            e
        )

        grocery_list = []

    # =====================================
    # Fallback
    # =====================================

    if not grocery_list:

        grocery_list = [

            {
                "name": "spinach",

                "quantity": 2,

                "unit": "bags",

                "category": "vegetable",

                "priority": "high",

                "estimated_price": 5,

                "nutrition_score": 9,

                "nutrition_tags": [
                    "fiber",
                    "vitamin",
                    "iron"
                ],

                "meal_support": [
                    "Weekly Meals"
                ],

                "storage_tip":
                    "Store refrigerated.",

                "reason":
                    "Healthy versatile ingredient for multiple meals."
            },

            {
                "name": "greek yogurt",

                "quantity": 1,

                "unit": "container",

                "category": "dairy",

                "priority": "medium",

                "estimated_price": 7,

                "nutrition_score": 8,

                "nutrition_tags": [
                    "protein",
                    "calcium"
                ],

                "meal_support": [
                    "Breakfast"
                ],

                "storage_tip":
                    "Keep refrigerated.",

                "reason":
                    "High protein food supporting healthy breakfasts."
            }
        ]

    # =====================================
    # Final Cleanup
    # =====================================

    cleaned = []

    seen = set()

    for item in grocery_list:

        name = item.get(
            "name",
            ""
        ).strip().lower()

        if not name:

            continue

        # avoid duplicates
        if name in seen:

            continue

        seen.add(name)

        # avoid pantry duplicates
        if name in pantry_names:

            continue

        cleaned.append({

            "name":
                item.get(
                    "name",
                    ""
                ),

            "quantity":
                item.get(
                    "quantity",
                    1
                ),

            "unit":
                item.get(
                    "unit",
                    "item"
                ),

            "category":
                item.get(
                    "category",
                    "other"
                ),

            "priority":
                item.get(
                    "priority",
                    "medium"
                ),

            "estimated_price":
                item.get(
                    "estimated_price",
                    0
                ),

            "nutrition_score":
                item.get(
                    "nutrition_score",
                    7
                ),

            "nutrition_tags":
                item.get(
                    "nutrition_tags",
                    []
                ),

            "meal_support":
                item.get(
                    "meal_support",
                    []
                ),

            "storage_tip":
                item.get(
                    "storage_tip",
                    ""
                ),

            "reason":
                item.get(
                    "reason",
                    ""
                )
        })

    # =====================================
    # Sort Priority
    # =====================================

    priority_order = {

        "high": 0,
        "medium": 1,
        "low": 2
    }

    cleaned.sort(

        key=lambda x:

        priority_order.get(
            x["priority"].lower(),
            99
        )
    )

    return cleaned


def generate_recommended_foods():
    prompt = RECOMMENDATION_PROMPT

    response = client.chat(
        model=f'{AI_MODEL}',
        messages=[{"role": "user", "content": prompt}]
    )

    content = clean_json(response["message"]["content"])

    try:
        return json.loads(content)
    except Exception:
        return []


# ============================
# Helpers
# ============================


def run_ai(prompt):
    response = client.chat(
        model=f'{AI_MODEL}',
        messages=[{"role": "user", "content": prompt}]
    )

    return clean_json(response["message"]["content"])


def get_weekly_summary(weekly_plan):
    weekly_summary = []
    for plan in weekly_plan:
        meals = plan["meals"]
        meal_names = []
        for m in ["breakfast", "lunch", "dinner"]:
            meal = meals[m]
            meal_names.append(meal["name"])

        weekly_summary.append({
            "day": plan["day"],
            "meals": meal_names
        })
    
    return weekly_summary


def calculate_days_left(expiry_date):
    if isinstance(expiry_date, str):
        expiry_date = datetime.strptime(expiry_date, "%Y-%m-%d").date()

    delta = expiry_date - date.today()
    return delta.days


def clean_json(s):
    return s.replace('```json', '').replace('```', '')