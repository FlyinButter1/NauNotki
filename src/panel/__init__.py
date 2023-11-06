import os
import re

from flask import Blueprint, url_for, redirect, render_template, flash, request, abort, make_response
from flask_login import current_user
from sqlalchemy import text

from src import db, bcrypt
from src.models import User
from .forms import ChangePassword

panel_bp = Blueprint(
    "panel_bp", __name__, template_folder="templates", static_folder="static", static_url_path='/panel-static')

@panel_bp.route("/panel/<path:username>", methods=["GET"])
def userpage(username):
    sql_query = text(f"SELECT * FROM user WHERE username = \'{username}\'")
    userdata = db.get_engine().connect().execute(sql_query).fetchall()
    if len(userdata) != 1:
        abort(404)
    if userdata[0][0] == current_user.id:
        return redirect("/panel")
    return render_template("foreign_panel.html", userdata=userdata[0],
                           pfp_exists=profile_picture_existence_checker(f"{userdata[0][0]}.bmp"))

@panel_bp.route("/panel", methods=["POST", "GET"])
def panel():
    if not current_user.is_authenticated:
        return redirect(url_for("main.main"))

    user = User.query.filter_by(id=current_user.id).first()

    form = ChangePassword()

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
    if re.match(r"^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$", new_email):
        if current_user.is_authenticated:
            connection = db.get_engine().connect()
            connection.execute(text(f"UPDATE user SET email = \'{new_email}\' WHERE id = {current_user.id}"))
            connection.commit()
            response = make_response('')
            response.status_code = 204
            return response
        abort(403)  # else
    abort(400)

@panel_bp.route("/change_type", methods=["POST"])
def change_type():
    new_type = request.form.get('curtype')
    if new_type not in {'uczen', 'nauczyciel'}:
        abort(400)
    role = 'uczen' if new_type == 'nauczyciel' else 'nauczyciel'
    if current_user.is_authenticated:
        connection = db.get_engine().connect()
        connection.execute(text(f"UPDATE user SET role = \'{role}\' WHERE id = {current_user.id}"))
        connection.commit()
        response = make_response('')
        response.status_code = 204
        return response
    abort(403)  # else

def profile_picture_existence_checker(filename):
    return os.path.exists(f'src/static/img/{filename}')
