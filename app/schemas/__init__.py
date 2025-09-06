from .chat import ChatMessage, SkincareAdviceRequest
from .auth import (
    LoginRequest, LoginResponse, RegisterRequest, RegisterResponse,
    ForgotPasswordRequest, ForgotPasswordResponse,
    ResetPasswordRequest, ResetPasswordResponse, EmailRequest
)
from .recommendation import RecommendationCreate, RecommendationRating
from .reminder import Reminder, ReminderCreate, ReminderUpdate

from .analysis import (
    AnalysisRequest,
    SkinAnalysisResult,
    HairAnalysisResult,
    MakeupAnalysisResult,
    RecommendationRequest,
    ProductRecommendation
)
from .user import UserCreate, UserUpdate, UserResponse
from .product import ProductSchema, ProductCreate, ProductUpdate
from .brand import BrandCreate,BrandResponse,BrandUpdate,BrandImageCreate
from .common import *

from .profile import Profile, ProfileCreate, ProfileUpdate, ProfilePreferences

from .recommendation import MakeupPreferences, RecommendationFilters
