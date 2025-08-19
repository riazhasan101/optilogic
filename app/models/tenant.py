# app/models/tenant.py

from sqlalchemy import Column, Integer, String,DateTime, func,Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base
class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    address = Column(String, nullable=True)
    isActive = Column(Boolean, default=True)
    createdAt = Column(DateTime, nullable=True, default=func.now())
    updatedAt = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now())
    users = relationship("User", back_populates="tenant")
