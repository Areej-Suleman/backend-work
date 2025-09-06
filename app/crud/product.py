from typing import Optional
from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


def get_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).offset(skip).limit(limit).all()


def get_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def get_by_brand(db: Session, brand_id: int):
    return db.query(Product).filter(Product.brand_id == brand_id).all()


def create(db: Session, product: ProductCreate) -> Product:
    """Create a product from the Pydantic ProductCreate schema.
    Ensures all non-nullable columns (category, price, brand_id, user_id) are set.
    """
    data = product.dict()
    db_product = Product(**data)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update(db: Session, product_id: int, product: ProductUpdate) -> Optional[Product]:
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        return None
    changes = product.dict(exclude_unset=True)
    for key, value in changes.items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product


def delete(db: Session, product_id: int) -> bool:
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        return False
    db.delete(db_product)
    db.commit()
    return True


def search_products(
    db: Session,
    q: Optional[str] = None,
    category: Optional[str] = None,
    brand_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
):
    qs = db.query(Product)
    if q:
        like = f"%{q}%"
        qs = qs.filter((Product.name.ilike(like)) | (Product.description.ilike(like)))
    if category:
        qs = qs.filter(Product.category == category)
    if brand_id is not None:
        qs = qs.filter(Product.brand_id == brand_id)
    if min_price is not None:
        qs = qs.filter(Product.price >= min_price)
    if max_price is not None:
        qs = qs.filter(Product.price <= max_price)
    return qs.all()
def count_all(db: Session) -> int:
    return db.query(Product).count()







