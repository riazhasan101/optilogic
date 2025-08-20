# app/api/tenant/router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.user import User
from app.db.database import get_db
from app.api.tenant import schemas
from app.api.tenant import tenant as tenant_def
from app.api.auth.dependencies import get_current_active_superuser

router = APIRouter(prefix="/tenants", tags=["Tenants"])

@router.get("/", response_model=List[schemas.TenantOut])
def read_tenants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),current_user: User = Depends(get_current_active_superuser)): 
    return tenant_def.get_tenants(db, skip=skip, limit=limit)

@router.get("/{tenant_id}", response_model=schemas.TenantOut)
def read_tenant(tenant_id: int, db: Session = Depends(get_db),current_user: User = Depends(get_current_active_superuser)):

    tenant =tenant_def.get_tenant(db, tenant_id)
    if tenant is None:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant

@router.post("/", response_model=schemas.TenantOut)
def create_tenant(tenant: schemas.TenantCreate, db: Session = Depends(get_db),current_user: User = Depends(get_current_active_superuser)):
    return tenant_def.create_tenant(db, tenant)

@router.put("/{tenant_id}", response_model=schemas.TenantOut)
def update_tenant(tenant_id: int, tenant: schemas.TenantUpdate, db: Session = Depends(get_db),current_user: User = Depends(get_current_active_superuser)):
    return tenant_def.update_tenant(db, tenant_id, tenant)

@router.delete("/{tenant_id}", response_model=schemas.TenantOut)
def delete_tenant(tenant_id: int, db: Session = Depends(get_db),current_user: User = Depends(get_current_active_superuser)):
    return tenant_def.delete_tenant(db, tenant_id)
