# =========================================
# nutrition_engine.py
# AI Pantry Nutrition Intelligence Engine
# =========================================

from collections import Counter
from .food_engine import enrich_pantry_foods

# =========================================
# Nutrition Tag Reference
# =========================================

NUTRITION_TAGS = [
    "protein",
    "fiber",
    "carb",
    "fat",
    "vitamin",
    "iron",
    "calcium",
    "omega3",
    "sugar",
    "sodium"
]

# =========================================
# Nutrition Goals
# =========================================

RECOMMENDED_COUNTS = {
    "protein": 5,
    "fiber": 5,
    "vitamin": 5,
    "iron": 3,
    "omega3": 2
}

# =========================================
# Processing Score
# =========================================

PROCESSING_SCORES = {
    "fresh": 100,
    "processed": 60,
    "ultra_processed": 20
}

# =========================================
# Nutrition Analytics
# =========================================

def generate_nutrition_analytics(pantry_foods):
    """
    Main nutrition analytics engine.
    """

    pantry_foods = enrich_pantry_foods(pantry_foods)

    if not pantry_foods:
        return empty_nutrition_response()

    # =====================================
    # Counters
    # =====================================

    total_nutrition_score = 0
    total_priority_score = 0
    fresh_count = 0
    processed_count = 0
    ultra_processed_count = 0
    tag_counter = Counter()
    category_counter = Counter()
    nutrition_balance = {tag: 0 for tag in NUTRITION_TAGS}

    # =====================================
    # Analyze foods
    # =====================================

    for food in pantry_foods:

        # scores
        total_nutrition_score += food.get("nutrition_score", 0)
        total_priority_score += food.get("priority_score", 0)

        # processing
        processing_level = food.get("processing_level", "fresh")

        if processing_level == "fresh":
            fresh_count += 1

        elif processing_level == "processed":
            processed_count += 1

        else:
            ultra_processed_count += 1

        # categories
        category = food.get("category", "other")

        category_counter[category] += 1

        # nutrition tags
        for tag in food.get("nutrition_tags", []):
            tag_counter[tag] += 1
            if tag in nutrition_balance:
                nutrition_balance[tag] += 1

    # =====================================
    # Totals
    # =====================================

    total_foods = len(
        pantry_foods
    )

    average_nutrition_score = round(total_nutrition_score / total_foods, 1)
    average_priority_score = round(total_priority_score / total_foods, 1)

    # =====================================
    # Processing %
    # =====================================

    fresh_percent = round(fresh_count / total_foods * 100, 1)
    processed_percent = round(processed_count / total_foods * 100, 1)
    ultra_processed_percent = round(ultra_processed_count / total_foods * 100, 1)

    # =====================================
    # Nutrition Balance
    # =====================================

    nutrition_balance_scores = {}
    for tag, count in nutrition_balance.items():
        recommended = RECOMMENDED_COUNTS.get(tag, 5)
        balance_score = min(100, int((count / recommended) * 100))
        nutrition_balance_scores[tag] = balance_score

    # =====================================
    # Top Nutrition Tags
    # =====================================

    top_tags = [
        {"tag": item[0], "count": item[1]} for item in tag_counter.most_common(5)
    ]

    # =====================================
    # Category Distribution
    # =====================================

    category_distribution = [
        {"category": item[0], "count": item[1]} for item in category_counter.items()
    ]

    # =====================================
    # Nutrition Insights
    # =====================================

    insights = generate_nutrition_insights(
        pantry_foods,
        nutrition_balance_scores,
        fresh_percent,
        ultra_processed_percent
    )

    # =====================================
    # Processing Insight
    # =====================================

    processing_insight = generate_processing_insight(
        fresh_percent,
        ultra_processed_percent
    )

    # =====================================
    # Daily Breakdown
    # =====================================

    daily_breakdown = generate_daily_breakdown(
        pantry_foods
    )

    # =====================================
    # Pantry Health Score
    # =====================================

    pantry_health_score = calculate_pantry_health_score(
        average_nutrition_score,
        fresh_percent,
        ultra_processed_percent
    )

    # =====================================
    # Final Response
    # =====================================

    return {
        "total_foods": total_foods,
        "average_nutrition_score": average_nutrition_score,
        "average_priority_score": average_priority_score,
        "pantry_health_score": pantry_health_score,
        "fresh_percent": fresh_percent,
        "processed_percent": processed_percent,
        "ultra_processed_percent": ultra_processed_percent,
        "top_tags": top_tags,
        "category_distribution": category_distribution,
        "nutrition_balance": nutrition_balance_scores,
        "processing_insight": processing_insight,
        "daily_breakdown": daily_breakdown,
        "insights": insights
    }

# =========================================
# Nutrition Insights
# =========================================

def generate_nutrition_insights(pantry_foods, nutrition_balance_scores, fresh_percent, ultra_processed_percent):

    insights = []

    # =====================================
    # Fresh foods
    # =====================================

    if fresh_percent >= 70:
        insights.append("Excellent fresh whole food balance.")

    elif fresh_percent < 40:
        insights.append("Increase fresh foods for better nutrition.")

    # =====================================
    # Ultra processed
    # =====================================

    if ultra_processed_percent >= 30:
        insights.append("Reduce ultra-processed foods.")

    # =====================================
    # Fiber
    # =====================================

    if nutrition_balance_scores.get("fiber", 0) < 50:
        insights.append("Add more fiber-rich foods.")

    # =====================================
    # Protein
    # =====================================

    if nutrition_balance_scores.get("protein", 0) < 50:
        insights.append("Increase healthy protein sources.")

    # =====================================
    # Vitamins
    # =====================================

    if nutrition_balance_scores.get("vitamin", 0) < 50:
        insights.append("Add more vitamin-rich produce.")

    # =====================================
    # Sugar
    # =====================================

    sugar_foods = len([food for food in pantry_foods if "sugar" in food.get("nutrition_tags", [])])

    if sugar_foods >= 5:
        insights.append("Monitor high sugar foods.")

    # =====================================
    # Sodium
    # =====================================

    sodium_foods = len([food for food in pantry_foods if "sodium" in food.get("nutrition_tags", [])])

    if sodium_foods >= 5:
        insights.append("Reduce high sodium foods.")

    if not insights:
        insights.append("Your pantry nutrition looks balanced.")

    return insights[:6]

# =========================================
# Processing Insight
# =========================================

def generate_processing_insight(fresh_percent, ultra_processed_percent):

    if fresh_percent >= 70:
        return "Your pantry emphasizes fresh whole foods."

    if ultra_processed_percent >= 40:
        return "Your pantry contains many ultra-processed foods."

    return "Your pantry has a moderate processing balance."

# =========================================
# Daily Breakdown
# =========================================

def generate_daily_breakdown(pantry_foods):
    """
    Simulated nutrition balance.
    """

    nutrition_score = round(sum([food.get("nutrition_score", 0) for food in pantry_foods]) / max(1, len(pantry_foods)), 1)

    return [
        {
            "day": "Mon",
            "score": nutrition_score
        },
        {
            "day": "Tue",
            "score": nutrition_score - 1
        },
        {
            "day": "Wed",
            "score": nutrition_score + 1
        },
        {
            "day": "Thu",
            "score": nutrition_score
        },
        {
            "day": "Fri",
            "score": nutrition_score + 1
        },
        {
            "day": "Sat",
            "score": nutrition_score - 1
        },
        {
            "day": "Sun",
            "score": nutrition_score
        }
    ]

# =========================================
# Pantry Health Score
# =========================================

def calculate_pantry_health_score(average_nutrition_score, fresh_percent, ultra_processed_percent):

    score = average_nutrition_score * 7 + fresh_percent * 0.3 - ultra_processed_percent * 0.2

    return max(1, min(100, round(score, 1)))

# =========================================
# Empty Response
# =========================================

def empty_nutrition_response():
    return {
        "total_foods": 0,
        "average_nutrition_score": 0,
        "average_priority_score": 0,
        "pantry_health_score": 0,
        "fresh_percent": 0,
        "processed_percent": 0,
        "ultra_processed_percent": 0,
        "top_tags": [],
        "category_distribution": [],
        "nutrition_balance": {},
        "processing_insight":
            "No nutrition data available.",
        "daily_breakdown": [],
        "insights": []
    }

# =========================================
# Nutrition Summary
# =========================================

def generate_nutrition_summary(analytics):

    if not analytics:
        return "No nutrition data available."

    health_score = analytics.get("pantry_health_score", 0)

    fresh_percent = analytics.get("fresh_percent", 0)

    if health_score >= 80:
        return "Excellent pantry nutrition quality."

    if health_score >= 60:
        return "Good pantry balance with room for improvement."

    if fresh_percent < 40:
        return "Increase fresh whole foods for better nutrition."

    return "Consider improving pantry food quality."