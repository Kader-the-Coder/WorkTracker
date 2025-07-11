import os
import sys
import sqlite3
from flask import Flask, render_template

app = Flask(__name__)


def init_db():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
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
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
            );
        """)

        conn.commit()


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    db_exists = os.path.exists("database.db")
    args = sys.argv[1:]

    if "reset" in args:
        if db_exists:
            os.remove("database.db")
        init_db()
        db_exists = True

    if not db_exists:
        init_db()

    if "local" in args:
        app.run(host="localhost", port=5000, debug=True)
    else:
        app.run()
