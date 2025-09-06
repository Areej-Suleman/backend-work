from sqlalchemy import Table, Column, Integer, ForeignKey
from app.core.db import Base

product_ingredients = Table(
    "product_ingredients",
    Base.metadata,
    Column("product_id", Integer, ForeignKey("products.id"), primary_key=True),
    Column("ingredient_id", Integer, ForeignKey("ingredients.id"), primary_key=True)
)
