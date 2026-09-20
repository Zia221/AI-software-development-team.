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

    connection.commit()
    connection.close()


def create_project(project_idea):

    now = datetime.utcnow().isoformat()

    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO projects
        (project_idea, state, result, error, created_at, updated_at)
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

    return [dict(row) for row in rows]


init_database()