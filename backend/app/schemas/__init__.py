from .user import UserCreate
from .product import ProductSchema
from .chat import ChatMessage
from .auth import LoginRequest  # or from .user if it's there
from .user import UserUpdate
from .recommendation import RecommendationCreate
from .reminder import ReminderCreate
from .analysis import (
    AnalysisRequest,
    SkinAnalysisResult,
    HairAnalysisResult,
    MakeupAnalysisResult,
    RecommendationRequest,
    ProductRecommendation
)