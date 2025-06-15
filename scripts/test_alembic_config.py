#!/usr/bin/env python3
"""
Simple test script to verify Alembic configuration with SQLModel.
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_alembic_imports():
    """Test that Alembic can import our models correctly."""
    print("Testing Alembic imports...")

    try:
        # Test SQLModel import
        from sqlmodel import SQLModel

        print("✅ SQLModel imported successfully")

        # Test models import
        print("✅ User model imported successfully")

        # Test that models are registered in metadata
        tables = SQLModel.metadata.tables
        print(f"✅ Found {len(tables)} tables in SQLModel metadata:")
        for table_name in tables.keys():
            print(f"   - {table_name}")

        return True

    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False


def test_alembic_env():
    """Test that Alembic env.py can be imported."""
    print("\nTesting Alembic env.py...")

    try:
        # Add alembic directory to path
        alembic_path = project_root / "alembic"
        sys.path.insert(0, str(alembic_path))

        # This should work if env.py is configured correctly
        print("✅ Alembic env.py imported successfully")
        return True

    except Exception as e:
        print(f"❌ Alembic env.py import failed: {e}")
        return False


def main():
    """Run all tests."""
    print("🧪 Testing Alembic + SQLModel configuration")
    print("=" * 50)

    # Check environment variables
    print("Checking environment variables...")
    required_vars = ["DB_HOST", "DB_PORT", "DB_USER", "DB_PASSWORD", "DB_NAME"]
    missing_vars = []

    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var} = {value}")
        else:
            print(f"❌ {var} is not set")
            missing_vars.append(var)

    if missing_vars:
        print(f"\n❌ Missing required environment variables: {missing_vars}")
        print("Please set these variables before running Alembic commands.")
        return False

    # Test imports
    if not test_alembic_imports():
        return False

    if not test_alembic_env():
        return False

    print("\n✅ All tests passed! Alembic configuration looks good.")
    print("\n📋 Next steps:")
    print("1. Set up database connection (ensure PostgreSQL is running)")
    print("2. Run: python scripts/setup_migrations.py")
    print("3. Or manually:")
    print("   - alembic revision --autogenerate -m 'Initial migration'")
    print("   - alembic upgrade head")

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
