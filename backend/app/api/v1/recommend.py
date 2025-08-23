from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app import crud, schemas

router = APIRouter()

@router.post("/{user_id}")
def recommend_products(user_id: int, db: Session = Depends(get_db)):
    recommendations = crud.recommend.generate_for_user(db, user_id)
    if not recommendations:
        raise HTTPException(status_code=404, detail="No recommendations found")
    return recommendations