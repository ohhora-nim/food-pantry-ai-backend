# =========================================
# recommendation_engine.py
# AI Pantry Recommendation System
# =========================================

from collections import Counter

from .food_engine import (
    SMART_FOODS,
    calculate_priority_score,
    enrich_pantry_foods,
    generate_reason,
    generate_benefits
)

# =========================================
# Constants
# =========================================

DEFAULT_LIMIT = 5

# =========================================
# User Preference Analysis
# =========================================

def analyze_user_preferences(pantry_foods):

    """
    Analyze pantry patterns to infer:
    - favorite categories
    - nutrition focus
    - processing habits
    """

    category_counter = Counter()
    nutrition_counter = Counter()
    processing_counter = Counter()

    for food in pantry_foods:

        # categories
        category = food.get("category", "other")
        category_counter[category] += 1

        # tags
        for tag in food.get("nutrition_tags", []):
            nutrition_counter[tag] += 1

        # processing
        processing_level = food.get("processing_level", "fresh")
        processing_counter[processing_level] += 1

    return {
        "favorite_categories": [item[0] for item in category_counter.most_common(3)],
        "top_nutrition_tags": [item[0] for item in nutrition_counter.most_common(5)],
        "processing_habits": dict(processing_counter)
    }

# =========================================
# Recommendation Scoring
# =========================================

def calculate_recommendation_score(food, pantry_foods, preferences):

    """
    Smart recommendation score.
    """

    score = calculate_priority_score(food)

    # =====================================
    # Category preference boost
    # =====================================

    favorite_categories = preferences.get("favorite_categories", [])

    if food.get("category") in favorite_categories:
        score += 8

    # =====================================
    # Nutrition preference boost
    # =====================================

    top_tags = preferences.get("top_nutrition_tags", [])
    shared_tags = len(set(food.get("nutrition_tags", [])) & set(top_tags))
    score += shared_tags * 4

    # =====================================
    # Fresh food bonus
    # =====================================

    if food.get("processing_level") == "fresh":
        score += 10

    # =====================================
    # Ultra processed penalty
    # =====================================

    if food.get("processing_level") == "ultra_processed":
        score -= 25

    # =====================================
    # Pantry diversity boost
    # =====================================

    pantry_categories = {item.get("category", "") for item in pantry_foods}

    # encourage diversity
    if food.get("category") not in pantry_categories:
        score += 6

    return max(1, min(100, int(score)))

# =========================================
# Filter Existing Foods
# =========================================

def filter_existing_foods(foods, pantry_foods

):

    pantry_names = {item.get("name", "").lower() for item in pantry_foods}

    filtered = []
    for food in foods:
        if food.get("name", "").lower() not in pantry_names:
            filtered.append(food)

    return filtered

# =========================================
# Filter Healthy Foods
# =========================================

def filter_healthy_foods(foods):
    """
    Remove unhealthy foods.
    """

    filtered = []
    for food in foods:

        # avoid ultra processed
        if food.get("processing_level") == "ultra_processed":
            continue

        # avoid low nutrition
        if food.get("nutrition_score", 0) < 5:
            continue

        filtered.append(food)

    return filtered

# =========================================
# Main Recommendation Engine
# =========================================

def generate_recommendations(pantry_foods, limit=DEFAULT_LIMIT):
    """
    Main recommendation engine.

    Fast rule-based intelligence.
    No AI required.
    """

    # =====================================
    # Enrich pantry
    # =====================================

    pantry_foods = enrich_pantry_foods(pantry_foods)

    # =====================================
    # User preference analysis
    # =====================================

    preferences = analyze_user_preferences(pantry_foods)

    # =====================================
    # Remove existing foods
    # =====================================

    candidate_foods = filter_existing_foods(SMART_FOODS, pantry_foods)

    # =====================================
    # Healthy filtering
    # =====================================

    candidate_foods = filter_healthy_foods(candidate_foods)

    # =====================================
    # Scoring
    # =====================================

    recommendations = []
    for food in candidate_foods:
        recommendation = food.copy()
        priority_score = calculate_recommendation_score(recommendation, pantry_foods, preferences)

        recommendation["priority_score"] = priority_score
        recommendation["reason"] = generate_reason(recommendation)
        recommendation["benefits"] = generate_benefits(recommendation)
        recommendations.append(recommendation)

    # =====================================
    # Sort
    # =====================================

    recommendations.sort(key=lambda x: x["priority_score"], reverse=True)

    return recommendations[:limit]

# =========================================
# Nutrition-Focused Recommendations
# =========================================

def recommend_high_protein_foods(pantry_foods, limit=5):
    recommendations = generate_recommendations(pantry_foods, limit=50)

    filtered = []
    for food in recommendations:
        if "protein" in food.get("nutrition_tags", []):
            filtered.append(food)

    return filtered[:limit]

# =========================================
# Budget-Friendly Recommendations
# =========================================

def recommend_budget_foods(pantry_foods, limit=5):
    recommendations = generate_recommendations(pantry_foods, limit=50)

    filtered = []
    for food in recommendations:
        if food.get("budget_score", 0) >= 8:
            filtered.append(food)

    filtered.sort(key=lambda x: (x["budget_score"], x["priority_score"]), reverse=True)

    return filtered[:limit]

# =========================================
# Fresh Food Recommendations
# =========================================

def recommend_fresh_foods(pantry_foods, limit=5):
    recommendations = generate_recommendations(pantry_foods, limit=50)

    filtered = []
    for food in recommendations:
        if food.get("processing_level") == "fresh":
            filtered.append(food)

    return filtered[:limit]

# =========================================
# Diversity Recommendations
# =========================================

def recommend_diverse_foods(pantry_foods, limit=5):
    """
    Recommend categories missing
    from current pantry.
    """

    pantry_categories = {food.get("category", "") for food in pantry_foods}

    recommendations = generate_recommendations(pantry_foods, limit=50)

    diverse = []
    for food in recommendations:
        if food.get("category") not in pantry_categories:
            diverse.append(food)

    return diverse[:limit]

# =========================================
# Pantry Health Score
# =========================================

def calculate_pantry_health_score(pantry_foods):
    """
    Overall pantry quality score.
    """

    if not pantry_foods:
        return 0

    pantry_foods = enrich_pantry_foods(pantry_foods)

    total_score = 0
    for food in pantry_foods:
        total_score += food.get("priority_score", 0)

    return round(total_score / len(pantry_foods), 1)

# =========================================
# Pantry Insights
# =========================================

def generate_pantry_insights(pantry_foods):
    """
    Smart pantry observations.
    """

    if not pantry_foods:
        return ["Add healthy foods to begin pantry analysis."]

    pantry_foods = enrich_pantry_foods(pantry_foods)

    insights = []

    # =====================================
    # Fresh ratio
    # =====================================

    fresh_count = len([food for food in pantry_foods if food.get("processing_level") == "fresh"])

    fresh_percent = (fresh_count / len(pantry_foods)) * 100

    if fresh_percent >= 70:
        insights.append("Excellent fresh food balance.")

    elif fresh_percent < 40:
        insights.append("Increase fresh whole foods.")

    # =====================================
    # Fiber check
    # =====================================

    fiber_count = len([food for food in pantry_foods if "fiber" in food.get("nutrition_tags", [])])

    if fiber_count < 3:
        insights.append("Add more fiber-rich foods.")

    # =====================================
    # Protein check
    # =====================================

    protein_count = len([food for food in pantry_foods if "protein" in food.get("nutrition_tags", [])])

    if protein_count < 3:
        insights.append("Increase healthy protein sources.")

    # =====================================
    # Expiry risk
    # =====================================

    urgent_foods = len([food for food in pantry_foods if food.get("expiry_score", 0) >= 8])

    if urgent_foods > 0:
        insights.append(f"{urgent_foods} foods need urgent use.")

    if not insights:
        insights.append("Your pantry looks balanced and healthy.")

    return insights[:5]