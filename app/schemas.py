# =========================================
# Schemas
# =========================================

from pydantic import BaseModel
from typing import List
from datetime import date


class PantryFood(BaseModel):
    name: str
    quantity: int
    expiry_date: date


class PantryRequest(BaseModel):
    pantry_foods: List[PantryFood]