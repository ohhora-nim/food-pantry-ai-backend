import os
import json
import math


# Get the absolute path to the parent directory
PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Mock USDA FoodData Central / Open Food Facts data

TOTAL_RECIPES_IN_DB = 1000


# ==========================================
# SCORING ALGORITHMS
# ==========================================

def calculate_nutrition_score(item, nutrition_db):
    """
    Calculates a simple Nutrient Rich Foods (NRF) index.
    Rewards protein and fiber; penalizes high sodium and sugar.
    Returns a normalized score out of 100.
    """
    data = nutrition_db.get(item)
    if not data:
        return 50.0  # Baseline default
    
    # 1. Define standard Reference Daily Values (DV) for normalization
    DV = {
        "protein": 50.0,       # grams
        "fiber": 28.0,         # grams
        "potassium": 4700.0,   # milligrams
        "calcium": 1300.0,     # milligrams
        "vitamin_c": 90.0,     # milligrams
        "sugar": 50.0,         # grams (added sugar limit baseline)
        "sodium": 2300.0,      # milligrams
        "saturated_fat": 20.0  # grams
    }
    
    # 2. Calculate Positive Nutrient Density Index
    # Each term represents the fraction of the daily value met per serving
    pos_protein = data.get("protein", 0) / DV["protein"]
    pos_fiber = data.get("fiber", 0) / DV["fiber"]
    pos_potassium = data.get("potassium", 0) / DV["potassium"]
    pos_calcium = data.get("calcium", 0) / DV["calcium"]
    pos_vit_c = data.get("vitamin", 0) / DV["vitamin_c"]
    
    # Assign weights to positive nutrients
    # Giving fiber and protein slightly higher weights for satiety and structure
    positive_score = (
        (pos_protein * 5) + 
        (pos_fiber * 5) + 
        (pos_potassium * 3) + 
        (pos_calcium * 2) + 
        (pos_vit_c * 2)
    )
    
    # 3. Calculate Negative Nutrient Impact Index
    neg_sugar = data.get("sugar", 0) / DV["sugar"]
    neg_sodium = data.get("sodium", 0) / DV["sodium"]
    
    # Assign weights to negative factors
    negative_score = (neg_sugar * 4) + (neg_sodium * 3)
    
    # 4. Final Aggregation
    # Subtracting negative impacts from positive density
    raw_score = positive_score - negative_score
    
    # Normalize to a 0-100 scale using a sigmoid-style ceiling
    normalized_score = 100 / (1 + math.exp(-0.1 * raw_score))
    return round(normalized_score, 1)


def calculate_versatility_score(freq):
    """
    Calculates versatility based on recipe database penetration.
    Returns a score out of 100.
    """

    if freq == 0:
        return 10.0
    
    # Percentage of recipes the item appears in, normalized to a 0-100 scale
    percentage = (freq / TOTAL_RECIPES_IN_DB) * 100
    # Scale logarithmically so you don't need to be in 100% of recipes to score well
    score = min(100.0, percentage * 2.2) 
    return round(score, 1)


def calculate_waste_risk(shelf_life_days, versatility_score):
    """
    Predicts waste risk (0 to 100). 
    Risk increases significantly as shelf life drops, 
    but high culinary versatility slightly mitigates risk (easier to use up quickly).
    """
    if shelf_life_days >= 180: # Long-term pantry staples
        return round(max(5.0, 15.0 - (versatility_score * 0.1)), 1)
    
    # Exponential risk curve for short shelf life items
    base_risk = 100 * math.exp(-0.05 * shelf_life_days)
    
    # Mitigate risk slightly if the item is incredibly easy to throw into any recipe
    versatility_mitigation = versatility_score * 0.15
    final_risk = max(10.0, min(95.0, base_risk - versatility_mitigation))
    
    return round(final_risk, 1)


def calculate_budget_score(cost_per_lb, median_cost=2.50):
    """
    Calculates a budget score from 0 to 100 based on price per pound.
    Lower costs yield scores closer to 100; higher costs decay toward 0.
    
    :param cost_per_lb: The price of the food per pound.
    :param median_cost: The target 'average' price baseline (default $2.50).
    """
    if cost_per_lb <= 0:
        return 100.0
        
    # Bounded rational decay formula
    score = 100 / (1 + (cost_per_lb / median_cost) ** 2)
    
    return round(score, 1)


# ==========================================
# PIPELINE INTEGRATION & EXECUTION
# ==========================================

def read_data():
    file_dir = os.path.join(PARENT_DIR, "pipeline", "data.json")
    with open(file_dir, "r") as f:
        foods = json.load(f)

    items = []
    for f in foods:
        name = f["name"]

        # Compute calculated metrics
        nutri_score = calculate_nutrition_score(name, f["nutrition"])
        versatility = calculate_versatility_score(f["recipe_frequency_per_1000"])
        waste_risk = calculate_waste_risk(f["shelf_life_days"], versatility)
        budget_score = calculate_budget_score(f["estimated_cost_per_lb_usd"])

        items.append({
            "name": name,
            "category": f["category"],
            "processing_level": "fresh",
            "nutrition_tags": [k for k, v in f["nutrition"].items()],
            "nutrition_score": nutri_score,
            "versatility_score": versatility,
            "waste_risk": waste_risk,
            "shelf_life_days": f["shelf_life_days"],
            "budget_score": budget_score
        })

    with open(os.path.join(PARENT_DIR, "data", "foods.json"), "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2)


if __name__ == "__main__":
    read_data()
