import sys

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from decouple import config
from flask_login import LoginManager
from ctypes import CDLL
import os
import dotenv

app = Flask(__name__)
app.config.from_object(config("APP_SETTINGS"))

if os.path.isfile(".env"):
    dotenv.load_dotenv(".env")

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
mylibrary = ""
if sys.platform.startswith('win'):
    mylibrary = CDLL("./src/static/c/bmp64lib.dll")
elif sys.platform.startswith('linux'):
    mylibrary = CDLL("./src/static/c/bmp64lib.so")
else:
    raise Exception('Unidentified operating system.')

# run app outside of src with flask --app src:app

login_manager = LoginManager()
login_manager.init_app(app)

from src.auth.views import auth_bp
from src.main import main_bp
from src.notes import notes_bp
from src.panel import panel_bp
from src.flashcards import flashcards_bp
from src.test import test_bp

app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(notes_bp)
app.register_blueprint(panel_bp)
app.register_blueprint(flashcards_bp)
app.register_blueprint(test_bp)

from src.models import User, Flashcards, Notes

with app.app_context():
    db.create_all()
