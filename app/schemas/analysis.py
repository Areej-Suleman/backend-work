from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class AnalysisRequest(BaseModel):
    image_base64: Optional[str] = None
    quiz_answers: Optional[Dict[str, Any]] = None
    analysis_type: str  # skin, hair, makeup

class SkinAnalysisResult(BaseModel):
    skin_type: str  # oily, dry, combination, sensitive
    skin_tone: str
    concerns: List[str]  # acne, dryness, pigmentation, etc.
    confidence_score: float

class HairAnalysisResult(BaseModel):
    hair_type: str  # straight, wavy, curly, coily
    hair_texture: str  # fine, medium, thick
    concerns: List[str]  # frizz, dandruff, thinning, etc.
    confidence_score: float

class MakeupAnalysisResult(BaseModel):
    skin_tone: str
    undertone: str  # warm, cool, neutral
    coverage_preference: str  # light, medium, full
    finish_preference: str  # matte, dewy, natural
    confidence_score: float

class RecommendationRequest(BaseModel):
    user_id: Optional[int] = None
    skin_type: Optional[str] = None
    hair_type: Optional[str] = None
    concerns: Optional[List[str]] = None
    category: Optional[str] = None
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    brand_preference: Optional[str] = None  # national, international, both

class ProductRecommendation(BaseModel):
    product_id: int
    product_name: str
    brand_name: str
    category: str
    price: Optional[float]
    image_url: Optional[str]
    product_url: Optional[str]
    match_score: float
    reason: str
