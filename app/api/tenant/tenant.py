# app/crud/crud_tenant.py
from app.db.database import engine
from sqlalchemy.orm import Session
from app.models.tenant import Tenant
from app.api.tenant.schemas import TenantCreate, TenantUpdate
from fastapi import HTTPException
from sqlalchemy import MetaData
from app.services.Sales_data_service import generate_sales_data_table

def get_tenant(db: Session, tenant_id: int):
    return db.query(Tenant).filter(Tenant.id == tenant_id).first()

def get_tenants(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Tenant).offset(skip).limit(limit).all()

def create_tenant(db: Session, tenant: TenantCreate):
    existing = db.query(Tenant).filter_by(name=tenant.name).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Tenant with this name already exists."
        )
    
    db_tenant = Tenant(name=tenant.name)
    db.add(db_tenant)
    db.commit()
    db.refresh(db_tenant)

    # Create dynamic sales_data_<tenant_id> table
    metadata = MetaData()
    sales_table = generate_sales_data_table(db_tenant.id, metadata)
    metadata.create_all(bind=engine)

    return db_tenant

def update_tenant(db: Session, tenant_id: int, tenant_data: TenantUpdate):
    db_tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if db_tenant:
        db_tenant.name = tenant_data.name
        db.commit()
        db.refresh(db_tenant)
    return db_tenant

def delete_tenant(db: Session, tenant_id: int):
    db_tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if db_tenant:
        db.delete(db_tenant)
        db.commit()
    return db_tenant