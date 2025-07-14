from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, session
    )
from werkzeug.security import check_password_hash
from db import add_user, get_user_by_username

auth_bp = Blueprint("auth", __name__, template_folder="templates")


def login_user(user):
    session["user_id"] = user[0]
    session["username"] = user[1]
    flash("Login successful!", "success")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]

        user = add_user(username, password, email)
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
