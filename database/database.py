import sqlite3
import os


DATABASE_FILE = "data/system_metrics.db"


def create_database():

    os.makedirs("data", exist_ok=True)

    connection = sqlite3.connect(DATABASE_FILE)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            cpu REAL,
            ram REAL,
            disk REAL,
            bytes_sent INTEGER,
            bytes_received INTEGER
        )
    """)

    connection.commit()

    connection.close()


def save_metrics(metrics):

    connection = sqlite3.connect(DATABASE_FILE)

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
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        metrics["timestamp"],
        metrics["cpu"],
        metrics["ram"],
        metrics["disk"],
        metrics["bytes_sent"],
        metrics["bytes_received"]
    ))

    connection.commit()

    connection.close()


def get_metrics():

    connection = sqlite3.connect(DATABASE_FILE)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            timestamp,
            cpu,
            ram,
            disk,
            bytes_sent,
            bytes_received
        FROM system_metrics
        ORDER BY id
    """)

    rows = cursor.fetchall()

    connection.close()

    return rows


if __name__ == "__main__":

    create_database()

    print("SQLite database created successfully!")
    print("Location:", DATABASE_FILE)