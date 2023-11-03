from flask import render_template, Blueprint, url_for, request, redirect
from flask_login import current_user
from sqlalchemy import text

from src import db
from src.main import main
from .forms import Add
from src.models import Notes

notes_bp = Blueprint('notes', __name__, template_folder='templates', static_folder="static")


@notes_bp.route("/notes/add", methods=["GET", "POST"])
def add():
    if not current_user.is_authenticated:
        return main()

    form = Add()
    if form.validate_on_submit():
        data = Notes(current_user.id, form.content.data, form.subject.data, form.grade.data, form.school_type.data,
                     form.chapter.data)
        db.session.add(data)
        db.session.commit()
        return main()

    return render_template("add.html", form=form)


@notes_bp.route("/notes/my_notes", methods=["GET", "POST"])
def my_notes():
    if not current_user.is_authenticated:
        return main()
    current_args = request.args.copy()
    component = ""
    for i in current_args:
        if i == 'class':
            component += f" AND grade = \'{current_args['class']}\'"
            break
        if i == 'subject':
            component += f" AND subject = \'{current_args['subject']}\'"
            break
        if i == 'school':
            component += f" AND school_type = \'{current_args['school']}\'"
            break
        if i == 'user_text' and current_args['user_text'] != "":
            component += f" AND content LIKE \'%{current_args['user_text']}%\'"
            break
    sql_query = text(
        f"SELECT * FROM note WHERE owner_id = {current_user.id}{component}")
    output = db.get_engine().connect().execute(sql_query).fetchall()
    return render_template("show.html", own=True, content=output, filtered=(component != ""))

