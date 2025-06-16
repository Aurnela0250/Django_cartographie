from contextlib import asynccontextmanager
from typing import Union

from fastapi import FastAPI  # Retrait de Depends

from config.settings import TORTOISE_ORM

# Importer les fonctions d'initialisation de Tortoise ORM et la configuration
from config.tortoise_init import close_tortoise, init_tortoise


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code exécuté au démarrage
    print("🚀 FastAPI starting - Initializing Tortoise ORM...")
    await init_tortoise(TORTOISE_ORM)  # Initialiser Tortoise ORM
    print("🐢 Tortoise ORM Initialized.")
    print("📋 Use Aerich for schema migrations for Tortoise ORM:")
    print("   - Check status: aerich status")
    print("   - Create migration: aerich migrate --name <migration_name>")
    print("   - Apply migrations: aerich upgrade")
    yield
    # Code exécuté à l'arrêt
    print("🐢 Closing Tortoise ORM connections...")
    await close_tortoise()  # Fermer les connexions Tortoise ORM
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
        "migrations": "Use 'make help' to see all available Alembic commands",
    }


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


# Exemple d'endpoint pour tester la base de données
@app.get("/users/count")
async def get_users_count():  # Retirer la dépendance de session SQLModel
    """Get the current number of users in the database (using Tortoise ORM)."""
    # Exemple avec Tortoise (nécessite que vos modèles soient définis et importés)
    from apps.users.models import (
        User,  # Assurez-vous que ce chemin d'import est correct
    )

    count = await User.all().count()
    return {"users_count": count}


@app.get("/health")
async def health_check():  # Retirer la dépendance de session SQLModel
    """Health check endpoint that tests database connectivity (using Tortoise ORM)."""
    try:
        # Test database connection avec Tortoise ORM
        from apps.users.models import User  # Exemple, utilisez un de vos modèles

        await User.all().first()  # Tente de récupérer un enregistrement

        return {
            "status": "healthy",
            "database": "connected (Tortoise ORM)",
            "message": "All systems operational",
        }
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}
