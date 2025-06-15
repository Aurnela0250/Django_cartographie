import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent.parent / ".env"
load_dotenv(env_path)

# Import all models to register them with SQLModel.metadata
# Note: These imports are necessary for table creation and Alembic autogenerate
from .models import User  # noqa: F401

# PostgreSQL async configuration - using variables from .env file
DATABASE_NAME = os.getenv("DB_NAME", "cartographie_db")
DATABASE_PASSWORD = os.getenv("DB_PASSWORD", "123456")
DATABASE_HOST = os.getenv("DB_HOST", "localhost")
DATABASE_PORT = os.getenv("DB_PORT", "5432")
DATABASE_USER = os.getenv(
    "DB_USERNAME", "cartographie"
)  # Note: using DB_USERNAME from .env
DATABASE_ECHO = os.getenv("DB_ECHO", "false").lower() == "true"

# PostgreSQL async URL for asynchronous operations
DATABASE_URL = f"postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

# Create async engine with PostgreSQL optimizations
engine = create_async_engine(
    DATABASE_URL,
    echo=DATABASE_ECHO,
    future=True,
    pool_size=20,
    max_overflow=0,
    pool_pre_ping=True,
    pool_recycle=300,
)

# Create async session factory
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def create_db_and_tables():
    """Create database tables asynchronously.

    Note: This is mainly for development/testing.
    In production, use Alembic migrations for schema management.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session():
    """Dependency to get async database session."""
    async with async_session() as session:
        yield session
