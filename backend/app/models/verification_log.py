from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database.db import Base

class VerificationLog(Base):
    __tablename__ = "verification_logs"

    id = Column(Integer, primary_key=True, index=True)
    qr_id = Column(Integer, ForeignKey("qr_codes.id"), nullable=True)
    result = Column(String, nullable=False)
    ip_address = Column(String, nullable=True)
    scanned_at = Column(DateTime(timezone=True), server_default=func.now())