import os
import json
import settings
from datetime import datetime, date


FOODS_FILE = os.path.join(settings.BASE_DIR, "data", "foods.json")

with open(FOODS_FILE, "r", encoding="utf-8") as f:
    SMART_FOODS = json.load(f)


FOOD_MAP = { food["name"].lower(): food for food in SMART_FOODS }


# =========================================
# Default Values
# =========================================

DEFAULT_FOOD = {
    "category": "other",
    "processing_level": "fresh",
    "nutrition_tags": [],
    "nutrition_score": 5,
    "budget_score": 5,
    "versatility_score": 5,
    "waste_risk": 5,
    "shelf_life_days": 7,
    "sustainability_score": 5
}

# =========================================
# Helper
# =========================================

def safe_int(value, default=0):
    try:
        return int(value)
    except:
        return default

# =========================================
# Get Food Intelligence
# =========================================

def get_food_data(food_name):
    """
    Return smart food data.
    """

    if not food_name:
        return DEFAULT_FOOD.copy()

    return FOOD_MAP.get(
        food_name.lower(),
        DEFAULT_FOOD.copy()
    )

# =========================================
# Calculate Expiry Score
# =========================================

def calculate_expiry_score(expiry_date):
    """
    Higher score = more urgent.
    """

    if not expiry_date:
        return 0

    if isinstance(expiry_date, str):
        expiry_date = datetime.strptime(expiry_date, "%Y-%m-%d").date()

    today = date.today()

    days_left = (expiry_date - today).days

    # expired
    if days_left < 0:
        return 10

    # urgent
    if days_left <= 2:
        return 9

    if days_left <= 4:
        return 7

    if days_left <= 7:
        return 5

    if days_left <= 14:
        return 3

    return 1

# =========================================
# Processing Penalty
# =========================================

def get_processing_penalty(level):
    penalties = {
        "fresh": 0,
        "processed": 5,
        "ultra_processed": 15
    }

    return penalties.get(level, 0)

# =========================================
# Calculate Priority Score
# =========================================

def calculate_priority_score(food):
    """
    Unified AI priority score.
    """

    nutrition_score = safe_int(food.get("nutrition_score", 5))
    budget_score = safe_int(food.get("budget_score", 5))
    versatility_score = safe_int(food.get("versatility_score", 5))
    sustainability_score = safe_int(food.get("sustainability_score", 5))
    waste_risk = safe_int(food.get("waste_risk", 5))
    expiry_score = safe_int(food.get("expiry_score", 0))
    processing_penalty = get_processing_penalty(food.get("processing_level", "fresh"))

    score = nutrition_score * 4 + budget_score * 2 + versatility_score * 3 + sustainability_score * 2 + expiry_score * 5 + waste_risk * 2 - processing_penalty

    # normalize
    score = max(1, min(100, int(score)))

    return score

# =========================================
# Enrich Pantry Food
# =========================================

def enrich_food_item(pantry_food):
    """
    Merge pantry item with
    smart food intelligence.
    """

    food_name = pantry_food.get("name", "")

    smart_data = get_food_data(food_name)

    enriched = {**smart_data, **pantry_food}

    # expiry intelligence
    expiry_score = calculate_expiry_score(
        enriched.get("expiry_date")
    )

    enriched["expiry_score"] = expiry_score

    # processing penalty
    processing_penalty = get_processing_penalty(
        enriched.get("processing_level")
    )
    
    enriched["processing_penalty"] = processing_penalty

    # priority score
    priority_score = calculate_priority_score(enriched)
    

    enriched["priority_score"] = priority_score

    return enriched

# =========================================
# Enrich Pantry
# =========================================

def enrich_pantry_foods(pantry_foods):
    enriched = []
    for food in pantry_foods:
        enriched.append(
            enrich_food_item(food)
        )

    # auto sort
    enriched.sort(key=lambda x: x["priority_score"], reverse=True)

    return enriched

# =========================================
# Recommend Foods
# =========================================

def recommend_foods(pantry_foods=None, limit=5):

    """
    Fast AI-free recommendation engine.
    """

    pantry_foods = pantry_foods or []

    existing_names = {food.get("name", "").lower() for food in pantry_foods}

    recommendations = []
    for food in SMART_FOODS:

        # skip duplicates
        if food["name"].lower() in existing_names:
            continue

        recommendation = food.copy()
        recommendation["priority_score"] = calculate_priority_score(recommendation)
        recommendation["reason"] = generate_reason(recommendation)
        recommendation["benefits"] = generate_benefits(recommendation)
        recommendations.append(recommendation)

    recommendations.sort(key=lambda x: x["priority_score"], reverse=True)

    return recommendations[:limit]

# =========================================
# Generate Reason
# =========================================

def generate_reason(food):
    tags = food.get("nutrition_tags", [])

    reasons = []
    if "protein" in tags:
        reasons.append("high protein")

    if "fiber" in tags:
        reasons.append("high fiber")

    if food.get("processing_level") == "fresh":
        reasons.append("fresh whole food")

    if food.get("budget_score", 0) >= 8:
        reasons.append("budget friendly")

    if food.get("versatility_score", 0) >= 8:
        reasons.append("versatile ingredient")

    if not reasons:
        reasons.appnd("healthy food choice")

    return ", ".join(reasons[:3])

# =========================================
# Generate Benefits
# =========================================

def generate_benefits(food):
    benefits = []

    tags = food.get("nutrition_tags", [])

    if "protein" in tags:
        benefits.append(
            "supports muscle health"
        )

    if "fiber" in tags:
        benefits.append(
            "supports digestion"
        )

    if "vitamin" in tags:
        benefits.append(
            "supports immunity"
        )

    if "iron" in tags:
        benefits.append(
            "supports energy"
        )

    if "healthy_fat" in tags:
        benefits.append(
            "supports heart health"
        )

    if not benefits:
        benefits.append(
            "supports healthy eating"
        )

    return benefits[:3]

# =========================================
# Grocery Optimization
# =========================================

def generate_smart_grocery_list(pantry_foods, limit=10):
    """
    Fast grocery optimization.
    """

    recommendations = recommend_foods(pantry_foods,limit=limit)

    grocery_list = []
    for food in recommendations:
        grocery_item = {
            "name":food["name"],
            "quantity": 1,
            "unit": "item",
            "category": food["category"],
            "priority": "high" if food["priority_score"] >= 80 else "medium",
            "estimated_price": estimate_price(food),
            "nutrition_score": food["nutrition_score"],
            "nutrition_tags": food["nutrition_tags"],
            "reason": food["reason"],
            "storage_tip": generate_storage_tip(food)
        }

        grocery_list.append(grocery_item)

    return grocery_list

# =========================================
# Estimate Price
# =========================================

def estimate_price(food):
    category = food.get("category", "other")

    price_map = {
        "vegetable": 4,
        "fruit": 5,
        "meat": 10,
        "seafood": 12,
        "grain": 6,
        "dairy": 5,
        "protein": 8
    }

    return price_map.get(category,5)

# =========================================
# Storage Tip
# =========================================

def generate_storage_tip(food):
    category = food.get("category", "")

    tips = {
        "vegetable": "Store refrigerated in crisper drawer.",
        "fruit": "Keep refrigerated after ripening.",
        "meat": "Store refrigerated and cook soon.",
        "seafood": "Keep very cold and use quickly.",
        "grain": "Store in cool dry place.",
        "dairy": "Keep refrigerated."
    }

    return tips.get(category, "Store properly for freshness."
    )

# =========================================
# Nutrition Analytics
# =========================================

def generate_nutrition_analytics(pantry_foods):

    if not pantry_foods:
        return {
            "average_nutrition_score": 0,
            "fresh_percent": 0,
            "processed_percent": 0,
            "ultra_processed_percent": 0,
            "top_tags": []
        }

    total_score = 0

    fresh = 0
    processed = 0
    ultra = 0

    tag_counter = {}
    for food in pantry_foods:
        total_score += food.get("nutrition_score", 0)
        level = food.get("processing_level", "fresh")

        if level == "fresh":
            fresh += 1

        elif level == "processed":
            processed += 1

        else:
            ultra += 1

        for tag in food.get("nutrition_tags", []):
            tag_counter[tag] = tag_counter.get(tag, 0) + 1

    total = len(pantry_foods)

    top_tags = sorted(tag_counter.items(), key=lambda x: x[1], reverse=True)

    return {
        "average_nutrition_score": round(total_score / total, 1),
        "fresh_percent": round(fresh / total * 100, 1),
        "processed_percent": round(processed / total * 100, 1),
        "ultra_processed_percent": round(ultra / total * 100, 1),
        "top_tags": top_tags[:5]
    }