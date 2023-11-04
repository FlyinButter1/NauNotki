from flask_login import current_user
from flask import render_template, Blueprint, request, redirect
from sqlalchemy import text
import re
from src import db

main_bp = Blueprint('main', __name__, template_folder='templates', static_folder="static")
@main_bp.route("/")
def main() -> str:  # main page render function isolated in file to get current status
    temp_username = current_user.username if current_user.is_authenticated else ""
    return render_template("main.html", username=temp_username)
