from sqlalchemy import Column, Integer, String, Text, Boolean, Time, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.db import Base

class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    reminder_type = Column(String(50))  # morning_routine, evening_routine, weekly, etc.
    reminder_time = Column(Time)
    frequency = Column(String(50))  # daily, weekly, monthly
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="reminders")
    product = relationship("Product", back_populates="reminders")
