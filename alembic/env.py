from logging.config import fileConfig
import os
import sys
from app.core.config import settings
from sqlalchemy import engine_from_config, pool
from alembic import context

# Add the base directory to sys.path
# sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "app")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.config import settings
from app.db.base import Base
from app.models import user, role, tenant, page, pages_roles  # import all models

# Alembic Config object
config = context.config

# Load logging config
fileConfig(config.config_file_name)

# Inject database URL dynamically
config.set_main_option("sqlalchemy.url", settings.SQLALCHEMY_DATABASE_URI)

# Set target metadata
target_metadata = Base.metadata

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()
