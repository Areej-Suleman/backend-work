from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app import crud, schemas

router = APIRouter()

@router.post("/analyze")
def analyze_user_profile(data: schemas.AnalysisRequest, db: Session = Depends(get_db)):
    result = crud.analysis.run(data)
    return {"analysis": result}