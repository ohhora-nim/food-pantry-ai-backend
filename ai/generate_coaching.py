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
Create AI health coaching from pantry data.

Data:
{json.dumps(context, separators=(",", ":"))}

Return JSON only.

Format:
{{
  "summary":"1-2 sentence overview.",
  "strengths":["short strength","short strength"],
  "risks":["short risk"],
  "recommendations":["short action","short action","short action"],
  "nutrition_focus":"one key nutrition focus",
  "fitness_tip":"short realistic fitness tip",
  "hydration_tip":"short hydration tip",
  "meal_balance_feedback":"short meal balance feedback"
}}

Rules:
- Keep all text concise
- Be supportive and practical
- Mention healthy eating
- Mention food waste reduction
- Fitness tip must be safe and realistic
- No markdown
- No explanation outside JSON
- Max 3 strengths
- Max 3 risks
- Max 4 recommendations
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
            "max_output_tokens": 350
        }
        
        content = run_ai(prompt, options)
        coaching = json.loads(content)

        return {
            "summary": coaching.get("summary", ""),
            "strengths": coaching.get("strengths", []),
            "risks": coaching.get("risks", []),
            "recommendations": coaching.get("recommendations", []),
            "nutrition_focus": coaching.get("nutrition_focus", ""),
            "fitness_tip": coaching.get("fitness_tip", ""),
            "hydration_tip": coaching.get("hydration_tip", ""),
            "meal_balance_feedback": coaching.get("meal_balance_feedback", "")
        }

    except Exception as e:
        print("Coaching generation error:", e)

        return {
            "summary": generate_fallback_coaching(nutrition_analytics, waste_forecast),
            "strengths": [
                "Pantry tracking supports better food decisions."
            ],
            "risks": [
                "Some foods may become waste if not planned."
            ],
            "recommendations": [
                "Use foods with high expiry priority first.",
                "Build meals around fresh whole foods.",
                "Add protein and fiber-rich foods when possible."
            ],
            "nutrition_focus": "Prioritize fresh foods, protein, and fiber.",
            "fitness_tip": "Add a short daily walk after meals when possible.",
            "hydration_tip": "Drink water regularly throughout the day.",
            "meal_balance_feedback": "Aim for meals with protein, vegetables, and fiber."
        }
    
    



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