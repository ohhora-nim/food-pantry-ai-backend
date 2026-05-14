from datetime import date
from typing import List, Dict, Optional

from pydantic import BaseModel


# ==========================================
# Pantry Food Input
# ==========================================

class FoodItem(BaseModel):
    name: str
    quantity: int
    expiry_date: date
    category: Optional[str] = ""
    processing_level: Optional[str] = ""
    nutrition_tags: Optional[List[str]] = []

# ==========================================
# Meal Ingredient
# ==========================================

class MealIngredient(BaseModel):
    name: str
    category: str
    processing_level: str
    nutrition_tags: List[str]


# ==========================================
# Meal Structure
# ==========================================

class Meal(BaseModel):
    name: str
    ingredients: List[MealIngredient]
    steps: List[str]
    reason: str
    score: float


# ==========================================
# Daily Meals
# ==========================================

class DailyMeals(BaseModel):
    breakfast: Meal
    lunch: Meal
    dinner: Meal


# ==========================================
# Weekly Plan Day
# ==========================================

class WeeklyPlanDay(BaseModel):
    day: str
    meals: DailyMeals


# ==========================================
# Grocery List
# ==========================================

class GroceryItem(BaseModel):
    name: str
    quantity: int
    category: str
    priority: str
    estimated_price: float
    nutrition_tags: List[str]
    reason: str
    meal_support: List[str]
    nutrition_score: float
    storage_tip: str

# ==========================================
# Nutrition Analytics
# ==========================================

class NutritionAnalytics(BaseModel):

    total_calories: float

    total_protein: float

    total_carbs: float

    total_fat: float

    total_fiber: float

    total_sugar: float

    total_sodium: float

    average_nutrition_score: float

    fresh_percent: float

    processed_percent: float

    ultra_processed_percent: float

    processing_insight: str

    daily_breakdown: List[Dict]


# ==========================================
# Waste Forecast
# ==========================================

class WasteForecastItem(BaseModel):
    name: str
    days_left: int
    risk_level: str
    recommendation: str


# ==========================================
# Budget Analysis
# ==========================================

class BudgetAnalysis(BaseModel):

    estimated_savings: float

    waste_reduction_percent: float

    budget_score: float

    monthly_projection: float

    high_value_foods: List[str]

    waste_risk_foods: List[str]

    optimization_tips: List[str]

    shopping_strategy: str

    summary: str


# ==========================================
# Health Coaching
# ==========================================

class HealthCoaching(BaseModel):

    health_score: float

    strengths: List[str]

    risks: List[str]

    recommendations: List[str]

    nutrition_focus: str

    fitness_tip: str

    longevity_tip: str

    hydration_tip: str

    meal_balance_feedback: str

    summary: str


# ==========================================
# Recommended Foods
# ==========================================

class RecommendedFood(BaseModel):
    name: str
    category: str
    nutrition_score: float
    priority_score: float
    processing_level: str
    nutrition_tags: List[str]
    reason: str
    benefits: List[str]


class MealPlanRequest(BaseModel):
    foods: List[FoodItem]


# ==========================================
# Meal Plan Response
# ==========================================

class RecommendFoodsResponse(BaseModel):
    status: str
    recommended_foods: List[RecommendedFood]


class MealPlanResponse(BaseModel):
    status: str
    weekly_plan: List[WeeklyPlanDay]
    grocery_list: List[GroceryItem]
    analytics: NutritionAnalytics
    waste_forecast: List[WasteForecastItem]
    budget_analysis: BudgetAnalysis
    health_coaching: HealthCoaching
    recommended_foods: List[RecommendedFood]