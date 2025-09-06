from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.core.db import Base


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255))
    reason = Column(Text)
    filters = Column(Text)  # JSON string of filters used
    rating = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="recommendations")
    items = relationship("RecommendationItem", back_populates="recommendation", cascade="all, delete-orphan")


class RecommendationItem(Base):
    __tablename__ = "recommendation_items"

    id = Column(Integer, primary_key=True, index=True)
    recommendation_id = Column(Integer, ForeignKey("recommendations.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    score = Column(Float)
    reason = Column(Text)
    rank = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    recommendation = relationship("Recommendation", back_populates="items")
    product = relationship("Product", back_populates="recommendation_items")
