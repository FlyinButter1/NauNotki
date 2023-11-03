from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from decouple import config
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(config("APP_SETTINGS"))

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
# censorship list shamelessly stolen from polish wikipedia

# run app ouside of src with flask --app src:app

login_manager = LoginManager()
login_manager.init_app(app)

from src.auth.views import auth_bp
from src.main import main_bp
from src.notes import notes_bp


app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(notes_bp)

with app.app_context(): 
    db.create_all()