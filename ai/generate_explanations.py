# =========================================
# explanation_ai.py
# Gemma AI Explanation Engine
# =========================================

import json
from .run_ollama import run_ai, clean_text

# =========================================
# Build Prompt
# =========================================

def build_explanation_prompt(context):
    return f"""
Task:
Explain briefly why each food is important.

Foods:
{json.dumps(context)}

Rules:
- concise
- practical
- human-friendly
- focus on nutrition and waste reduction
- max 15 words per explanation

Return JSON only.

[
  {{
    "name":"spinach",
    "explanation":"High nutrition and should be used soon."
  }}
]
"""


# =========================================
# Main Generate Explanations
# =========================================


def generate_explanations(items):

    """
    Generate short AI explanations.

    Optimized for:
    - local Gemma
    - fast inference
    - concise outputs
    """

    if not items:
        return []

    try:
        context = build_explanation_context(items)
        prompt = build_explanation_prompt(context)

        options = {
            "temperature": 0.3,
            "top_p": 0.8,
            "top_k": 20,
            "max_output_tokens": 250
        }
        content = run_ai(prompt, options)
        explanations = json.loads(content)

        if not explanations:
            explanations = generate_fallback_explanations(items)

        explanations = normalize_explanations(explanations)
        
        return merge_explanations(items, explanations)

    except Exception as e:
        print("Explanation generation error:", e)
        fallback = generate_fallback_explanations(items)
        return merge_explanations(items, fallback)


# =========================================
# Build Explanation Context
# =========================================

def build_explanation_context(items):

    """
    Keep context compact for
    fast local Gemma inference.
    """

    compact_items = []
    for item in items[:10]:
        compact_items.append({
            "name": item.get("name"),
            "category": item.get("category"),
            "nutrition_score": item.get("nutrition_score", 0),
            "priority_score": item.get("priority_score", 0),
            "expiry_score": item.get("expiry_score", 0),
            "processing_level": item.get("processing_level", "fresh"),
            "nutrition_tags": item.get("nutrition_tags", [])
        })

    return compact_items


# =========================================
# Normalize Explanations
# =========================================

def normalize_explanations(explanations):
    normalized = []
    for item in explanations:
        normalized.append({
            "name": item.get("name", ""),
            "explanation": item.get("explanation", "Healthy pantry food.")
        })

    return normalized

# =========================================
# Fallback Explanations
# =========================================

def generate_fallback_explanations(items):
    explanations = []
    for item in items:
        tags = item.get("nutrition_tags", [])
        nutrition_score = item.get("nutrition_score", 0)
        expiry_score = item.get("expiry_score", 0)

        processing_level = item.get("processing_level", "fresh")

        reasons = []

        # =================================
        # Nutrition
        # =================================

        if nutrition_score >= 8:
            reasons.append("high nutrition")

        # =================================
        # Expiry
        # =================================

        if expiry_score >= 8:
            reasons.append("use soon")

        # =================================
        # Fresh
        # =================================

        if processing_level == "fresh":
            reasons.append("fresh whole food")

        # =================================
        # Tags
        # =================================

        if "protein" in tags:
            reasons.append("high protein")

        if "fiber" in tags:
            reasons.append("high fiber")

        if not reasons:
            reasons.append("healthy pantry choice")

        explanations.append({
            "name": item.get("name", ""),
            "explanation": ", ".join(reasons[:3])
        })

    return explanations

# =========================================
# Merge Explanations
# =========================================

def merge_explanations(items, explanations):
    explanation_map = {item.get("name", "").lower(): item.get("explanation", "") for item in explanations}

    merged = []
    for item in items:
        name = item.get("name", "")
        merged_item = {**item, "explanation": explanation_map.get(name.lower(), "No explanations found.")}
        merged.append(merged_item)

    return merged
