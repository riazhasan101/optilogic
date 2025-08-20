from app.db.database import engine
from sqlalchemy import MetaData
from app.models.tenant import Tenant
from sqlalchemy import Table, Column, Integer, String, DateTime, DECIMAL, MetaData
from sqlalchemy.sql import select
from sqlalchemy.orm import Session
from app.utility.dynamic_table import generate_sales_data_table 
from app.api.tenant.schemas import TenantCreate 

def generate_sales_data_table(tenant_id: int, metadata: MetaData):
    table_name = f"sales_data_{tenant_id}"
    return Table(
        table_name,
        metadata,
        Column("id", Integer, primary_key=True),
        Column("StoreName", String, nullable=False),
        Column("SalesDate", DateTime, nullable=False),
        Column("Style", String),
        Column("SKU", String, nullable=False),
        Column("SizeName", String),
        Column("ColorName", String),
        Column("InvoiceNo", String),
        Column("Category", String, nullable=False),
        Column("SubCategoryName", String),
        Column("Season", String),
        Column("Gender", String),
        Column("Price", DECIMAL, nullable=False),
        Column("SaleQty", DECIMAL, nullable=False),
        Column("DiscPercent", DECIMAL),
        Column("DiscValue", DECIMAL),
        Column("VatPercent", DECIMAL),
        Column("VatValue", DECIMAL),
        Column("NetAmountWithFrac", DECIMAL, nullable=False),
    )

def create_tenant_with_sales_table(db: Session, tenant_data: TenantCreate):
    # Step 1: Create tenant record
    tenant = Tenant(**tenant_data.dict())
    db.add(tenant)
    db.commit()
    db.refresh(tenant)

    # Step 2: Create dynamic sales_data_<tenant_id> table
    metadata = MetaData()
    sales_table = generate_sales_data_table(tenant.id, metadata)
    metadata.create_all(engine)

    return tenant


def get_sales_data_for_tenant(tenant_id: int, db: Session):
    metadata = MetaData()
    table = generate_sales_data_table(tenant_id, metadata)
    table.metadata.bind = db.bind
    return db.execute(select(table)).fetchall()