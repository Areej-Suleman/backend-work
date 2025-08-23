from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime, func, Boolean
from sqlalchemy.orm import relationship
from app.core.db import Base
from app.models.product_ingredient import product_ingredients

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    image_url = Column(String)
    product_url = Column(String)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    brand = relationship("Brand", back_populates="products")
    user = relationship("User", back_populates="products")
    ingredients = relationship("Ingredient", secondary=product_ingredients, back_populates="products")
    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")
    reminders = relationship("Reminder", back_populates="product", cascade="all, delete-orphan")
    analyses = relationship("Analysis", back_populates="product", cascade="all, delete-orphan")

class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String, nullable=False)
    is_primary = Column(Boolean, default=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    product = relationship("Product", back_populates="images")
    user = relationship("User", back_populates="product_images")
