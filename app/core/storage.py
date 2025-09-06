import os
import uuid
from typing import Optional
from fastapi import UploadFile
import aiofiles
from pathlib import Path
import cloudinary
import cloudinary.uploader
from app.core.config import CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET

cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
    secure=True
)

class StorageService:
    def __init__(self, upload_dir: str = "uploads", use_cloudinary: bool = True):
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(exist_ok=True)
        self.use_cloudinary = use_cloudinary and all([CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET])
        
        # Create subdirectories for local storage
        (self.upload_dir / "images").mkdir(exist_ok=True)
        (self.upload_dir / "profiles").mkdir(exist_ok=True)
        (self.upload_dir / "products").mkdir(exist_ok=True)
        (self.upload_dir / "brands").mkdir(exist_ok=True)

    async def save_file(self, file: UploadFile, subfolder: str = "images") -> dict:
        """Save uploaded file and return file info"""
        if self.use_cloudinary:
            return await self._save_to_cloudinary(file, subfolder)
        else:
            return await self._save_locally(file, subfolder)
    
    async def _save_to_cloudinary(self, file: UploadFile, subfolder: str) -> dict:
        """Save file to Cloudinary"""
        try:
            result = cloudinary.uploader.upload(
                file.file,
                folder=f"glow_genius/{subfolder}",
                resource_type="auto",
                transformation=[
                    {"width": 1000, "height": 1000, "crop": "limit"},
                    {"quality": "auto"},
                    {"fetch_format": "auto"}
                ]
            )
            
            return {
                "filename": result["public_id"],
                "original_filename": file.filename,
                "file_path": result["secure_url"],
                "file_size": result.get("bytes", 0),
                "content_type": file.content_type,
                "public_id": result["public_id"],
                "width": result.get("width"),
                "height": result.get("height"),
                "format": result.get("format"),
                "storage_type": "cloudinary"
            }
        except Exception as e:
            # Fallback to local storage if Cloudinary fails
            return await self._save_locally(file, subfolder)
    
    async def _save_locally(self, file: UploadFile, subfolder: str) -> dict:
        """Save file locally (fallback method)"""
        # Generate unique filename
        file_extension = file.filename.split(".")[-1] if "." in file.filename else ""
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        
        # Create file path
        file_path = self.upload_dir / subfolder / unique_filename
        
        # Save file
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        return {
            "filename": unique_filename,
            "original_filename": file.filename,
            "file_path": str(file_path),
            "file_size": len(content),
            "content_type": file.content_type,
            "storage_type": "local"
        }

    def delete_file(self, file_path: str, public_id: str = None) -> bool:
        """Delete file from storage"""
        if self.use_cloudinary and public_id:
            try:
                cloudinary.uploader.destroy(public_id)
                return True
            except Exception:
                pass
        
        # Local file deletion
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
        except Exception:
            pass
        return False

    def get_file_url(self, file_path: str) -> str:
        """Get URL for accessing file"""
        if file_path.startswith("http"):
            return file_path  # Already a full URL (Cloudinary)
        return f"/static/{file_path.replace(str(self.upload_dir) + '/', '')}"

# Global storage instance
storage = StorageService()
