# app/api/tenant/schemas.py
from pydantic import BaseModel
from typing import Optional

class TenantCreate(BaseModel):
    name: str
    description: Optional[str] = None

class TenantUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class TenantOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True