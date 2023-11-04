import os
import re

from flask import Blueprint, url_for, redirect, render_template, flash, request, send_file, abort
from flask_login import current_user
from sqlalchemy import text

from src import db, bcrypt
from src.models import User
from .forms import ChangePassword

panel_bp = Blueprint("panel_bp", __name__, template_folder="templates")


@panel_bp.route("/panel", methods=["POST", "GET"])
def panel():
    if not current_user.is_authenticated:
        return redirect(url_for("main.main"))

    user = User.query.filter_by(id=current_user.id).first()

    username = user.username

    form=ChangePassword()

    if form.validate_on_submit():
        if bcrypt.check_password_hash(user.password, form.oldpassword.data):
            user.password = bcrypt.generate_password_hash(form.newpassword.data, 12)
            db.session.commit()

            flash("password changed successfully")
        else:
            flash("incorrect old password")

    userdata = db.get_engine().connect().execute(text(f"SELECT * FROM user WHERE id = {current_user.id}")).fetchall()[0]
    pfp = str(userdata[0])+".bmp"
    return render_template("panel.html", form=form, username=userdata[2], email=userdata[1], account_type=userdata[4],
                           pfp=pfp, pfp_exists=profile_picture_existence_checker(pfp))

@panel_bp.route("/change_email", methods=["POST"])
def change_email():
    new_email = request.form.get('email')
    if re.match("^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$", new_email):
        connection = db.get_engine().connect()
        connection.execute(text(f"UPDATE user SET email = \'{new_email}\' WHERE id = {current_user.id}"))
        connection.commit()
    return ""

@panel_bp.route("/change_type", methods=["POST"])
def change_type():
    new_email = request.form.get('curtype')
    role = 'uczen' if new_email == 'nauczyciel' else 'nauczyciel'
    connection = db.get_engine().connect()
    connection.execute(text(f"UPDATE user SET role = \'{role}\' WHERE id = {current_user.id}"))
    connection.commit()
    return ""

@panel_bp.route("/account")
def account():
    pass

def profile_picture_existence_checker(filename):
    return os.path.exists(f'src/static/img/{filename}')
