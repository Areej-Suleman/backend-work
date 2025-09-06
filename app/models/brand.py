from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.db import Base


class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text)
    country = Column(String)
    website = Column(String)
    is_international = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # ✅ ForeignKey to link each brand to a user (brand owner / creator)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # ✅ Relationships
    user = relationship("User", back_populates="brands")
    images = relationship("BrandImage", back_populates="brand", cascade="all, delete-orphan")
    products = relationship("Product", back_populates="brand", cascade="all, delete-orphan")


class BrandImage(Base):
    __tablename__ = "brand_images"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String, nullable=False)
    is_primary = Column(Boolean, default=False)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # ✅ Relationships
    brand = relationship("Brand", back_populates="images")
    user = relationship("User", back_populates="brand_images")
