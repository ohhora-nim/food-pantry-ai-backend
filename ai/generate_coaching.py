# =========================================
# coaching_ai.py
# Gemma AI Human Coaching Engine
# =========================================

import json
from .run_ollama import run_ai, clean_text


# =========================================
# Build Prompt
# =========================================

def build_coaching_prompt(context):
    return f"""
Task:
Give healthy pantry coaching.

Data:
{json.dumps(context)}

Rules:
- supportive
- practical
- human-like
- concise
- positive tone
- mention healthy eating
- mention waste reduction
- mention budget awareness
- max 4 sentences

Return plain text only.
"""


# =========================================
# Generate Coaching
# =========================================

def generate_coaching(pantry_foods, nutrition_analytics, waste_forecast):

    """
    Main AI coaching generator.

    Optimized for:
    - local Gemma
    - short generation
    - fast inference
    """

    try:
        context = build_coaching_context(pantry_foods, nutrition_analytics, waste_forecast)
        prompt = build_coaching_prompt(context)

        options={
            "temperature": 0.5,
            "top_p": 0.8,
            "top_k": 20,
            "max_output_tokens": 160
        }
        
        content = run_ai(prompt, options)
        coaching = clean_text(content)

        # =================================
        # Validation
        # =================================

        if not coaching:
            return generate_fallback_coaching(nutrition_analytics, waste_forecast)

        return coaching

    except Exception as e:
        print("Coaching generation error:", e)

        return generate_fallback_coaching(nutrition_analytics, waste_forecast)



# =========================================
# Build Coaching Context
# =========================================

def build_coaching_context(pantry_foods, nutrition_analytics, waste_forecast):
    """
    Compact context for fast inference.
    """

    # =====================================
    # Pantry snapshot
    # =====================================

    pantry_snapshot = [{
        "name": food.get("name"),
        "priority": food.get("priority_score", 0),
        "expiry": food.get("expiry_score", 0)
        } for food in pantry_foods[:10]]

    # =====================================
    # Nutrition
    # =====================================

    nutrition = {
        "health_score": nutrition_analytics.get("pantry_health_score", 0),
        "fresh_percent": nutrition_analytics.get("fresh_percent", 0),
        "ultra_processed_percent": nutrition_analytics.get("ultra_processed_percent", 0),
        "top_tags": [tag.get("tag") for tag in nutrition_analytics.get("top_tags", [])[:3]]
    }

    # =====================================
    # Waste
    # =====================================
    waste = {
        "waste_score": waste_forecast.get("overall_waste_score", 0),
        "urgent_items": waste_forecast.get("urgent_items", 0)
    }

    return {
        "pantry": pantry_snapshot,
        "nutrition": nutrition,
        "waste": waste
    }





# =========================================
# Fallback Coaching
# =========================================

def generate_fallback_coaching(nutrition_analytics, waste_forecast):
    health_score = nutrition_analytics.get("pantry_health_score", 0)
    fresh_percent = nutrition_analytics.get("fresh_percent", 0)
    waste_score = waste_forecast.get("overall_waste_score", 0)
    urgent_items = waste_forecast.get("urgent_items", 0)

    coaching = []

    # =====================================
    # Nutrition
    # =====================================

    if health_score >= 80:
        coaching.append("Your pantry has strong nutrition quality.")

    elif fresh_percent < 50:
        coaching.append("Add more fresh whole foods for better balance.")

    else:
        coaching.append("Your pantry nutrition is reasonably balanced.")

    # =====================================
    # Waste
    # =====================================

    if urgent_items >= 3:
        coaching.append("Prioritize foods expiring soon.")

    elif waste_score >= 50:
        coaching.append("Plan meals around fresh ingredients first.")

    else:
        coaching.append("Your waste management looks good.")

    # =====================================
    # Budget
    # =====================================

    coaching.append("Using pantry foods first can reduce grocery costs.")

    return " ".join(coaching)