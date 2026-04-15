# app/models/report.py
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    file_path = Column(String, nullable=False)
    extracted_text = Column(Text)
    analysis = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
