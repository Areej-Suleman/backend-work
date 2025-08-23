from sqlalchemy.orm import Session
from app.models.product import Product

def get_all(db: Session):
    return db.query(Product).all()

def get_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()