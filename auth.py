# auth.py
from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, session
    )
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

auth_bp = Blueprint("auth", __name__, template_folder="templates")


def get_user_by_username(username):
    with sqlite3.connect("instance\\database.db") as conn:
        cursor = conn.cursor()
        return cursor.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()


def login_user(user):
    session["user_id"] = user[0]
    session["username"] = user[1]
    flash("Login successful!", "success")


def create_user(username, password, email):
    hashed = generate_password_hash(password)
    with sqlite3.connect("instance\\database.db") as conn:
        conn.execute(
            "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
            (username, hashed, email),
        )
        conn.commit()
        return get_user_by_username(username)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]

        user = create_user(username, password, email)
        login_user(user)
        return redirect(url_for("dashboard"))
    return render_template("register.html.jinja")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = get_user_by_username(username)

        if user and check_password_hash(user[2], password):
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password", "error")
    return render_template("login.html.jinja")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out!", "info")
    return redirect(url_for("auth.login"))
