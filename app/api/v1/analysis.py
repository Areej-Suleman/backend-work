from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.core.db import get_db
from app import crud, schemas
from app.services.skin_analysis import SkinAnalysisService
from app.services.shade_matcher import ShadeMatcherService

router = APIRouter()

@router.post("/analyze")
def analyze_user_profile(data: schemas.AnalysisRequest, db: Session = Depends(get_db)):
    skin_service = SkinAnalysisService()
    result = skin_service.analyze_skin(data.dict())
    
    # Save analysis to database
    analysis_record = crud.analysis.create_analysis(db, data.user_id, result)
    return {"analysis": result, "analysis_id": analysis_record.id}

@router.post("/skin-analysis")
async def analyze_skin_image(
    user_id: int,
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not image.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    skin_service = SkinAnalysisService()
    analysis_result = await skin_service.analyze_skin_from_image(image)
    
    # Save analysis
    analysis_data = schemas.AnalysisRequest(
        user_id=user_id,
        skin_type=analysis_result.get('skin_type'),
        concerns=analysis_result.get('concerns', [])
    )
    analysis_record = crud.analysis.create_analysis(db, user_id, analysis_result)
    
    return {"analysis": analysis_result, "analysis_id": analysis_record.id}

@router.post("/shade-match")
async def match_shade(
    user_id: int,
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    shade_service = ShadeMatcherService()
    shade_matches = await shade_service.find_matching_shades(image)
    
    return {"shade_matches": shade_matches, "user_id": user_id}

@router.get("/{user_id}/history")
def get_analysis_history(user_id: int, db: Session = Depends(get_db)):
    analyses = crud.analysis.get_user_analyses(db, user_id)
    return {"analyses": analyses}
