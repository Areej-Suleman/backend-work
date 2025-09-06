from dotenv import load_dotenv
import os
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    SECRET_KEY: str | None = os.getenv("SECRET_KEY", "hello1234")
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://glow_user:1234@localhost:5432/glowgenius"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # File upload settings
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB

    # ML Model settings
    MODEL_PATH: str = "ml_models"

    # Cloudinary settings
    CLOUDINARY_CLOUD_NAME: str | None = os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY: str | None = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET: str | None = os.getenv("CLOUDINARY_API_SECRET")
    CLOUDINARY_URL: str | None = os.getenv("CLOUDINARY_URL")

    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Glow Genius API"

    # Admin control
    ADMIN_EMAIL: str | None = os.getenv("ADMIN_EMAIL")
    
    # Email settings
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME: str | None = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD: str | None = os.getenv("SMTP_PASSWORD")
    FROM_EMAIL: str = os.getenv("FROM_EMAIL", "noreply@glowgenius.com")
    FROM_NAME: str = os.getenv("FROM_NAME", "GlowGenius")
    
    # Frontend URL for email links
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    
    # Email verification settings
    VERIFICATION_TOKEN_EXPIRE_HOURS: int = int(os.getenv("VERIFICATION_TOKEN_EXPIRE_HOURS", "24"))

    # Gemini API Key
    GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")

    model_config = {"case_sensitive": True}

settings = Settings()

# Keep backward compatibility
SECRET_KEY = settings.SECRET_KEY
DATABASE_URL = settings.DATABASE_URL
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
UPLOAD_DIR = settings.UPLOAD_DIR
MAX_FILE_SIZE = settings.MAX_FILE_SIZE
MODEL_PATH = settings.MODEL_PATH
CLOUDINARY_CLOUD_NAME = settings.CLOUDINARY_CLOUD_NAME
CLOUDINARY_API_KEY = settings.CLOUDINARY_API_KEY
CLOUDINARY_API_SECRET = settings.CLOUDINARY_API_SECRET
CLOUDINARY_URL = settings.CLOUDINARY_URL
API_V1_STR = settings.API_V1_STR
PROJECT_NAME = settings.PROJECT_NAME
