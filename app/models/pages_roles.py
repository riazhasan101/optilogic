# app/models/pages_roles.py

from sqlalchemy import Column, Integer, ForeignKey, Table
from app.db.base import Base

class PageRole(Base):
    __tablename__ = "pages_roles"

    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(Integer, ForeignKey("pages.id", ondelete="CASCADE"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
