"""
Health Database Manager
Handles all database operations for health gamification system
Uses async SQLite for non-blocking operations
"""

import aiosqlite
import json
import os
from datetime import datetime, date
from typing import Optional, Dict, List, Any
from pathlib import Path


class HealthDatabase:
    """Manages health metrics database with async operations"""

    def __init__(self, db_path: str = None):
        """
        Initialize database manager

        Args:
            db_path: Path to SQLite database file (default: health_gamification/data/health.db)
        """
        if db_path is None:
            base_dir = Path(__file__).parent.parent.parent
            db_path = base_dir / "data" / "health.db"

        self.db_path = str(db_path)
        self.connection = None

    async def initialize(self) -> bool:
        """
        Initialize database and create tables from schema

        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure data directory exists
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

            # Read schema file
            schema_path = Path(__file__).parent / "schema.sql"
            with open(schema_path, 'r') as f:
                schema_sql = f.read()

            # Connect and execute schema
            async with aiosqlite.connect(self.db_path) as db:
                await db.executescript(schema_sql)
                await db.commit()

            await self.audit_log(
                operation="INITIALIZE",
                table_name="system",
                details={"action": "database_initialized", "schema_version": "1.0"}
            )

            return True

        except Exception as e:
            print(f"Error initializing database: {e}")
            return False

    async def connect(self):
        """Open database connection"""
        if self.connection is None:
            self.connection = await aiosqlite.connect(self.db_path)
            self.connection.row_factory = aiosqlite.Row

    async def disconnect(self):
        """Close database connection"""
        if self.connection:
            await self.connection.close()
            self.connection = None

    async def insert_metrics(
        self,
        date: str,
        weight_kg: Optional[float] = None,
        systolic_bp: Optional[int] = None,
        diastolic_bp: Optional[int] = None,
        steps: Optional[int] = None,
        weight_source: str = "manual",
        bp_source: str = "manual",
        steps_source: str = "manual"
    ) -> bool:
        """
        Insert or update health metrics for a specific date

        Args:
            date: ISO 8601 date string (YYYY-MM-DD)
            weight_kg: Weight in kilograms
            systolic_bp: Systolic blood pressure
            diastolic_bp: Diastolic blood pressure
            steps: Daily step count
            weight_source: Source of weight data
            bp_source: Source of blood pressure data
            steps_source: Source of steps data

        Returns:
            True if successful, False otherwise
        """
        try:
            await self.connect()

            # Use INSERT OR REPLACE to handle duplicates
            query = """
                INSERT OR REPLACE INTO health_metrics
                (date, weight_kg, systolic_bp, diastolic_bp, steps,
                 weight_source, bp_source, steps_source, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?,
                        COALESCE((SELECT created_at FROM health_metrics WHERE date = ?), datetime('now')),
                        datetime('now'))
            """

            await self.connection.execute(
                query,
                (date, weight_kg, systolic_bp, diastolic_bp, steps,
                 weight_source, bp_source, steps_source, date)
            )
            await self.connection.commit()

            # Log to audit trail
            await self.audit_log(
                operation="INSERT",
                table_name="health_metrics",
                details={
                    "date": date,
                    "weight_kg": weight_kg,
                    "systolic_bp": systolic_bp,
                    "diastolic_bp": diastolic_bp,
                    "steps": steps
                }
            )

            return True

        except Exception as e:
            print(f"Error inserting metrics: {e}")
            await self.audit_log(
                operation="INSERT",
                table_name="health_metrics",
                details={"error": str(e)},
                success=False
            )
            return False

    async def get_latest_weight(self) -> Optional[Dict[str, Any]]:
        """
        Get most recent weight measurement

        Returns:
            Dictionary with date, weight_kg, source or None
        """
        try:
            await self.connect()

            query = """
                SELECT date, weight_kg, weight_source
                FROM health_metrics
                WHERE weight_kg IS NOT NULL
                ORDER BY date DESC
                LIMIT 1
            """

            async with self.connection.execute(query) as cursor:
                row = await cursor.fetchone()
                if row:
                    return {
                        "date": row["date"],
                        "weight_kg": row["weight_kg"],
                        "source": row["weight_source"]
                    }
            return None

        except Exception as e:
            print(f"Error getting latest weight: {e}")
            return None

    async def get_running_balance(self) -> float:
        """
        Get current running balance from health scores

        Returns:
            Current running balance (default 0.0)
        """
        try:
            await self.connect()

            query = """
                SELECT running_balance
                FROM health_scores
                ORDER BY date DESC
                LIMIT 1
            """

            async with self.connection.execute(query) as cursor:
                row = await cursor.fetchone()
                if row:
                    return row["running_balance"]
            return 0.0

        except Exception as e:
            print(f"Error getting running balance: {e}")
            return 0.0

    async def get_metrics_by_date(self, date: str) -> Optional[Dict[str, Any]]:
        """
        Get all metrics for a specific date

        Args:
            date: ISO 8601 date string (YYYY-MM-DD)

        Returns:
            Dictionary of metrics or None
        """
        try:
            await self.connect()

            query = "SELECT * FROM health_metrics WHERE date = ?"

            async with self.connection.execute(query, (date,)) as cursor:
                row = await cursor.fetchone()
                if row:
                    return dict(row)
            return None

        except Exception as e:
            print(f"Error getting metrics by date: {e}")
            return None

    async def get_metrics_range(self, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """
        Get metrics for a date range

        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)

        Returns:
            List of metric dictionaries
        """
        try:
            await self.connect()

            query = """
                SELECT * FROM health_metrics
                WHERE date BETWEEN ? AND ?
                ORDER BY date ASC
            """

            async with self.connection.execute(query, (start_date, end_date)) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]

        except Exception as e:
            print(f"Error getting metrics range: {e}")
            return []

    async def insert_score(
        self,
        date: str,
        weight_score: float = 0,
        bp_score: float = 0,
        steps_score: float = 0,
        total_daily_score: float = 0,
        running_balance: float = 0,
        portfolio_usd: float = 0
    ) -> bool:
        """
        Insert daily health score

        Args:
            date: ISO 8601 date string
            weight_score: Score from weight
            bp_score: Score from blood pressure
            steps_score: Score from steps
            total_daily_score: Sum of all scores
            running_balance: Cumulative balance
            portfolio_usd: Portfolio value

        Returns:
            True if successful
        """
        try:
            await self.connect()

            query = """
                INSERT OR REPLACE INTO health_scores
                (date, weight_score, bp_score, steps_score, total_daily_score,
                 running_balance, portfolio_usd)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """

            await self.connection.execute(
                query,
                (date, weight_score, bp_score, steps_score, total_daily_score,
                 running_balance, portfolio_usd)
            )
            await self.connection.commit()

            return True

        except Exception as e:
            print(f"Error inserting score: {e}")
            return False

    async def audit_log(
        self,
        operation: str,
        table_name: str,
        record_id: Optional[int] = None,
        user_agent: str = "health_db",
        details: Optional[Dict[str, Any]] = None,
        success: bool = True
    ) -> bool:
        """
        Add entry to audit log

        Args:
            operation: Operation type (INSERT, UPDATE, DELETE, etc.)
            table_name: Name of affected table
            record_id: ID of affected record
            user_agent: Component making the change
            details: Additional details as dictionary
            success: Whether operation succeeded

        Returns:
            True if logged successfully
        """
        try:
            await self.connect()

            query = """
                INSERT INTO audit_log
                (operation, table_name, record_id, user_agent, details, success)
                VALUES (?, ?, ?, ?, ?, ?)
            """

            details_json = json.dumps(details) if details else None

            await self.connection.execute(
                query,
                (operation, table_name, record_id, user_agent, details_json, int(success))
            )
            await self.connection.commit()

            return True

        except Exception as e:
            # Don't log audit failures to avoid recursion
            print(f"Error writing to audit log: {e}")
            return False

    async def get_config(self, key: str) -> Optional[str]:
        """Get configuration value by key"""
        try:
            await self.connect()

            query = "SELECT value FROM system_config WHERE key = ?"
            async with self.connection.execute(query, (key,)) as cursor:
                row = await cursor.fetchone()
                if row:
                    return row["value"]
            return None

        except Exception as e:
            print(f"Error getting config: {e}")
            return None

    async def set_config(self, key: str, value: str, description: str = "") -> bool:
        """Set configuration value"""
        try:
            await self.connect()

            query = """
                INSERT OR REPLACE INTO system_config (key, value, description, updated_at)
                VALUES (?, ?, ?, datetime('now'))
            """

            await self.connection.execute(query, (key, value, description))
            await self.connection.commit()

            return True

        except Exception as e:
            print(f"Error setting config: {e}")
            return False


# Context manager support
class HealthDatabaseContext:
    """Context manager for HealthDatabase to ensure cleanup"""

    def __init__(self, db_path: str = None):
        self.db = HealthDatabase(db_path)

    async def __aenter__(self):
        await self.db.connect()
        return self.db

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.db.disconnect()
