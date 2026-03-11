"""
PostgreSQL database connector for H1B data pipeline.

Provides connection management for both the admin database (curion_agent)
and the target H1B database.
"""

import os
from urllib.parse import urlparse

import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv()


def _parse_database_url():
    """Parse DATABASE_URL from .env into connection components."""
    url = os.environ["DATABASE_URL"]
    parsed = urlparse(url)
    return {
        "host": parsed.hostname,
        "port": parsed.port or 5432,
        "user": parsed.username,
        "password": parsed.password,
        "dbname": parsed.path.lstrip("/"),
    }


def get_admin_connection(autocommit=False):
    """
    Connect to the admin database (from DATABASE_URL).
    Used for CREATE DATABASE and other server-level operations.
    """
    params = _parse_database_url()
    conn = psycopg2.connect(**params)
    conn.autocommit = autocommit
    return conn


def get_h1b_connection(autocommit=False):
    """
    Connect to the H1B database.
    Assumes the H1B database already exists.
    """
    params = _parse_database_url()
    params["dbname"] = "h1b"
    conn = psycopg2.connect(**params)
    conn.autocommit = autocommit
    return conn


def execute_sql_file(conn, filepath):
    """Read and execute an entire SQL file against a connection."""
    with open(filepath, "r") as f:
        sql_content = f.read()
    with conn.cursor() as cur:
        cur.execute(sql_content)
    conn.commit()
