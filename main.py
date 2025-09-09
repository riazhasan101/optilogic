# main.py (clean version)
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.db.database import create_db_and_tables
import logging
from app.api.tenant import router as tenant_router
from app.api.users import router as user_router
from app.api.sales import router as sales_router
from app.api.auth import auth

# Define lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        create_db_and_tables()
        logger.info("Database connected and tables created.")
        yield
    except Exception as e:
        logger.error(f"Error during database initialization: {e}")
        raise

# Create FastAPI instance
app = FastAPI(
    title="Optilogic API",
    description="An API for managing tenants, users, authentication, and sales forecasting.",
    version="1.0.0",
    lifespan=lifespan
)

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Include API routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(tenant_router.router, tags=["tenant"])
app.include_router(user_router.router, tags=["user"])
app.include_router(sales_router.router, tags=["sales"])

# Root endpoint
@app.get("/")
async def read_root():
    return {"message": "Welcome to Optilogic API2!"}


# to run with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)