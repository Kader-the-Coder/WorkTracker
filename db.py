import sqlite3
from werkzeug.security import generate_password_hash


def init_db():
    with sqlite3.connect("instance//database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL UNIQUE,
                color TEXT NOT NULL,
                description TEXT DEFAULT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS time_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                project_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                description TEXT DEFAULT NULL,
                start_time TIMESTAMP NOT NULL,
                end_time TIMESTAMP DEFAULT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
                             ON DELETE CASCADE,
                FOREIGN KEY (project_id) REFERENCES projects(id)
                             ON DELETE CASCADE
            );
        """)

        conn.commit()


def add_user(username, password, email):
    hashed = generate_password_hash(password)
    with sqlite3.connect("instance\\database.db") as conn:
        conn.execute(
            "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
            (username, hashed, email),
        )
        conn.commit()
        return get_user_by_username(username)


def get_user_by_username(username):
    with sqlite3.connect("instance\\database.db") as conn:
        cursor = conn.cursor()
        return cursor.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()


def add_project(user_id, name, color, description=""):
    with sqlite3.connect("instance\\database.db") as conn:
        conn.execute(
            "INSERT INTO projects (user_id, name, color, description) "
            "VALUES (?, ?, ?, ?)",
            (user_id, name, color, description),
        )
        conn.commit()


def get_projects(user_id):
    with sqlite3.connect("instance\\database.db") as conn:
        cursor = conn.cursor()
        data = cursor.execute(
            "SELECT * FROM projects WHERE user_id = ?", (user_id,)
        ).fetchall()

        return [
            {
                "id": project[0],
                "name": project[2],
                "color": project[3],
                "description": project[4],
            }
            for project in data
        ]
