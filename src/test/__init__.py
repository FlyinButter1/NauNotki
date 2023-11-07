from flask import Blueprint, render_template, request, redirect, jsonify, url_for
from flask_login import current_user
from src.models import Notes
import openai
from decouple import config
import json

test_bp = Blueprint("test_bp", __name__, template_folder="templates", static_folder="static", static_url_path='/tets-static')

openai.api_key = config("OPENAI_API_KEY")

@test_bp.route("/test/api/get_test")
def test_api():
    note_id = request.args['note']

    note = Notes.query.filter_by(id=note_id).first()

    if not current_user.is_authenticated or (note.private and note.owner_id != current_user.id):
        return ""

    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {
        "role": "system",
        "content": "Jesteś nauczycielem, który tworzy test na podstawie notatek. test podaj jako json według wzoru '[{\"pytanie\":\"content\", \"a\":\"content\", \"b\":\"content\", \"c\":\"content\", \"d\":\"content\", \"poprawna\":\"content\"} , ...]'."        },
        {
        "role": "user",
        "content": f"{note.content}"
        }
    ],
    temperature=1,
    max_tokens=4000,
    top_p=1,
    frequency_penalty=0.2,
    presence_penalty=0
    )

    return jsonify(json.loads(response.choices[0].message.content))


@test_bp.route("/test")
def test():

    note_id = request.args['note']

    note = Notes.query.filter_by(id=note_id).first()

    if not current_user.is_authenticated or note is None or (note.private and note.owner_id != current_user.id):
        return redirect(url_for("main.main"))

    return render_template("test.html")
