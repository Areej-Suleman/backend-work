from sqlalchemy.orm import Session
from app.models.file import File
from typing import Optional, Dict

def create_file(db: Session, user_id: int, data: Dict) -> File:
    """Create a File DB record from upload data.
    Expected keys in data: filename, original_filename, file_path, file_size,
    file_type, purpose, public_id, storage_type
    """
    file_row = File(
        user_id=user_id,
        filename=data.get("filename"),
        original_filename=data.get("original_filename"),
        file_path=data.get("file_path"),
        file_size=data.get("file_size"),
        file_type=data.get("file_type"),
        purpose=data.get("purpose"),
        public_id=data.get("public_id"),
        storage_type=data.get("storage_type"),
    )
    db.add(file_row)
    db.commit()
    db.refresh(file_row)
    return file_row


def delete_by_public_id(db: Session, public_id: str) -> int:
    """Delete file records by Cloudinary public_id. Returns number deleted."""
    q = db.query(File).filter(File.public_id == public_id)
    count = 0
    for row in q.all():
        db.delete(row)
        count += 1
    if count:
        db.commit()
    return count
