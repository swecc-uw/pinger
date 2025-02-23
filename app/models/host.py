from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class Host(Base):
    __tablename__ = "hosts"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False)
    host = Column(String, nullable=False)
    last_check = Column(DateTime(timezone=True))
    is_up = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
