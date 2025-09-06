from sqlalchemy import Column, Integer, String, DateTime, func, Boolean, text
from sqlalchemy.orm import relationship
from app.core.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String)
    skin_type = Column(String)
    skin_color = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    hashed_password = Column(String, nullable=False)
    # Admin flag
    is_admin = Column(Boolean, server_default=text('false'), nullable=False)
    # Email verification fields
    is_verified = Column(Boolean, server_default=text('false'), nullable=False)
    verification_token = Column(String, nullable=True)
    verification_expires = Column(DateTime(timezone=True), nullable=True)

    # ✅ Relationships
    reminders = relationship("Reminder", back_populates="user", cascade="all, delete-orphan")
    analyses = relationship("Analysis", back_populates="user", cascade="all, delete-orphan")
    files = relationship("File", back_populates="user", cascade="all, delete-orphan")
    products = relationship("Product", back_populates="user", cascade="all, delete-orphan")
    brands = relationship("Brand", back_populates="user", cascade="all, delete-orphan")  # ✅ fixed
    brand_images = relationship("BrandImage", back_populates="user", cascade="all, delete-orphan")
    product_images = relationship("ProductImage", back_populates="user", cascade="all, delete-orphan")
    profile = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    chatbot_logs = relationship("ChatbotLog", back_populates="user", cascade="all, delete-orphan")
    clickouts = relationship("Clickout", back_populates="user", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="user", cascade="all, delete-orphan")
