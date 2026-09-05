"""
Database connection and query management module for the portfolio application.
Uses SQLite by default with parameterized queries to completely prevent SQL injection.
"""

import os
import sqlite3
from contextlib import contextmanager
from typing import Any, Dict, List, Optional

# Database file location (co-located with app in workspace)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.environ.get("DATABASE_PATH", os.path.join(BASE_DIR, "portfolio.db"))
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")


@contextmanager
def get_db_connection():
    """
    Context manager providing a managed SQLite connection.
    Automatically handles commit and rollback, and configures Row factory for dict access.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db() -> None:
    """
    Initialize the database using the DDL and seed statements from schema.sql.
    Safe to run repeatedly; tables and seed rows use IF NOT EXISTS.
    """
    if not os.path.exists(SCHEMA_PATH):
        raise FileNotFoundError(f"Schema file not found at: {SCHEMA_PATH}")

    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema_script = f.read()

    with get_db_connection() as conn:
        conn.executescript(schema_script)


def save_contact_message(name: str, email: str, subject: str, message: str) -> int:
    """
    Inserts a contact form submission using parameterized SQL queries to prevent SQL injection.

    :param name: Sender's name
    :param email: Sender's email address
    :param subject: Inquiry subject line
    :param message: Message body
    :return: The generated message ID
    """
    query = """
        INSERT INTO contact_messages (name, email, subject, message)
        VALUES (?, ?, ?, ?);
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (name.strip(), email.strip(), subject.strip(), message.strip()))
        return cursor.lastrowid


def get_all_projects() -> List[Dict[str, Any]]:
    """
    Fetches all projects ordered by creation date.
    :return: List of project dictionaries
    """
    query = """
        SELECT id, title, description, tags, live_url, github_url, created_at
        FROM projects
        ORDER BY id ASC;
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def get_contact_messages(limit: int = 50) -> List[Dict[str, Any]]:
    """
    Fetches recent contact messages.
    :param limit: Maximum number of messages to return
    :return: List of contact message dictionaries
    """
    query = """
        SELECT id, name, email, subject, message, created_at
        FROM contact_messages
        ORDER BY created_at DESC
        LIMIT ?;
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (limit,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


if __name__ == "__main__":
    print("[*] Initializing database...")
    init_db()
    print("[*] Database initialized successfully at:", DATABASE_PATH)
    projects = get_all_projects()
    print(f"[*] Loaded {len(projects)} projects.")
    for p in projects:
        print(f"  - {p['title']} ({p['tags']})")
