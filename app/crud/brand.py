from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.brand import Brand, BrandImage
from app.schemas.brand import BrandCreate, BrandUpdate, BrandImageCreate

# Canonical CRUD functions

def get_brand(db: Session, brand_id: int) -> Optional[Brand]:
    return db.query(Brand).filter(Brand.id == brand_id).first()

def get_brand_by_name(db: Session, name: str) -> Optional[Brand]:
    return db.query(Brand).filter(Brand.name == name).first()

def get_brands(db: Session, skip: int = 0, limit: int = 100) -> List[Brand]:
    return db.query(Brand).offset(skip).limit(limit).all()

def create_brand(db: Session, brand: BrandCreate) -> Brand:
    # NOTE: Brand model requires user_id. Ensure your BrandCreate includes user_id
    # or set it in the API layer before calling this function.
    db_brand = Brand(**brand.dict())
    db.add(db_brand)
    db.commit()
    db.refresh(db_brand)
    return db_brand

def update_brand(db: Session, brand_id: int, brand: BrandUpdate) -> Optional[Brand]:
    db_brand = db.query(Brand).filter(Brand.id == brand_id).first()
    if db_brand:
        for key, value in brand.dict(exclude_unset=True).items():
            setattr(db_brand, key, value)
        db.commit()
        db.refresh(db_brand)
    return db_brand

def delete_brand(db: Session, brand_id: int) -> bool:
    db_brand = db.query(Brand).filter(Brand.id == brand_id).first()
    if db_brand:
        db.delete(db_brand)
        db.commit()
        return True
    return False

# Aliases expected by API routers

def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Brand]:
    return get_brands(db, skip, limit)

def get_by_id(db: Session, brand_id: int) -> Optional[Brand]:
    return get_brand(db, brand_id)

def create(db: Session, brand: BrandCreate) -> Brand:
    return create_brand(db, brand)

def update(db: Session, brand_id: int, brand: BrandUpdate) -> Optional[Brand]:
    return update_brand(db, brand_id, brand)

def delete(db: Session, brand_id: int) -> bool:
    return delete_brand(db, brand_id)

def add_image(db: Session, brand_id: int, image: BrandImageCreate) -> BrandImage:
    db_brand = get_brand(db, brand_id)
    if not db_brand:
        raise ValueError("Brand not found")
    img = BrandImage(
        image_url=image.image_url,
        is_primary=image.is_primary,
        brand_id=brand_id,
        user_id=db_brand.user_id,
    )
    db.add(img)
    db.commit()
    db.refresh(img)

def count_all(db: Session) -> int:
    return db.query(Brand).count()
