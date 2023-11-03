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
@main_bp.route("/change_email", methods=["POST"])
def change_email():
    new_email = request.form.get('email')
    if re.match("^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$", new_email):
        connection = db.get_engine().connect()
        connection.execute(text(f"UPDATE user SET email = \'{new_email}\' WHERE id = {current_user.id}"))
        connection.commit()
    return ""

@main_bp.route("/change_type", methods=["POST"])
def change_type():
    new_email = request.form.get('curtype')
    role = 'uczen' if new_email == 'nauczyciel' else 'nauczyciel'
    connection = db.get_engine().connect()
    connection.execute(text(f"UPDATE user SET role = \'{role}\' WHERE id = {current_user.id}"))
    connection.commit()
    return ""

@main_bp.route("/my_account")
def my_account():
    userdata = db.get_engine().connect().execute(text(f"SELECT * FROM user WHERE id = {current_user.id}")).fetchall()[0]
    print(userdata)
    return render_template("my_account.html", username=userdata[2], email=userdata[1], account_type=userdata[4])

@main_bp.route("/account")
def account():
    pass