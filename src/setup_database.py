"""
Set up the H1B database: create database, schema, and all raw tables.

Usage:
    uv run python src/setup_database.py
"""

import os
import sys

import psycopg2

# Ensure project root is on path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.db_connector import get_admin_connection, get_h1b_connection, execute_sql_file

SQL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sql")


def create_database():
    """Create the H1B database if it doesn't exist."""
    conn = get_admin_connection(autocommit=True)
    cur = conn.cursor()
    try:
        # Check if database already exists
        cur.execute("SELECT 1 FROM pg_database WHERE datname = 'h1b'")
        if cur.fetchone():
            print("[INFO] Database 'h1b' already exists, skipping creation.")
        else:
            cur.execute("CREATE DATABASE h1b")
            print("[OK] Database 'h1b' created.")
    finally:
        cur.close()
        conn.close()


def create_schema():
    """Create the raw schema inside H1B database."""
    conn = get_h1b_connection()
    try:
        execute_sql_file(conn, os.path.join(SQL_DIR, "02_create_schema.sql"))
        print("[OK] Schema 'raw' created.")
    finally:
        conn.close()


def create_tables():
    """Create all raw tables inside the H1B database."""
    conn = get_h1b_connection()
    try:
        execute_sql_file(conn, os.path.join(SQL_DIR, "03_create_tables.sql"))
        print("[OK] All raw tables created.")
    finally:
        conn.close()


def verify():
    """Verify all tables were created correctly."""
    conn = get_h1b_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'raw'
            ORDER BY table_name
        """)
        tables = [row[0] for row in cur.fetchall()]
        print(f"\n[VERIFY] Found {len(tables)} tables in raw schema:")
        for t in tables:
            # Count columns
            cur.execute("""
                SELECT COUNT(*)
                FROM information_schema.columns
                WHERE table_schema = 'raw' AND table_name = %s
            """, (t,))
            col_count = cur.fetchone()[0]
            print(f"  - raw.{t} ({col_count} columns)")
    finally:
        cur.close()
        conn.close()


def main():
    print("=" * 60)
    print("H1B Database Setup")
    print("=" * 60)

    print("\n[Step 1/4] Creating database...")
    create_database()

    print("\n[Step 2/4] Creating schema...")
    create_schema()

    print("\n[Step 3/4] Creating tables...")
    create_tables()

    print("\n[Step 4/4] Verifying...")
    verify()

    print("\n" + "=" * 60)
    print("Database setup complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
