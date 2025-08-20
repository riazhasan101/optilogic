# app/ml/data_preparation.py

import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import text

def prepare_sales_data_from_db(tenant_id: int, db: Session):
    table_name = f"sales_data_{tenant_id}"

    try:
        # Load data from tenant-specific table using raw SQL
        query = text(f"SELECT * FROM {table_name}")
        df = pd.read_sql(query, db.bind)

        # Clean and transform as before
        df['SalesDate'] = pd.to_datetime(df['SalesDate'], errors='coerce')
        df = df.dropna(subset=['SalesDate', 'Category', 'SaleQty'])

        df['SaleQty'] = pd.to_numeric(df['SaleQty'], errors='coerce').fillna(0)
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce').fillna(0)
        df['Month'] = df['SalesDate'].dt.to_period('M')

        # Group by Month, Category, StoreName
        monthly_sales = df.groupby(['Month', 'Category', 'StoreName']) \
                          .agg(total_qty=('SaleQty', 'sum'),
                               avg_price=('Price', 'mean')) \
                          .reset_index()

        return monthly_sales.to_dict(orient="records")

    except Exception as e:
        raise ValueError(f"Error processing tenant sales data: {str(e)}")
