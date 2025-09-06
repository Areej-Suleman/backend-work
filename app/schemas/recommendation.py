from pydantic import BaseModel
from typing import List, Optional

class RecommendationCreate(BaseModel):
    product_ids: List[int]
    reason: str


class RecommendationRating(BaseModel):
    rating: int

class MakeupPreferences(BaseModel):
    skin_tone: Optional[str] = None
    occasion: Optional[str] = None
    style: Optional[str] = None
    budget_range: Optional[str] = None

class RecommendationFilters(BaseModel):
    category: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    brands: Optional[List[str]] = None
