from sqlalchemy import Column, Integer, String, Text, Float, Boolean
from sqlalchemy.orm import relationship
from app.core.db import Base
from app.models.product_ingredient import product_ingredients

class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    inci_name = Column(String(255))  # International nomenclature
    category = Column(String(100))  # active, preservative, emollient, etc.
    function = Column(String(255))  # moisturizing, anti-aging, etc.
    description = Column(Text)
    benefits = Column(Text)  # JSON string of benefits
    side_effects = Column(Text)  # JSON string of potential side effects
    comedogenic_rating = Column(Integer)  # 0–5 scale
    is_natural = Column(Boolean, default=False)
    safety_score = Column(Float)  # 1–10 scale

    products = relationship("Product", secondary=product_ingredients, back_populates="ingredients")