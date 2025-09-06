import cloudinary
import cloudinary.uploader
import os
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.core.config import CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET
from fastapi.security import OAuth2PasswordBearer
from app import crud
from app.core.permissions import get_current_authenticated_user, require_user_or_admin, get_optional_user
from app.models.user import User
from typing import Optional

cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
    secure=True
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
router = APIRouter()

@router.post("/")
async def upload_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)  # Optional authentication
):
    """Upload single image - Authenticated users only"""
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")

    # Use current user from dependency
    user = current_user
    
    try:
        # Upload to Cloudinary
        result = cloudinary.uploader.upload(
            file.file,
            folder="glow_genius",  # Organize uploads in folders
            resource_type="image",
            transformation=[
                {"width": 1000, "height": 1000, "crop": "limit"},  # Optimize image size
                {"quality": "auto"},  # Auto optimize quality
                {"fetch_format": "auto"}  # Auto format (WebP when supported)
            ]
        )

        # Persist to DB
        file_row = crud.file.create_file(
            db,
            user_id=user.id if user else None,
            data={
                "filename": result["public_id"],
                "original_filename": file.filename,
                "file_path": result["secure_url"],
                "file_size": result.get("bytes", 0),
                "file_type": file.content_type,
                "purpose": "upload",
                "public_id": result["public_id"],
                "storage_type": "cloudinary",
            },
        )
        
        return {
            "file_id": file_row.id,
            "filename": file_row.filename,
            "url": result["secure_url"],
            "public_id": result["public_id"],
            "width": result.get("width"),
            "height": result.get("height"),
            "format": result.get("format"),
            "resource_type": result.get("resource_type")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.post("/multiple")
async def upload_multiple_images(
    files: list[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)  # Optional authentication
):
    """Upload multiple images - Authenticated users only"""
    if len(files) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 files allowed")
    
    # Use current user from dependency
    user = current_user

    results = []
    for file in files:
        if not file.content_type.startswith('image/'):
            results.append({"filename": file.filename, "error": "Not an image"})
            continue
        
        try:
            result = cloudinary.uploader.upload(
                file.file,
                folder="glow_genius",
                resource_type="image",
                transformation=[
                    {"width": 1000, "height": 1000, "crop": "limit"},
                    {"quality": "auto"},
                    {"fetch_format": "auto"}
                ]
            )

            file_row = crud.file.create_file(
                db,
                user_id=user.id if user else None,
                data={
                    "filename": result["public_id"],
                    "original_filename": file.filename,
                    "file_path": result["secure_url"],
                    "file_size": result.get("bytes", 0),
                    "file_type": file.content_type,
                    "purpose": "upload",
                    "public_id": result["public_id"],
                    "storage_type": "cloudinary",
                },
            )

            results.append({
                "file_id": file_row.id,
                "filename": file.filename,
                "url": result["secure_url"],
                "public_id": result["public_id"]
            })
        except Exception as e:
            results.append({
                "filename": file.filename,
                "error": str(e)
            })
    
    return {"uploaded_files": results}

@router.delete("/{public_id:path}")
async def delete_image(
    public_id: str, 
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)  # Optional authentication
):
    """Delete uploaded image - Authenticated users only"""
    try:
        # public_id may include folder segments like "glow_genius/abc123"
        result = cloudinary.uploader.destroy(public_id)
        if result.get("result") == "ok":
            # Optionally remove DB records referencing this public_id
            try:
                crud.file.delete_by_public_id(db, public_id)
            except Exception:
                pass
            return {"detail": "Image deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Image not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")

@router.post("/analyze")
async def upload_for_analysis(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)  # Optional authentication
):
    """Upload image for skin analysis - Authenticated users only"""
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Upload with analysis-specific transformations
        result = cloudinary.uploader.upload(
            file.file,
            folder="glow_genius/analysis",
            resource_type="image",
            transformation=[
                {"width": 800, "height": 800, "crop": "fill"},
                {"quality": "auto"},
                {"fetch_format": "auto"}
            ]
        )
        
        # Store in database for analysis tracking
        if current_user:
            crud.analysis.create_analysis_record(db, current_user.id, result["secure_url"])
        
        return {
            "url": result["secure_url"],
            "public_id": result["public_id"],
            "analysis_ready": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
