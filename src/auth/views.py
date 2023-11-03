from flask import render_template, url_for, redirect, flash
from flask import Blueprint
from src.models import User
from src import db, bcrypt, login_manager
from .forms import Register, Login
from flask_login import login_user, login_required, logout_user
from src.main import main

auth_bp = Blueprint("auth", __name__, template_folder="templates", static_folder="static")

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

login_manager.login_view = "auth.login"

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form=Register()
    
    if form.validate_on_submit():
        user = User(form.email.data, form.username.data, form.password.data, form.role.data)
        db.session.add(user)
        db.session.commit()
        return login()

    return render_template("register.html", form=form)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form=Login()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user is not None:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return main()
        
        
        flash("Nieporawny login i/lub hasło")

    return render_template("login.html", form=form)
        

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Wylogowano")
    return redirect(url_for("auth.login"))

@auth_bp.route("/login_test")
@login_required
def login_test():
    return "tajny shit"