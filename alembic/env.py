import asyncio
import os
from logging.config import fileConfig
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

# Import SQLModel and your models
from sqlmodel import SQLModel

# Import all your models here to ensure they are registered with SQLModel.metadata
# This is crucial for autogenerate to work properly
from infrastructure.db.fastapi.models import *  # noqa: F401, F403

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set the SQLModel metadata as the target for autogenerate
target_metadata = SQLModel.metadata


# Configure table inclusion to avoid conflicts with Django tables
def include_name(name, type_, parent_names):
    """Include only specific tables and schemas in autogenerate."""
    if type_ == "table":
        # Only include our SQLModel tables, ignore all existing Django tables
        sqlmodel_tables = ["user"]  # Add new SQLModel table names here
        if name in sqlmodel_tables:
            return True
        # Exclude all other tables to prevent unwanted modifications
        return False
    return True


# Configure the database URL from environment variables
def get_database_url() -> str:
    """Get database URL from environment variables matching .env file."""
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    user = os.getenv("DB_USERNAME", "cartographie")  # Using DB_USERNAME from .env
    password = os.getenv("DB_PASSWORD", "123456")
    database = os.getenv("DB_NAME", "cartographie_db")

    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"


# Override the database URL in the config
config.set_main_option("sqlalchemy.url", get_database_url())


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_name=include_name,  # Use our custom include function
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Run migrations with a connection."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_name=include_name,  # Use our custom include function
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations in async mode."""
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = get_database_url()

    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
