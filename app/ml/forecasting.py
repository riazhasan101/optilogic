# app/ml/forecasting.py
import logging
from fastapi import HTTPException
import pandas as pd
from prophet import Prophet
from sqlalchemy.orm import Session
from sqlalchemy import text

# app/ml/forecasting.py

from prophet import Prophet
from sqlalchemy.orm import Session
from app.ml.data_preparation import prepare_sales_data_from_db
import pandas as pd

def forecast_sales_by_category(tenant_id: int, category: str, db: Session, periods: int = 6):
    try:
        # Use cleaned & prepared data from existing logic
        monthly_sales = prepare_sales_data_from_db(tenant_id, db)

        # Convert to DataFrame
        df = pd.DataFrame(monthly_sales)

        # Filter for category
        df = df[df['Category'] == category]

        if df.empty:
            raise ValueError(f"No sales data found for category: {category}")

        # Prophet expects columns: ds = datetime, y = value
        prophet_df = df.rename(columns={
            "Month": "ds",
            "total_qty": "y"
        })[['ds', 'y']]

        model = Prophet()
        model.fit(prophet_df)

        future = model.make_future_dataframe(periods=periods, freq='M')
        forecast = model.predict(future)

        result = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(periods)
        return result.to_dict(orient="records")

    except Exception as e:
        raise RuntimeError(f"Forecasting failed: {e}")

def forecast_sales_by_category_db(tenant_id: int, category: str, db: Session, periods: int = 6):
    table_name = f"sales_data_{tenant_id}"
    
    query = text(f"""
        SELECT "SalesDate", "Category", "SaleQty"
        FROM {table_name}
        WHERE "Category" = :category
    """)
    df = pd.read_sql(query, db.bind, params={"category": category})

    if df.empty:
        raise HTTPException(status_code=400, detail="No sales data found")

    df = df[df['Category'].str.lower() == category.lower()]
    if df.empty:
        raise HTTPException(status_code=400, detail=f"No data found for category '{category}'")

    df = df[['SalesDate', 'SaleQty']].dropna()
    # Ensure SaleQty is numeric, coerce errors to NaN
    df['SaleQty'] = pd.to_numeric(df['SaleQty'], errors='coerce')
    if df.shape[0] < 2:
        raise HTTPException(status_code=400, detail="Not enough data points to forecast")
    # Convert date
    df['SalesDate'] = pd.to_datetime(df['SalesDate'], errors='coerce')
    # Monthly aggregation
    df['Month'] = df['SalesDate'].dt.to_period('M').dt.to_timestamp()
    grouped = df.groupby('Month')['SaleQty'].sum().reset_index()
    grouped = grouped.rename(columns={'Month': 'ds'})  # Rename for Prophet compatibility
    logging.info(f"Grouped data for category '{category}': {grouped}")
    # Prophet needs columns: 'ds' (datetime) and 'y' (numeric value)
    # Ensure 'ds' is datetime and 'y' is numeric for Prophet compatibility
    prophet_df = grouped.rename(columns={'Month': 'ds', 'SaleQty': 'y'})

    # Forecasting
    model = Prophet()
    model.fit(prophet_df)

    future = model.make_future_dataframe(periods=periods, freq='M')
    forecast = model.predict(future)

    result = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(periods)
    return result.to_dict(orient='records')