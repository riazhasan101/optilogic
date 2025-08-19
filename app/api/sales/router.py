# app/api/sales/router.py

from fastapi import APIRouter, UploadFile, File, Depends,HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.api.auth.dependencies import get_current_active_user
from app.api.sales.sales import import_sales_csv
from app.ml.data_preparation import prepare_sales_data_from_db

router = APIRouter(prefix="/sales", tags=["Sales"])

@router.post("/upload/")
async def upload_sales_data_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return await import_sales_csv(file, db, current_user)

@router.get("/analyze/")
def analyze_sales_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    try:
        tenant_id = current_user.tenant_id  # Use current user's tenant
        cleaned_data = prepare_sales_data_from_db(tenant_id, db)
        return {
            "message": f"Sales data for tenant {tenant_id} processed.",
            "rows": len(cleaned_data),
            "data": cleaned_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# app/api/sales/router.py

from app.ml.forecasting import forecast_sales_by_category,forecast_sales_by_category_db

@router.get("/forecast/")
def forecast_category_sales(
    category: str,
    months: int = 6,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    try:
        forecast = forecast_sales_by_category_db(
            tenant_id=current_user.tenant_id,
            category=category,
            db=db,
            periods=months
        )
        return {
            "category": category,
            "forecast_months": months,
            "predictions": forecast
        }
    except Exception as e:
        raise RuntimeError(f"Forecasting failed: {e}")
