from flask_login import current_user
from flask import render_template, Blueprint, request, redirect, url_for
from sqlalchemy import text
import re
from src import db, app

main_bp = Blueprint('main', __name__, template_folder='templates', static_folder="static", static_url_path='/main-static')
@main_bp.route("/")
def main() -> str:  # main page render function isolated in file to get current status
    temp_username = current_user.username if current_user.is_authenticated else ""
    return render_template("main.html", username=temp_username)

# error handlers
@app.errorhandler(404)
def error_404(e):
    return render_template("error_handler.html", error=404, content="This site does not exist")
@app.errorhandler(403)
def error_403(e):
    return render_template("error_handler.html", error=403, content="You are not logged in or you have attempted to access files that are not yours")
@app.errorhandler(418)
def error_418(e):
    return render_template("error_handler.html", error=418, content="I'm a teapot")
