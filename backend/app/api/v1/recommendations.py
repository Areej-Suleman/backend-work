from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app import crud, schemas

router = APIRouter()

@router.get("/{user_id}")
def get_saved_recommendations(user_id: int, db: Session = Depends(get_db)):
    saved = crud.recommendations.get_for_user(db, user_id)
    if not saved:
        raise HTTPException(status_code=404, detail="No saved recommendations")
    return saved

@router.post("/{user_id}")
def save_recommendation(user_id: int, rec: schemas.RecommendationCreate, db: Session = Depends(get_db)):
    return crud.recommendations.save(db, user_id, rec)