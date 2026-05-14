from datetime import date
from .ai_services import classify_food

# ============================
# Main
# ============================

def rank_foods(foods):
    ranked = []

    for food in foods:
        enriched = enrich_food(food)

        expiry_score = calculate_expiry_score(enriched["expiry_date"])

        enriched["expiry_score"] = (expiry_score)

        # ============================
        # Processing Penalty
        # ============================

        processing_penalty = 0

        if enriched["processing_level"] == "ultra_processed":
            processing_penalty = -5
        elif enriched["processing_level"] == "processed":
            processing_penalty = -2

        # ============================
        # Priority Score
        # ============================

        priority_score = enriched["nutrition_score"] * 2 + expiry_score * 2 + processing_penalty

        enriched["priority_score"] = round(priority_score, 1)

        ranked.append(enriched)

    ranked.sort(key=lambda x: x["priority_score"], reverse=True)

    return ranked


def generate_nutrition_analytics(weekly_plan):

    # ====================================
    # Totals
    # ====================================

    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0

    total_fiber = 0
    total_sugar = 0
    total_sodium = 0

    nutrition_scores = []

    # ====================================
    # Processing Counters
    # ====================================

    fresh_count = 0
    processed_count = 0
    ultra_processed_count = 0

    # ====================================
    # Daily Breakdown
    # ====================================

    daily_breakdown = []

    # ====================================
    # Iterate Days
    # ====================================

    for day in weekly_plan:

        meals = day.get("meals", {})

        # ================================
        # Daily Totals
        # ================================

        day_calories = 0
        day_protein = 0
        day_carbs = 0
        day_fat = 0

        day_fiber = 0
        day_sugar = 0
        day_sodium = 0

        # ================================
        # Iterate Meals
        # ================================

        for m in ['breakfast', 'lunch', 'dinner']:
            meal = meals[m]
            
            ingredients = meal.get(
                "ingredients",
                []
            )

            # ============================
            # Meal Nutrition Estimates
            # ============================

            meal_calories = 0
            meal_protein = 0
            meal_carbs = 0
            meal_fat = 0

            meal_fiber = 0
            meal_sugar = 0
            meal_sodium = 0

            # ============================
            # Ingredient Analysis
            # ============================

            for ingredient in ingredients:

                tags = ingredient.get(
                    "nutrition_tags",
                    []
                )

                # ========================
                # Protein
                # ========================

                if "protein" in tags:

                    meal_protein += 15
                    meal_calories += 120

                # ========================
                # Carbs
                # ========================

                if "carb" in tags:

                    meal_carbs += 20
                    meal_calories += 80

                # ========================
                # Fat
                # ========================

                if "fat" in tags:

                    meal_fat += 10
                    meal_calories += 90

                # ========================
                # Fiber
                # ========================

                if "fiber" in tags:

                    meal_fiber += 5

                # ========================
                # Sugar
                # ========================

                if "sugar" in tags:

                    meal_sugar += 8

                # ========================
                # Sodium Estimation
                # ========================

                processing_level = ingredient.get(
                    "processing_level",
                    "fresh"
                )

                if processing_level == "ultra_processed":

                    meal_sodium += 800

                elif processing_level == "processed":

                    meal_sodium += 400

                else:

                    meal_sodium += 100

                # ========================
                # Processing Counts
                # ========================

                if processing_level == "fresh":

                    fresh_count += 1

                elif processing_level == "processed":

                    processed_count += 1

                elif processing_level == "ultra_processed":

                    ultra_processed_count += 1

            # ============================
            # Meal Score
            # ============================

            score = meal.get(
                "score",
                0
            )

            nutrition_scores.append(
                score
            )

            # ============================
            # Total Nutrition
            # ============================

            total_calories += meal_calories
            total_protein += meal_protein
            total_carbs += meal_carbs
            total_fat += meal_fat

            total_fiber += meal_fiber
            total_sugar += meal_sugar
            total_sodium += meal_sodium

            # ============================
            # Daily Totals
            # ============================

            day_calories += meal_calories
            day_protein += meal_protein
            day_carbs += meal_carbs
            day_fat += meal_fat

            day_fiber += meal_fiber
            day_sugar += meal_sugar
            day_sodium += meal_sodium

            # ============================
            # Processing Levels
            # ============================

            for ingredient in ingredients:

                processing_level = ingredient.get(
                    "processing_level",
                    "fresh"
                )

                if processing_level == "fresh":

                    fresh_count += 1

                elif processing_level == "processed":

                    processed_count += 1

                elif processing_level == "ultra_processed":

                    ultra_processed_count += 1

        # ====================================
        # Daily Breakdown
        # ====================================

        daily_breakdown.append({

            "day":
                day.get("day"),

            "calories":
                day_calories,

            "protein":
                day_protein,

            "carbs":
                day_carbs,

            "fat":
                day_fat,

            "fiber":
                day_fiber,

            "sugar":
                day_sugar,

            "sodium":
                day_sodium
        })

    # ====================================
    # Average Nutrition Score
    # ====================================

    average_nutrition_score = 0

    if nutrition_scores:

        average_nutrition_score = round(

            sum(nutrition_scores) /
            len(nutrition_scores),

            1
        )

    # ====================================
    # Processing Percentages
    # ====================================

    total_processing = (

        fresh_count +
        processed_count +
        ultra_processed_count
    )

    if total_processing == 0:

        fresh_percent = 0
        processed_percent = 0
        ultra_processed_percent = 0

    else:

        fresh_percent = round(
            (fresh_count / total_processing) * 100,
            1
        )

        processed_percent = round(
            (processed_count / total_processing) * 100,
            1
        )

        ultra_processed_percent = round(
            (ultra_processed_count / total_processing) * 100,
            1
        )

    # ====================================
    # AI Processing Insight
    # ====================================

    if ultra_processed_percent >= 40:

        processing_insight = (

            "High ultra-processed food intake detected. "
            "Increase fresh vegetables, fruits, and "
            "whole foods for better health outcomes."
        )

    elif fresh_percent >= 70:

        processing_insight = (

            "Excellent fresh food balance detected. "
            "Your meals strongly emphasize nutritious "
            "whole foods and lower processing levels."
        )

    else:

        processing_insight = (

            "Balanced food processing levels detected. "
            "Reducing processed foods slightly could "
            "improve overall nutrition quality."
        )

    # ====================================
    # Fiber Insight
    # ====================================

    fiber_insight = ""

    if total_fiber < 25:

        fiber_insight = (

            "Fiber intake appears low. "
            "Consider adding beans, oats, fruits, "
            "and vegetables."
        )

    else:

        fiber_insight = (

            "Fiber intake looks healthy."
        )

    # ====================================
    # Sugar Insight
    # ====================================

    sugar_insight = ""

    if total_sugar > 100:

        sugar_insight = (

            "Sugar intake may be too high. "
            "Reducing sweetened foods could improve health."
        )

    else:

        sugar_insight = (

            "Sugar intake is within a reasonable range."
        )

    # ====================================
    # Sodium Insight
    # ====================================

    sodium_insight = ""

    if total_sodium > 2300:

        sodium_insight = (

            "High sodium intake detected. "
            "Reducing processed foods may help."
        )

    else:

        sodium_insight = (

            "Sodium intake looks balanced."
        )

    # ====================================
    # Final Analytics
    # ====================================

    analytics = {

        "total_calories":
            total_calories,

        "total_protein":
            total_protein,

        "total_carbs":
            total_carbs,

        "total_fat":
            total_fat,

        "total_fiber":
            total_fiber,

        "total_sugar":
            total_sugar,

        "total_sodium":
            total_sodium,

        "average_nutrition_score":
            average_nutrition_score,

        "daily_breakdown":
            daily_breakdown,

        "fresh_percent":
            fresh_percent,

        "processed_percent":
            processed_percent,

        "ultra_processed_percent":
            ultra_processed_percent,

        "processing_insight":
            processing_insight,

        "fiber_insight":
            fiber_insight,

        "sugar_insight":
            sugar_insight,

        "sodium_insight":
            sodium_insight
    }

    return analytics





# ============================
# Helpers
# ============================


def enrich_food(food):
    ai = classify_food(food.name)
    nutrition_score = ai["nutrition_score"]
    expiry_score = calculate_expiry_score(food.expiry_date)
    processing_penalty = 0

    if ai["processing_level"] == "ultra_processed":
        processing_penalty = -5
    elif ai["processing_level"] == "processed":
        processing_penalty = -2

    priority_score = nutrition_score * 2 + expiry_score * 2 + processing_penalty

    return {
        "name": food.name,
        "quantity": food.quantity,
        "expiry_date": food.expiry_date,
        "category": ai["category"],
        "processing_level": ai["processing_level"],
        "nutrition_tags": ai["nutrition_tags"],
        "nutrition_score": nutrition_score,
        "expiry_score": expiry_score,
        "priority_score": round(priority_score, 1)
    }


def calculate_expiry_score(expiry_date):
    """
    Higher score = should be used sooner
    """

    if not expiry_date:
        return 1

    days_left = (expiry_date - date.today()).days

    if days_left <= 0:
        return 12
    elif days_left <= 1:
        return 10
    elif days_left <= 3:
        return 7
    elif days_left <= 7:
        return 4
    else:
        return 1
