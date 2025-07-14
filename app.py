import os
import sys
from db import init_db
from functools import wraps
from flask import (
    Flask, flash, render_template, url_for, redirect, session
)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
if app.secret_key is None:
    raise RuntimeError("SECRET_KEY not set in environment!")


def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in first.", "error")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapper


@app.route("/")
def index():
    return render_template("index.html.jinja")


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html.jinja")


if __name__ == "__main__":
    from auth import auth_bp
    app.register_blueprint(auth_bp)
    db_exists = os.path.exists("instance\\database.db")
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
