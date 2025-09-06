from sqlalchemy.orm import Session
from typing import Any, Dict, List, Optional
from datetime import datetime
import json

from app.models.analysis import Analysis


def create_analysis_record(db: Session, user_id: int, image_url: str, analysis_type: str = "image_upload") -> Analysis:
    """Create a minimal analysis record to track an uploaded image for analysis."""
    record = Analysis(
        user_id=user_id,
        image_url=image_url,
        analysis_type=analysis_type,
        analysis_date=datetime.utcnow(),
        results=None,
        confidence_score=None,
        recommendations=None,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def create_analysis(db: Session, user_id: int, results: Dict[str, Any], analysis_type: str = "skin") -> Analysis:
    """Create a full analysis record with computed results."""
    record = Analysis(
        user_id=user_id,
        analysis_type=analysis_type,
        results=json.dumps(results),
        analysis_date=datetime.utcnow(),
        confidence_score=results.get("confidence_score") if isinstance(results, dict) else None,
        recommendations=json.dumps(results.get("recommendations")) if isinstance(results, dict) and results.get("recommendations") is not None else None,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_user_analyses(db: Session, user_id: int) -> List[Analysis]:
    """Return analyses for a user ordered by newest first."""
    return (
        db.query(Analysis)
        .filter(Analysis.user_id == user_id)
        .order_by(Analysis.id.desc())
        .all()
    )

def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Analysis]:
    return db.query(Analysis).offset(skip).limit(limit).all()

def count_all(db: Session) -> int:
    return db.query(Analysis).count()
