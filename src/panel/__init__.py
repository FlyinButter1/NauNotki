from flask import Blueprint, url_for, redirect, render_template, flash
from flask_login import current_user
from src import db, bcrypt
from src.models import User
from .forms import ChangePassword

panel_bp = Blueprint("panel_bp", __name__, template_folder="templates")




@panel_bp.route("/panel", methods=["POST","GET"])
def panel():
    if not current_user.is_authenticated:
        return redirect(url_for("main.main"))
    
    user = User.query.filter_by(id=current_user.id).first()

    username= user.username

    form=ChangePassword()

    if form.validate_on_submit():
        if bcrypt.check_password_hash(user.password, form.oldpassword.data):
            user.password = bcrypt.generate_password_hash(form.newpassword.data, 12)
            db.session.commit()
            
            flash("password changed succesfully")
        else:
            flash("incorrect old password")
        
    return render_template("panel.html", form=form, username=username)