from contextlib import asynccontextmanager
from typing import Union

from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from infrastructure.db.fastapi.engine import create_db_and_tables, get_session
from infrastructure.db.fastapi.models.user_model import User


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code exécuté au démarrage
    # Note: En production, utilisez Alembic pour les migrations
    # Cette ligne est utile pour le développement/test uniquement
    await create_db_and_tables()
    print("🚀 FastAPI started - Database tables ready")
    print(
        "📋 Use Alembic for schema migrations: python scripts/migration_helper.py status"
    )
    yield
    # Code exécuté à l'arrêt (si nécessaire)
    print("⏹️  FastAPI shutting down")


app = FastAPI(
    title="Django Cartographie API",
    description="API FastAPI with SQLModel and Alembic migrations",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
async def read_root():
    return {
        "message": "Django Cartographie API",
        "status": "running",
        "migrations": "Use Alembic for database schema management",
    }


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


# Exemple d'endpoint pour tester la base de données
@app.get("/users/count")
async def get_users_count(session: AsyncSession = Depends(get_session)):
    """Get the current number of users in the database."""
    from sqlmodel import func

    statement = select(func.count()).select_from(User)
    result = await session.execute(statement)
    count = result.scalar()

    return {"users_count": count}


@app.get("/health")
async def health_check(session: AsyncSession = Depends(get_session)):
    """Health check endpoint that tests database connectivity."""
    try:
        # Test database connection
        from sqlmodel import text

        result = await session.execute(text("SELECT 1"))
        result.scalar()

        return {
            "status": "healthy",
            "database": "connected",
            "message": "All systems operational",
        }
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}
