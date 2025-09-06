from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.core.db import Base

class Shade(Base):
    __tablename__ = "shades"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    hex_code = Column(String(7), nullable=False)  # #RRGGBB format
    rgb_r = Column(Integer, nullable=False)
    rgb_g = Column(Integer, nullable=False)
    rgb_b = Column(Integer, nullable=False)
    undertone = Column(String, nullable=True)  # warm, cool, neutral
    category = Column(String, nullable=False)  # foundation, lipstick, eyeshadow, etc.
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    
    # Relationships
    brand = relationship("Brand", back_populates="shades")
    product = relationship("Product", back_populates="shades")
