import os.path
import re
from ctypes import c_char_p, c_int

from flask import render_template, url_for, redirect, flash, send_file, abort, make_response
from flask import Blueprint
from sqlalchemy import text

from src.models import User
from src import db, bcrypt, login_manager, mylibrary
from .forms import Register, Login
from flask_login import login_user, login_required, logout_user, current_user
from src.main import main
from random import randint, choice
from math import log

auth_bp = Blueprint(
    "auth", __name__, template_folder="templates", static_folder="static", static_url_path='/auth-static')
frequency_list = [1, 2, 2]+[4 for _ in range(4)]+[8 for _ in range(8)]+[16 for _ in range(16)]+[8 for _ in range(32)]
@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

login_manager.login_view = "auth.login"

def generate_named_pfp(name: str, username=""):
    mylibrary.generate(
        c_char_p(bytes(os.path.abspath("src/static/img/template.bmp"), 'utf-8')),
        c_char_p(bytes(os.path.abspath(f"src/static/img/{name}.bmp"), 'utf-8')),
        c_char_p(bytes(username, 'utf-8')),
        c_int(choice(frequency_list)))  # the randomness is now in the username

@auth_bp.route("/generate_pfp", methods=["POST"])
def generate_new_pfp():
    try:
        filename = str(current_user.id)
        generate_named_pfp(filename, current_user.username)
        return make_response('File created successfully.', 201)  # file created - hence http 201
    except Exception:
        abort(403)

@auth_bp.route("/pfp/<path:filename>")
def serve_profile_picture(filename):
    if re.match(r"[0-9]+\.(bmp|png)", filename):
        try:
            return send_file(f'static/img/{filename}')
        except Exception:
            abort(404)
    abort(403)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form=Register()

    if form.validate_on_submit():
        user = User(form.email.data, form.username.data, form.password.data, form.role.data)
        db.session.add(user)
        db.session.commit()
        received_data = db.get_engine().connect().execute(
            text(f"SELECT id FROM user WHERE username = \'{form.username.data}\'")).fetchall()[0][0]
        generate_named_pfp(received_data, form.username.data)
        return redirect(url_for("auth.login"))

    return render_template("register.html", form=form)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form=Login()

    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user is not None:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for("notes.my_notes"))
        flash("Nieporawny login i/lub hasło")

    return render_template("login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Wylogowano")
    return redirect(url_for("auth.login"))
