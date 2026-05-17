# =========================================
# main.py
# AI Pantry Backend
# FastAPI + Gemma AI
# =========================================

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .schemas import PantryRequest

# =========================================
# Services
# =========================================

from services.food_engine import enrich_pantry_foods
from services.recommendation_engine import generate_recommendations
from services.nutrition_engine import generate_nutrition_analytics
from services.waste_engine import generate_waste_forecast

# =========================================
# AI Services
# =========================================

from ai.generate_meals import generate_meals
from ai.generate_summary import generate_summary
from ai.generate_coaching import generate_coaching
from ai.generate_explanations import generate_explanations

# =========================================
# FastAPI
# =========================================

app = FastAPI()

# =========================================
# CORS
# =========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# =========================================
# Root
# =========================================

@app.get("/")
def root():
    return {
        "message": "Food Pantry AI API"
    }


# =========================================
# Dashboard
# =========================================

@app.post("/dashboard")
def get_dashboard(request: PantryRequest):
    """
    Main unified dashboard endpoint.
    """

    try:
        enriched = get_enriched_pantry(request)
        nutrition = generate_nutrition_analytics(enriched)
        waste = generate_waste_forecast(enriched)
        recommendations = generate_recommendations(enriched)

        return {
            "pantry_foods": enriched,
            "nutrition": nutrition,
            "waste": waste,
            "recommendations": recommendations,

            # AI-heavy outputs are intentionally empty here.
            # Frontend should load these from localStorage
            # or request them via /ai/... endpoints.
            "meals": [],
            "coaching": "",
            "summary": ""
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================================
# ON-DEMAND AI: Meals
# This calls Gemma only when user clicks button.
# =========================================

@app.post("/ai/meals")
def generate_ai_meals(request: PantryRequest):
    
    try:
        enriched = get_enriched_pantry(request)
        if not enriched:
            return {"meals": []}

        meals = generate_meals(enriched)

        return {
            "meals": meals
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================
# ON-DEMAND AI: Coaching
# This calls Gemma only when user clicks button.
# =========================================

@app.post("/ai/coaching")
def generate_ai_coaching(request: PantryRequest):
    try:
        enriched = get_enriched_pantry(request)
        nutrition = generate_nutrition_analytics(enriched)
        waste = generate_waste_forecast(enriched)
        coaching = generate_coaching(enriched, nutrition, waste)

        return {
            "coaching": coaching
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================
# ON-DEMAND AI: Summary
# This calls Gemma only when user clicks button.
# =========================================

@app.post("/ai/summary")
def generate_ai_summary(request: PantryRequest):
    try:
        enriched = get_enriched_pantry(request)
        nutrition = generate_nutrition_analytics(enriched)
        waste = generate_waste_forecast(enriched)
        recommendations = generate_recommendations(enriched)
        summary = generate_summary(nutrition, waste, recommendations)

        return {
            "summary": summary
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================
# ON-DEMAND AI: Explanations
# This calls Gemma only when user clicks button.
# =========================================

@app.post("/ai/explanations")
def generate_ai_explanations(request: PantryRequest):
    try:
        enriched = get_enriched_pantry(request)
        recommendations = generate_recommendations(enriched)
        explained_recommendations = generate_explanations(recommendations)
    
        return {
            "recommendations": explained_recommendations
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================
# Helper: Enrich Pantry
# =========================================

def get_enriched_pantry(request: PantryRequest):
    pantry_foods = normalize_pantry_foods(request.pantry_foods)
    enriched = enrich_pantry_foods(pantry_foods)

    return enriched


def normalize_pantry_foods(pantry_foods: PantryRequest):
    normalized = []

    for food in pantry_foods:
        food_dict = food.model_dump()

        # Convert date object to string for JSON / engines
        food_dict["expiry_date"] = str(
            food_dict["expiry_date"]
        )

        normalized.append(
            food_dict
        )

    return normalized