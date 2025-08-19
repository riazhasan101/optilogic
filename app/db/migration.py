# migration.py

from app.db import engine
from app.db.base import Base

# Import all models so SQLAlchemy registers them
from app.models import user, role, page, pages_roles  # Add all your model files here
def run_migrations():
    print("Running DB migration...")
    Base.metadata.create_all(bind=engine)
    print("Migration completed.")

if __name__ == "__main__":
    run_migrations()