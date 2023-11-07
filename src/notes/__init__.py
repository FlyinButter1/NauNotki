from flask import render_template, Blueprint, url_for, request, redirect, abort, make_response
from flask_login import current_user
from sqlalchemy import text, TextClause
from werkzeug.datastructures import MultiDict
from random import sample

from src import db
from .forms import Add, censorship_validator_string
from src.models import Notes

notes_bp = Blueprint(
    'notes', __name__, template_folder='templates', static_folder="static", static_url_path='/notes-static')

run = lambda x: db.get_engine().connect().execute(x)

@notes_bp.route("/notes/add", methods=["GET", "POST"])
def add():
    if not current_user.is_authenticated:
        return redirect(url_for("main.main"))

    form = Add()
    if form.validate_on_submit():
        data = Notes(current_user.id, '', form.subject.data, form.grade.data, form.school_type.data,
                     form.chapter.data, form.privacy.data)
        db.session.add(data)
        db.session.commit()
        return redirect(url_for(".my_notes"))

    return render_template("add.html", form=form)

# exorbitantly shoddy code that works using the powers of allah
def notes_sql(current_args: MultiDict, demand_only_public = False, demand_only_own = False) -> TextClause:
    component = f"WHERE owner_id = {current_user.id}" if demand_only_own else ""
    clause = "WHERE" if not demand_only_own else "AND"  # where if first clause, and if not first clause
    for i in current_args:
        if i == 'class' and current_args['class'] != "":
            component += f" {clause} grade = \'{current_args['class']}\'"
            clause = "AND"
        if i == 'subject' and current_args['subject'] != "":
            component += f" {clause} subject = \'{current_args['subject']}\'"
            clause = "AND"
        if i == 'school' and current_args['school'] != "":
            component += f" {clause} school_type = \'{current_args['school']}\'"
            clause = "AND"
        if i == 'user_text' and current_args['user_text'] != "":
            component += f" {clause} content LIKE \'%{current_args['user_text']}%\'"
            clause = "AND"
        if i == 'teacher':
            component += f"{clause} owner_id IN (SELECT id FROM user WHERE username = \'{current_args['teacher']}\')"
            clause = "AND"

    if demand_only_public:
        component += f"{clause} (private IS NULL OR private != 1)"
    return text(f"SELECT * FROM note {component}")


@notes_bp.route("/notes/my_notes", methods=["GET", "POST"])
def my_notes():
    if not current_user.is_authenticated:
        return redirect(url_for("main.main"))
    query = notes_sql(request.args.copy(), False, True)
    output = list(run(query).fetchall())  # below: "own" field nonfunctional
    return render_template("show.html", curlink="my_notes",
                           own=True, content=output, filtered=("AND" in query.text), username=current_user.username)

@notes_bp.route("/notes", methods=["GET", "POST"])
def browse_notes_redirect():
    return redirect(url_for("notes.browse_notes"))

@notes_bp.route("/notes/browse_notes", methods=["GET", "POST"])
def browse_notes():
    args = request.args.copy()  # public static void main(String[] args)
    if 'delete' in args:
        if not current_user.is_authenticated:
            abort(403)
        owner_id = run(text(f"SELECT owner_id FROM note WHERE id = {args['delete']}")).fetchall()
        if len(owner_id) != 0:
            owner_id = owner_id[0][0]
            if owner_id != current_user.id:
                abort(403)
            connection = db.get_engine().connect()
            connection.execute(text(f"DELETE FROM note WHERE id = {args['delete']}"))
            connection.commit()
            return redirect("/notes/browse_notes")
    query = notes_sql(args, True, False)
    output = [list(i)+
        [run(text(f"SELECT username FROM user WHERE id = {i[1]}")).fetchall()[0][0]]
        for i in db.get_engine().connect().execute(query).fetchall()]  # below: "own" field nonfunctional
    return render_template("show.html",
                           curlink="browse_notes", own=False, content=sample(output, len(output)),
                           filtered=("AND" in query.text))

@notes_bp.route("/notes/render_note/<path:note_id>", methods=["GET", "POST"])
def render_single_note(note_id):
    user_id = ""
    if current_user.is_authenticated:
        user_id = current_user.id
    query1 = f"SELECT * FROM note WHERE id = {note_id} " \
             f"{f'AND (owner_id = {user_id} OR private IS NULL OR private = 0)' if user_id != '' else ''}"
    results = run(text(query1)).fetchall()
    if len(results) != 1:
        abort(404)
    query2 = f"SELECT username FROM user WHERE id = {results[0][1]}"
    author = run(text(query2)).fetchall()[0][0]
    if len(results) == 0:
        return redirect("/notes/browse_notes")
    return render_template("rendernote.html", note=results[0], author=author, note_id = note_id)
@notes_bp.route("/notes/edit_note/<path:note_id>", methods=["GET", "POST"])
def edit_single_note(note_id):
    return render_template("edit.html", id=note_id)

@notes_bp.route("/notes/run_edit/<path:note_id>", methods=["POST"])
def run_edit_note(note_id):
    data = request.form.get('content')
    if not current_user.is_authenticated:
        abort(403)
    query1 = f"SELECT * FROM note WHERE id = {note_id} " \
             f"{f'AND (owner_id = {current_user.id} OR private IS NULL OR private = 0)' if current_user.id != '' else ''}"
    check_if_exists = run(text(query1)).fetchall()
    if not censorship_validator_string(data):
        abort(418)  # temporary
    if len(check_if_exists) != 1:
        abort(404)
    else:
        userid = check_if_exists[0][0]
        if userid != int(note_id):
            abort(403)
        if current_user.id != check_if_exists[0][1]:
            abort(403)
    connection = db.get_engine().connect()
    connection.execute(text(f"UPDATE note SET content = \'{data}\' WHERE id = {note_id}"))
    connection.commit()
    return make_response('', 201)
