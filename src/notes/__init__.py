from flask import render_template, Blueprint, url_for, request, redirect
from flask_login import current_user
from sqlalchemy import text, TextClause
from werkzeug.datastructures import MultiDict
from random import sample

from src import db
from src.main import main
from .forms import Add
from src.models import Notes

notes_bp = Blueprint('notes', __name__, template_folder='templates', static_folder="static", static_url_path='/notes-static')

run = lambda x: db.get_engine().connect().execute(x)

@notes_bp.route("/notes/add", methods=["GET", "POST"])
def add():
    if not current_user.is_authenticated:
        return redirect(url_for("main.main"))

    form = Add()
    if form.validate_on_submit():
        data = Notes(current_user.id, form.content.data, form.subject.data, form.grade.data, form.school_type.data,
                     form.chapter.data, form.privacy.data)
        db.session.add(data)
        db.session.commit()
        return redirect(url_for(".my_notes"))

    return render_template("add.html", form=form)

# exorbitantly shoddy code that works using the powers of allah
def notes_sql(current_args: MultiDict, demand_only_public = False, demand_only_own = False) -> TextClause:
    component = f"WHERE owner_id = {current_user.id}" if demand_only_own else ""
    clause = "WHERE" if not demand_only_own else "AND" # where if first clause, and if not first clause
    for i in current_args:
        if i == 'class':
            component += f" {clause} grade = \'{current_args['class']}\'"
            clause = "AND"
            break
        if i == 'subject':
            component += f" {clause} subject = \'{current_args['subject']}\'"
            clause = "AND"
            break
        if i == 'school':
            component += f" {clause} school_type = \'{current_args['school']}\'"
            clause = "AND"
            break
        if i == 'user_text' and current_args['user_text'] != "":
            component += f" {clause} content LIKE \'%{current_args['user_text']}%\'"
            clause = "AND"
            break
        if i == 'teacher':
            component += f"{clause} owner_id IN (SELECT id FROM user WHERE username = \'{current_args['teacher']}\')"
            clause = "AND"
            break
    if demand_only_public:
        component += f"{clause} private IS NULL OR private != 1"
    return text(f"SELECT * FROM note {component}")


@notes_bp.route("/notes/my_notes", methods=["GET", "POST"])
def my_notes():
    if not current_user.is_authenticated:
        return redirect(url_for("main.main"))
    query = notes_sql(request.args.copy(), False, True)
    output = list(run(query).fetchall())  # below: "own" field nonfunctional
    return render_template("show.html", curlink="my_notes", own=True, content=output, filtered=("AND" in query.text))

@notes_bp.route("/notes/browse_notes", methods=["GET", "POST"])
def browse_notes():
    query = notes_sql(request.args.copy(), True, False)
    output = [list(i)+
        [run(text(f"SELECT username FROM user WHERE id = {i[1]}")).fetchall()[0][0]]
        for i in db.get_engine().connect().execute(query).fetchall()]  # below: "own" field nonfunctional
    return render_template(
        "show.html", curlink="browse_notes", own=True, content=sample(output, len(output)), filtered=("AND" in query.text))

@notes_bp.route("/notes/render_note", methods=["GET", "POST"])
def render_single_note():
    note_id = ""
    user_id = ""
    current_args = request.args.copy()
    for i in current_args:
        if i == 'note':
            note_id = current_args['note']
            break
    else:
        return redirect("/notes/browse_notes")
    if current_user.is_authenticated:
        user_id = current_user.id
    query1 = f"SELECT * FROM note WHERE id = {note_id} " \
            f"{f'AND (owner_id = {user_id} OR private IS NULL OR private = 0)' if user_id != '' else ''}"
    results = run(text(query1)).fetchall()[0]
    query2 = f"SELECT username FROM user WHERE id = {results[1]}"
    author = run(text(query2)).fetchall()[0][0]
    print(results)
    if len(results) == 0:
        return redirect("/notes/browse_notes")
    return render_template("rendernote.html", note=results, author=author, note_id = note_id)
