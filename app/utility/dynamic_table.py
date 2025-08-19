# app/utils/dynamic_table.py

from sqlalchemy import Table, Column, Integer, String, DateTime, DECIMAL, MetaData

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
