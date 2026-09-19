import os
import psycopg2
from psycopg2.extras import RealDictCursor


def get_connection():
    """
    Connect to Supabase PostgreSQL database.
    """

    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError(
            "DATABASE_URL is not configured."
        )

    return psycopg2.connect(database_url)


def create_database():
    """
    Create the system_metrics table if it does not already exist.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_metrics (
            id BIGSERIAL PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT NOW(),
            cpu REAL,
            ram REAL,
            disk REAL,
            bytes_sent BIGINT,
            bytes_received BIGINT
        )
    """)

    connection.commit()

    cursor.close()
    connection.close()


def save_metrics(metrics):
    """
    Save one system-metrics record to Supabase.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO system_metrics (
            timestamp,
            cpu,
            ram,
            disk,
            bytes_sent,
            bytes_received
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        metrics["timestamp"],
        metrics["cpu"],
        metrics["ram"],
        metrics["disk"],
        metrics["bytes_sent"],
        metrics["bytes_received"]
    ))

    connection.commit()

    cursor.close()
    connection.close()


def get_metrics(limit=150):
    """
    Get recent system metrics from Supabase.
    """

    connection = get_connection()

    cursor = connection.cursor(
        cursor_factory=RealDictCursor
    )

    cursor.execute("""
        SELECT
            timestamp,
            cpu,
            ram,
            disk,
            bytes_sent,
            bytes_received
        FROM system_metrics
        ORDER BY id DESC
        LIMIT %s
    """, (limit,))

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows