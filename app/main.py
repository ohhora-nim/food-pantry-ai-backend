from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import schemas

from .ai_services import (
    generate_structured_meals,
    generate_waste_forecast,
    generate_budget_analysis, 
    generate_health_coaching,
    generate_recommended_foods,
    generate_grocery_list
)

from .functions import (
    rank_foods,
    generate_nutrition_analytics
)

# =====================================================
# FastAPI App
# =====================================================

app = FastAPI()

# =====================================================
# CORS
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Food Pantry AI API"}


@app.post("/recommend-foods", response_model=schemas.RecommendFoodsResponse)
def rcommend_foods():
    return {
        "status": "success",
        "recommended_foods": generate_recommended_foods()
    }


@app.post("/meal-plan", response_model=schemas.MealPlanResponse)
def create_meal_plan(payload: schemas.MealPlanRequest):

    # =============================================
    # payload.foods
    # contains foods from frontend
    # =============================================

    ranked_foods = rank_foods(payload.foods)
    weekly_plan = generate_structured_meals(ranked_foods)
    analytics = generate_nutrition_analytics(weekly_plan)
    recommendations = generate_recommended_foods()
    
    return {
        "status": "success",
        "weekly_plan": weekly_plan,
        "grocery_list": generate_grocery_list(weekly_plan, recommendations, ranked_foods),
        "analytics": analytics,
        "waste_forecast": generate_waste_forecast(ranked_foods, weekly_plan),
        "budget_analysis": generate_budget_analysis(ranked_foods),
        "health_coaching": generate_health_coaching(analytics, ranked_foods, weekly_plan),
        "recommended_foods": recommendations
    }