# app/models/page.py

from sqlalchemy import Column, Integer, String, Boolean,DateTime,func
from app.db.base import Base

class Page(Base):
    __tablename__ = "pages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False)  # like 'dashboard', 'user-management'
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    createdAt = Column(DateTime, nullable=True, default=func.now())
    updatedAt = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now())
