#!/usr/bin/env python3
"""
Utilitaire pour gérer les migrations Alembic SQLModel.

Usage:
    python scripts/migration_helper.py status           # Voir l'état actuel
    python scripts/migration_helper.py create "message" # Créer une migration
    python scripts/migration_helper.py apply           # Appliquer les migrations
    python scripts/migration_helper.py rollback        # Revenir d'une migration
    python scripts/migration_helper.py history         # Voir l'historique
    python scripts/migration_helper.py check           # Vérifier l'état de la base
"""

import argparse
import asyncio
import os
import subprocess
import sys
from pathlib import Path

from sqlmodel import text

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from infrastructure.db.fastapi.engine import engine


def run_alembic_command(command: list) -> bool:
    """Run an Alembic command and return success status."""
    try:
        result = subprocess.run(
            command, cwd=project_root, capture_output=True, text=True, timeout=60
        )

        print(result.stdout)
        if result.stderr:
            print("Warnings/Errors:", result.stderr)

        return result.returncode == 0

    except subprocess.TimeoutExpired:
        print(f"❌ Command {' '.join(command)} timed out")
        return False
    except Exception as e:
        print(f"❌ Error running command {' '.join(command)}: {e}")
        return False


async def check_database_status():
    """Check database connection and current state."""
    try:
        async with engine.connect() as conn:
            # Test connection
            result = await conn.execute(text("SELECT version()"))
            version = result.scalar()
            print("✅ Database connection: OK")
            version_str = version.split(",")[0] if version else "Unknown"
            print(f"   PostgreSQL: {version_str}")

            # Check if alembic_version table exists
            result = await conn.execute(
                text(
                    "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'alembic_version')"
                )
            )
            alembic_exists = result.scalar()

            if alembic_exists:
                result = await conn.execute(
                    text("SELECT version_num FROM alembic_version")
                )
                current_version = result.scalar()
                print("✅ Alembic: Configured")
                print(f"   Current revision: {current_version}")
            else:
                print("⚠️  Alembic: Not initialized")

            # Check user table structure
            result = await conn.execute(
                text(
                    "SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'user'"
                )
            )
            column_count = result.scalar()
            print(f"✅ User table: {column_count} columns")

            return True

    except Exception as e:
        print(f"❌ Database check failed: {e}")
        return False


def status():
    """Show current migration status."""
    print("🔍 Migration Status")
    print("=" * 40)

    # Check database
    if not asyncio.run(check_database_status()):
        return False

    print("\n📋 Alembic Status:")
    run_alembic_command(["alembic", "current", "-v"])

    print("\n🔄 Pending migrations:")
    run_alembic_command(["alembic", "history", "--rev-range", "current:head"])

    return True


def create_migration(message: str):
    """Create a new migration."""
    print(f"🔨 Creating migration: {message}")
    print("=" * 40)

    return run_alembic_command(["alembic", "revision", "--autogenerate", "-m", message])


def apply_migrations():
    """Apply pending migrations."""
    print("🚀 Applying migrations...")
    print("=" * 40)

    return run_alembic_command(["alembic", "upgrade", "head"])


def rollback_migration():
    """Rollback last migration."""
    print("⏪ Rolling back last migration...")
    print("=" * 40)

    # First show current status
    print("Current status:")
    run_alembic_command(["alembic", "current"])

    # Ask for confirmation
    response = input("\n⚠️  Are you sure you want to rollback? (y/N): ")
    if response.lower() != "y":
        print("❌ Rollback cancelled")
        return False

    return run_alembic_command(["alembic", "downgrade", "-1"])


def show_history():
    """Show migration history."""
    print("📜 Migration History")
    print("=" * 40)

    return run_alembic_command(["alembic", "history", "-v"])


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(description="SQLModel Migration Helper")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Status command
    subparsers.add_parser("status", help="Show current migration status")

    # Create command
    create_parser = subparsers.add_parser("create", help="Create a new migration")
    create_parser.add_argument("message", help="Migration message")

    # Apply command
    subparsers.add_parser("apply", help="Apply pending migrations")

    # Rollback command
    subparsers.add_parser("rollback", help="Rollback last migration")

    # History command
    subparsers.add_parser("history", help="Show migration history")

    # Check command
    subparsers.add_parser("check", help="Check database status")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Ensure we have the required environment variables
    required_vars = ["DB_HOST", "DB_PORT", "DB_USERNAME", "DB_PASSWORD", "DB_NAME"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease check your .env file")
        sys.exit(1)

    success = False

    if args.command == "status":
        success = status()
    elif args.command == "create":
        success = create_migration(args.message)
    elif args.command == "apply":
        success = apply_migrations()
    elif args.command == "rollback":
        success = rollback_migration()
    elif args.command == "history":
        success = show_history()
    elif args.command == "check":
        success = asyncio.run(check_database_status())

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
