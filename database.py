import os
import sqlite3
from pathlib import Path
from datetime import datetime


DATABASE_PATH = Path(
    os.getenv("DATABASE_PATH", "project_history.db")
)


def get_connection():
    connection = sqlite3.connect(
        DATABASE_PATH,
        timeout=30
    )

    connection.row_factory = sqlite3.Row

    return connection


def init_database():

    connection = get_connection()

    # Project history table
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_idea TEXT NOT NULL,
            state TEXT NOT NULL,
            result TEXT,
            error TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )

    # Users table
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


# --------------------------------
# PROJECT FUNCTIONS
# --------------------------------

def create_project(project_idea):

    now = datetime.utcnow().isoformat()

    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO projects
        (
            project_idea,
            state,
            result,
            error,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            project_idea,
            "running",
            "",
            "",
            now,
            now
        )
    )

    project_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return project_id


def update_project(
    project_id,
    state,
    result="",
    error=""
):

    now = datetime.utcnow().isoformat()

    connection = get_connection()

    connection.execute(
        """
        UPDATE projects
        SET state = ?,
            result = ?,
            error = ?,
            updated_at = ?
        WHERE id = ?
        """,
        (
            state,
            str(result),
            str(error),
            now,
            project_id
        )
    )

    connection.commit()
    connection.close()


def get_recent_projects(limit=20):

    connection = get_connection()

    rows = connection.execute(
        """
        SELECT *
        FROM projects
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,)
    ).fetchall()

    connection.close()

    return [
        dict(row)
        for row in rows
    ]


# --------------------------------
# USER FUNCTIONS
# --------------------------------

def create_user(
    username,
    password_hash
):

    now = datetime.utcnow().isoformat()

    connection = get_connection()

    try:

        connection.execute(
            """
            INSERT INTO users
            (
                username,
                password_hash,
                created_at
            )
            VALUES (?, ?, ?)
            """,
            (
                username,
                password_hash,
                now
            )
        )

        connection.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        connection.close()


def get_user(username):

    connection = get_connection()

    row = connection.execute(
        """
        SELECT *
        FROM users
        WHERE username = ?
        """,
        (username,)
    ).fetchone()

    connection.close()

    if row:
        return dict(row)

    return None


# --------------------------------
# INITIALIZE DATABASE
# --------------------------------

init_database()