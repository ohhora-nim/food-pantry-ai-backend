# =========================================
# summary_ai.py
# Gemma AI Summary Engine
# =========================================

import json
from .run_ollama import run_ai, clean_text



# =========================================
# Build Prompt
# =========================================

def build_summary_prompt(
    context
):

    return f"""
Task:
Write a short pantry health summary.

Data:
{json.dumps(context)}

Rules:
- supportive tone
- practical advice
- concise
- max 3 sentences
- mention waste reduction
- mention healthy eating

Return plain text only.
"""


# =========================================
# Main Generate Summary
# =========================================

def generate_summary(nutrition_analytics, waste_forecast, recommendations):

    """
    Generate human-friendly
    AI pantry summary.

    Optimized for:
    - local Gemma
    - low latency
    - short outputs
    """

    try:
        context = build_summary_context(nutrition_analytics, waste_forecast, recommendations)
        prompt = build_summary_prompt(context)
        options = {
            "temperature": 0.4,
            "top_p": 0.8,
            "top_k": 20,
            "max_output_tokens": 120
        }
        
        content = run_ai(prompt, options)
        summary = clean_text(content)

        # =================================
        # Validation
        # =================================

        if not summary:
            return generate_fallback_summary(nutrition_analytics, waste_forecast)

        return summary

    except Exception as e:
        print("Summary generation error:", e)

        return generate_fallback_summary(nutrition_analytics, waste_forecast)



# =========================================
# Build Analytics Context
# =========================================

def build_summary_context(nutrition_analytics, waste_forecast, recommendations):
    """
    Keep context VERY compact
    for fast local Gemma inference.
    """

    return {
        "nutrition": {
            "health_score": nutrition_analytics.get("pantry_health_score", 0),
            "fresh_percent": nutrition_analytics.get("fresh_percent", 0),
            "ultra_processed_percent": nutrition_analytics.get("ultra_processed_percent", 0),
            "top_tags": [tag.get("tag") for tag in nutrition_analytics.get("top_tags", [])[:3]]
        },
        "waste": {
            "waste_score": waste_forecast.get("overall_waste_score", 0),
            "urgent_items": waste_forecast.get("urgent_items", 0)
        },
        "recommended_foods": [food.get("name") for food in recommendations[:3]]
    }


# =========================================
# Fallback Summary
# =========================================

def generate_fallback_summary(nutrition_analytics, waste_forecast):
    health_score = nutrition_analytics.get("pantry_health_score", 0)
    waste_score = waste_forecast.get("overall_waste_score", 0)

    if health_score >= 80:
        health_text = "Your pantry has strong nutrition quality."

    elif health_score >= 60:
        health_text = "Your pantry nutrition is balanced."

    else:
        health_text = "Consider adding more fresh whole foods."

    if waste_score >= 70:
        waste_text = "Several foods should be used soon."

    elif waste_score >= 40:
        waste_text = "Monitor expiry dates to reduce waste."

    else:
        waste_text = "Your food waste risk is well controlled."

    return f"{health_text} {waste_text}"
