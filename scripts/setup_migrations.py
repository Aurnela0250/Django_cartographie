#!/usr/bin/env python3
"""
Script pour tester et initialiser les migrations Alembic avec SQLModel.

Ce script :
1. Vérifie la connection à PostgreSQL
2. Crée la première migration si nécessaire
3. Applique les migrations
4. Teste l'autogenerate

Usage:
    python scripts/setup_migrations.py
"""

import asyncio
import os
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv
from sqlmodel import text

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Now import project modules
from infrastructure.db.fastapi.engine import engine

# Import all models to ensure they're registered
from infrastructure.db.fastapi.models import *  # noqa: F401, F403


async def test_database_connection():
    """Test if we can connect to PostgreSQL."""
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT version()"))
            version = result.scalar()
            print("✅ Database connection successful!")
            print(f"   PostgreSQL version: {version}")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


async def check_tables_exist():
    """Check if tables already exist in the database."""
    try:
        async with engine.connect() as conn:
            # Check if user table exists
            result = await conn.execute(
                text(
                    "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'user')"
                )
            )
            table_exists = result.scalar()

            # Check if alembic_version table exists
            result = await conn.execute(
                text(
                    "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'alembic_version')"
                )
            )
            alembic_exists = result.scalar()

            return table_exists, alembic_exists
    except Exception as e:
        print(f"❌ Error checking tables: {e}")
        return False, False


def run_alembic_command(command_args: list) -> bool:
    """Run an Alembic command and return success status."""
    try:
        result = subprocess.run(
            command_args, cwd=project_root, capture_output=True, text=True, timeout=30
        )

        command_str = " ".join(command_args)
        if result.returncode == 0:
            print(f"✅ Command '{command_str}' completed successfully")
            if result.stdout:
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Command '{command_str}' failed")
            if result.stderr:
                print(f"   Error: {result.stderr.strip()}")
            return False

    except subprocess.TimeoutExpired:
        print(f"❌ Command '{command_str}' timed out")
        return False
    except Exception as e:
        print(f"❌ Error running command '{command_str}': {e}")
        return False


async def main():
    """Main migration setup function."""
    print("🚀 Setting up Alembic migrations for SQLModel...")
    print("=" * 50)

    # Check database connection
    print("\n1. Testing database connection...")
    if not await test_database_connection():
        print("❌ Cannot proceed without database connection")
        return False

    # Check current state
    print("\n2. Checking current database state...")
    table_exists, alembic_exists = await check_tables_exist()

    print(f"   User table exists: {'Yes' if table_exists else 'No'}")
    print(f"   Alembic version table exists: {'Yes' if alembic_exists else 'No'}")

    # Determine strategy
    if table_exists and not alembic_exists:
        print("\n3. Tables exist but no Alembic version table found.")
        print(
            "   Strategy: Create initial migration and stamp as head (no actual migration)"
        )

        # Create initial migration
        print("\n   Creating initial migration...")
        if not run_alembic_command(
            ["alembic", "revision", "--autogenerate", "-m", "Initial migration"]
        ):
            return False

        # Stamp as head (mark as applied without running)
        print("\n   Stamping database as head...")
        if not run_alembic_command(["alembic", "stamp", "head"]):
            return False

    elif not table_exists and not alembic_exists:
        print("\n3. No tables found - creating initial migration.")
        print("   Strategy: Create and apply initial migration")

        # Create initial migration
        print("\n   Creating initial migration...")
        if not run_alembic_command(
            ["alembic", "revision", "--autogenerate", "-m", "Initial migration"]
        ):
            return False

        # Apply migration
        print("\n   Applying initial migration...")
        if not run_alembic_command(["alembic", "upgrade", "head"]):
            return False

    elif alembic_exists:
        print("\n3. Alembic is already set up.")
        print("   Checking for pending migrations...")

        # Check current revision
        print("\n   Checking current revision...")
        run_alembic_command(["alembic", "current"])

        # Apply any pending migrations
        print("\n   Applying any pending migrations...")
        if not run_alembic_command(["alembic", "upgrade", "head"]):
            return False

    # Final verification
    print("\n4. Final verification...")
    table_exists_final, alembic_exists_final = await check_tables_exist()

    if table_exists_final and alembic_exists_final:
        print("✅ Migration setup completed successfully!")
        print("\n📋 Next steps:")
        print(
            "   - To create a new migration: alembic revision --autogenerate -m 'Description'"
        )
        print("   - To apply migrations: alembic upgrade head")
        print("   - To check current revision: alembic current")
        print("   - To see migration history: alembic history")
        return True
    else:
        print("❌ Migration setup verification failed")
        return False


if __name__ == "__main__":
    # Ensure we have the required environment variables
    required_vars = ["DB_HOST", "DB_PORT", "DB_USERNAME", "DB_PASSWORD", "DB_NAME"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set these variables or create a .env file")
        sys.exit(1)

    # Run the setup
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
