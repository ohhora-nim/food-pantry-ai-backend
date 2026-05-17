# =========================================
# waste_engine.py
# AI Pantry Food Waste Intelligence Engine
# =========================================

from datetime import datetime,date

from services.food_engine import enrich_pantry_foods

# =========================================
# Waste Risk Levels
# =========================================

WASTE_LEVELS = {
    "low": {
        "min": 0,
        "max": 39
    },
    "medium": {
        "min": 40,
        "max": 69
    },
    "high": {
        "min": 70,
        "max": 100
    }
}

# =========================================
# Waste Risk Score
# =========================================

def calculate_food_waste_risk(food):
    """
    Main waste risk calculation.
    """

    risk = 0

    # =====================================
    # Expiry urgency
    # =====================================

    expiry_score = food.get("expiry_score", 0)
    risk += expiry_score * 6

    # =====================================
    # Quantity risk
    # =====================================

    quantity = food.get("quantity", 1)

    if quantity >= 5:
        risk += 15

    elif quantity >= 3:
        risk += 8

    # =====================================
    # Shelf life
    # =====================================

    shelf_life = food.get("shelf_life_days", 7)

    if shelf_life <= 5:
        risk += 20

    elif shelf_life <= 10:
        risk += 10

    # =====================================
    # Fresh foods spoil faster
    # =====================================

    processing_level = food.get("processing_level", "fresh")

    if processing_level == "fresh":
        risk += 10

    elif processing_level == "processed":
        risk += 4

    # =====================================
    # Waste-prone foods
    # =====================================

    waste_risk = food.get("waste_risk", 5)

    risk += waste_risk * 2

    return max(1, min(100, int(risk)))

# =========================================
# Waste Level
# =========================================

def get_waste_level(risk_score):
    for level, values in WASTE_LEVELS.items():
        if (values["min"] <= risk_score <= values["max"]):
            return level

    return "medium"

# =========================================
# Waste Recommendation
# =========================================

def generate_waste_recommendation(food):
    expiry_score = food.get("expiry_score", 0)
    quantity = food.get("quantity", 1)
    processing_level = food.get("processing_level", "fresh")

    # =====================================
    # Urgent expiry
    # =====================================

    if expiry_score >= 9:
        return "Use immediately to avoid waste."

    # =====================================
    # Large quantity
    # =====================================

    if quantity >= 5:
        return "Use in multiple meals this week."

    # =====================================
    # Fresh foods
    # =====================================

    if processing_level == "fresh":
        return "Prioritize fresh foods first."

    return "Store properly for longer freshness."

# =========================================
# Storage Advice
# =========================================

def generate_storage_advice(food):
    category = food.get("category", "")

    storage_map = {
        "vegetable": "Store refrigerated in crisper drawer.",
        "fruit": "Keep refrigerated after ripening.",
        "meat": "Store refrigerated and cook soon.",
        "seafood": "Keep very cold and use quickly.",
        "grain": "Store in airtight dry container.",
        "dairy": "Keep refrigerated below 4°C.",
        "protein": "Refrigerate and monitor expiry dates."
    }

    return storage_map.get(category, "Store properly for freshness.")

# =========================================
# Days Until Expiry
# =========================================

def calculate_days_left(expiry_date):
    if not expiry_date:
        return None

    if isinstance(expiry_date, str):
        expiry_date = datetime.strptime(expiry_date, "%Y-%m-%d").date()

    return (expiry_date - date.today()).days

# =========================================
# Waste Forecast Engine
# =========================================

def generate_waste_forecast(pantry_foods):
    """
    Main food waste forecast engine.
    """

    pantry_foods = enrich_pantry_foods(pantry_foods)

    if not pantry_foods:
        return empty_waste_response()

    high_risk_foods = []
    medium_risk_foods = []
    low_risk_foods = []
    total_waste_score = 0
    urgent_items = 0

    # =====================================
    # Analyze each food
    # =====================================

    for food in pantry_foods:
        waste_risk_score = (calculate_food_waste_risk(food))
        waste_level = get_waste_level(waste_risk_score)
        days_left = calculate_days_left(food.get("expiry_date"))
        food_result = {
            "name": food.get("name"),
            "category": food.get("category"),
            "quantity": food.get("quantity"),
            "expiry_date": food.get("expiry_date"),
            "days_left": days_left,
            "waste_risk_score": waste_risk_score,
            "waste_level": waste_level,
            "priority_score": food.get("priority_score"),
            "processing_level": food.get("processing_level"),
            "recommendation": generate_waste_recommendation(food),
            "storage_advice": generate_storage_advice(food)
        }

        total_waste_score += waste_risk_score

        # =================================
        # Grouping
        # =================================

        if waste_level == "high":
            high_risk_foods.append(food_result)

        elif waste_level == "medium":
            medium_risk_foods.append(food_result)

        else:
            low_risk_foods.append(food_result)

        # =================================
        # Urgent foods
        # =================================

        if food.get("expiry_score", 0) >= 8:
            urgent_items += 1

    # =====================================
    # Sort High Risk First
    # =====================================

    high_risk_foods.sort(key=lambda x: x["waste_risk_score"], reverse=True)

    medium_risk_foods.sort(key=lambda x: x["waste_risk_score"], reverse=True)

    # =====================================
    # Overall Waste Score
    # =====================================

    overall_waste_score = round(total_waste_score / len(pantry_foods), 1)

    # =====================================
    # Waste Insights
    # =====================================

    insights = generate_waste_insights(pantry_foods, overall_waste_score, urgent_items)

    # =====================================
    # Sustainability Impact
    # =====================================

    sustainability_impact = generate_sustainability_impact(
        high_risk_foods
    )

    # =====================================
    # Final Response
    # =====================================

    return {
        "overall_waste_score": overall_waste_score,
        "urgent_items": urgent_items,
        "high_risk_count": len(high_risk_foods),
        "medium_risk_count": len(medium_risk_foods),
        "low_risk_count": len(low_risk_foods),
        "high_risk_foods": high_risk_foods,
        "medium_risk_foods": medium_risk_foods,
        "low_risk_foods": low_risk_foods,
        "insights": insights,
        "sustainability_impact": sustainability_impact
    }

# =========================================
# Waste Insights
# =========================================

def generate_waste_insights(pantry_foods, overall_waste_score, urgent_items):

    insights = []

    # =====================================
    # Overall score
    # =====================================

    if overall_waste_score >= 70:
        insights.append("High food waste risk detected.")

    elif overall_waste_score >= 40:
        insights.append("Moderate waste risk in pantry.")

    else:
        insights.append("Good food waste management.")

    # =====================================
    # Urgent foods
    # =====================================

    if urgent_items >= 3:
        insights.append("Several foods need urgent use.")

    # =====================================
    # Fresh food analysis
    # =====================================

    fresh_foods = len([food for food in pantry_foods if food.get("processing_level") == "fresh"])

    if fresh_foods >= 6:
        insights.append("Plan meals around fresh ingredients first.")

    # =====================================
    # Quantity issue
    # =====================================

    bulk_foods = len([food for food in pantry_foods if food.get("quantity", 1) >= 5])

    if bulk_foods >= 3:
        insights.append("Large quantities may increase waste risk.")

    if not insights:
        insights.append("Your pantry waste risk is balanced.")

    return insights[:6]

# =========================================
# Sustainability Impact
# =========================================

def generate_sustainability_impact(high_risk_foods):

    risk_count = len(high_risk_foods)

    if risk_count == 0:
        return "Excellent sustainability performance."

    if risk_count <= 2:
        return "Small improvements can reduce food waste further."

    return "Reducing food waste can improve sustainability and save money."

# =========================================
# Empty Response
# =========================================

def empty_waste_response():
    return {
        "overall_waste_score": 0,
        "urgent_items": 0,
        "high_risk_count": 0,
        "medium_risk_count": 0,
        "low_risk_count": 0,
        "high_risk_foods": [],
        "medium_risk_foods": [],
        "low_risk_foods": [],
        "insights": [],
        "sustainability_impact":
            "No pantry data available."
    }

# =========================================
# Waste Summary
# =========================================

def generate_waste_summary(waste_data):

    if not waste_data:
        return "No waste data available."

    overall_score = waste_data.get("overall_waste_score", 0)
    urgent_items = waste_data.get("urgent_items", 0)

    if overall_score < 40:
        return "Your pantry waste risk is well controlled."

    if urgent_items >= 3:
        return "Several foods should be used soon."

    return "Monitor pantry freshness to reduce waste."