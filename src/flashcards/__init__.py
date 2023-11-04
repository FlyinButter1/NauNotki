from flask import Blueprint, redirect, url_for, request, render_template, jsonify
from flask_login import current_user
from src.models import Notes, Flashcards
from src import db
from sqlalchemy.sql import text
from decouple import config
import openai
import json
from src.auth.views import login_manager

flashcards_bp = Blueprint('flashcards_bp', __name__, template_folder='templates', static_folder="static", static_url_path='/flashcards-static')
openai.api_key = config("OPENAI_API_KEY")

@flashcards_bp.route("/flashcards/api/generate")
def generate():

    note_id = request.args['note']

    note = Notes.query.filter_by(id=note_id).first()

    if not current_user.is_authenticated or note.has_flashcards:
        return ""
    

    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {
        "role": "system",
        "content": "Jesteś nauczycielem, który tworzy fiszki z notatek. Fiszki podaj jako json według wzoru [{\"front\":\"content\", \"back\":\"content\"}, ...]."
        },
        {
        "role": "user",
        "content": f"{note.content}"
        }
    ],
    temperature=1,
    max_tokens=1000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )

    result = json.loads(response.choices[0].message.content)

    for i in result:
        flashcard = Flashcards(note_id, i["front"], i["back"])
        db.session.add(flashcard)
        db.session.commit()

    note.has_flashcards = True
    db.session.commit()

    return '{"result":"success"}'

@flashcards_bp.route("/flashcards/api/get")
def get():
    note_id = request.args['note']

    note = Notes.query.filter_by(id=note_id).first()

    if note is None or not note.has_flashcards or (note.private and note.owner_id != current_user.id):
        return ""

    flashcards = Flashcards.query.filter_by(note_id=note_id)

    response = []

    for i in flashcards:
        response.append({'id':i.id, 'front':i.front, 'back':i.back, 'box':i.box})

    return jsonify(response)

@flashcards_bp.route("/flashcards")
def flashcards():
    if not current_user.is_authenticated:
        return redirect(url_for("main.main"))

    note_id = request.args['note']

    note = Notes.query.filter_by(id=note_id).first()

    if note is None or (note.private and note.owner_id != current_user.id):
        return redirect(url_for("main.main"))
    
    if Flashcards.query.filter_by(note_id=note_id).first() is None:  
        return render_template("generowanie.html", note_id=note_id)
        
    else:
        return render_template("render_flashcards.html")
            


        