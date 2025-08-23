from pydantic import BaseModel
from typing import List

class RecommendationCreate(BaseModel):
    product_ids: List[int]
    reason: str