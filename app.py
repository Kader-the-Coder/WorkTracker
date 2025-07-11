import os
import sqlite3
from flask import Flask, render_template

app = Flask(__name__)


def init_db():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.executemany(
            """
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                color TEXT NOT NULL,
                description TEXT
            );
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                color TEXT NOT NULL,
                description TEXT
            );
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                color TEXT NOT NULL,
                description TEXT
            );
        """
        )
        conn.commit()


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
