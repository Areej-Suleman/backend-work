from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.core.db import Base

class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)  # For Cloudinary, this will be the secure_url
    file_size = Column(Integer)
    file_type = Column(String(100))  # image/jpeg, image/png, etc.
    purpose = Column(String(100))    # profile photo, skin analysis, etc.
    # Cloudinary metadata
    public_id = Column(String(255))
    storage_type = Column(String(50))  # e.g., 'cloudinary' or 'local'

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="files")
