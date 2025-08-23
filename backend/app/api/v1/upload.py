import cloudinary
import cloudinary.uploader
import os

cloudinary.config(secure=True)

from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db

router = APIRouter()

@router.post("/")
def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    result = cloudinary.uploader.upload(file.file)
    return {"url": result["secure_url"]}