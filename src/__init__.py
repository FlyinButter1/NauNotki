import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from decouple import config
from flask_login import LoginManager
from ctypes import CDLL

app = Flask(__name__)
app.config.from_object(config("APP_SETTINGS"))

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
mylibrary = CDLL("./src/static/c/bmp64lib.dll")

# run app outside of src with flask --app src:app

login_manager = LoginManager()
login_manager.init_app(app)

from src.auth.views import auth_bp
from src.main import main_bp
from src.notes import notes_bp
from src.panel import panel_bp
from src.flashcards import flashcards_bp

app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(notes_bp)
app.register_blueprint(panel_bp)
app.register_blueprint(flashcards_bp)

with app.app_context(): 
    db.create_all()