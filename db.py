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
                name TEXT NOT NULL,
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
