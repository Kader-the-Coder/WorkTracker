from flask import (
    Blueprint, render_template, redirect, url_for, flash, request, session
)
from utils import login_required
from db import add_project, get_projects

tracker_bp = Blueprint("tracker", __name__, template_folder="templates")


@tracker_bp.route("/")
def index():
    return render_template("index.html.jinja")


@tracker_bp.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    if request.method == "POST":
        user_id = session["user_id"]
        proj_name = request.form["project_name"]
        proj_color = request.form["project_color"]
        proj_desc = request.form["project_description"]
        if not add_project(user_id, proj_name, proj_color, proj_desc):
            flash("Project already exists", "error")

        return redirect(url_for("tracker.dashboard"))

    proj = get_projects(session["user_id"])
    return render_template("dashboard.html.jinja", projects=proj)
