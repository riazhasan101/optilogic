# app/models/role.py

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    createdAt = Column(DateTime, nullable=True, default=func.now())
    updatedAt = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now())


    # Relationships
    users = relationship("User",secondary="users_roles", back_populates="roles")
   
  