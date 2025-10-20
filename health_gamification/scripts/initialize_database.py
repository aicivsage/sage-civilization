#!/usr/bin/env python3
"""
Database Initialization Script
Creates health.db and sets up all tables
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from database.health_db import HealthDatabase


async def main():
    """Initialize database"""
    print("=" * 60)
    print("Health Gamification - Database Initialization")
    print("=" * 60)
    print()

    # Initialize database
    db = HealthDatabase()
    print(f"Database path: {db.db_path}")
    print()

    print("Creating database and tables...")
    success = await db.initialize()

    if success:
        print("✓ Database initialized successfully!")
        print()

        # Verify tables exist
        print("Verifying tables...")
        await db.connect()

        query = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        async with db.connection.execute(query) as cursor:
            tables = await cursor.fetchall()

        print(f"Found {len(tables)} tables:")
        for table in tables:
            print(f"  - {table[0]}")

        # Show configuration
        print()
        print("System configuration:")
        config_query = "SELECT key, value, description FROM system_config"
        async with db.connection.execute(config_query) as cursor:
            configs = await cursor.fetchall()

        for config in configs:
            print(f"  {config[0]}: {config[1]} ({config[2]})")

        await db.disconnect()

        print()
        print("=" * 60)
        print("Database ready for use!")
        print("=" * 60)

    else:
        print("✗ Error initializing database")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
