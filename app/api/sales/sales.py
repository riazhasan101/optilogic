# app/api/sales/service.py

from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.utility.dynamic_table import generate_sales_data_table
from sqlalchemy import MetaData
import io
import pandas as pd

def bulk_insert_using_copy(file_obj, db: Session, tenant_id: int):
    table_name = f"sales_data_{tenant_id}"
    raw_connection = db.connection().connection  # psycopg2 connection

    try:
        with raw_connection.cursor() as cur:
            cur.copy_expert(
                f"""
                COPY {table_name} (
                    "StoreName", "SalesDate", "Style", "SKU", "SizeName", "ColorName",
                    "InvoiceNo", "Category", "SubCategoryName", "Season", "Gender",
                    "Price", "SaleQty", "DiscPercent", "DiscValue", "VatPercent", "VatValue",
                    "NetAmountWithFrac"
                ) FROM STDIN WITH (FORMAT CSV, HEADER TRUE)
                """,
                file_obj
            )
        raw_connection.commit()
    except Exception as e:
        raw_connection.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to insert data: {str(e)}")


async def import_sales_csv(file: UploadFile, db: Session, current_user: User):
    tenant_id = current_user.tenant_id

    # Ensure table exists
    metadata = MetaData()
    table = generate_sales_data_table(tenant_id, metadata)
    table.name = f"sales_data_{tenant_id}"
    table.create(bind=db.get_bind(), checkfirst=True)

    try:
        # Read bytes once
        csv_bytes = await file.read()

        # Count rows using pandas
        df = pd.read_csv(io.BytesIO(csv_bytes))
        row_count = len(df)

        # Rewind for COPY
        csv_stream = io.StringIO(csv_bytes.decode("utf-8"))

        # Efficient bulk insert
        bulk_insert_using_copy(csv_stream, db, tenant_id)

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Upload failed: {str(e)}")

    return {
        "tenant_id": tenant_id,
        "rows_imported": row_count,
        "message": "Sales data imported successfully"
    }
