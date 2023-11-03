from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from decouple import config
from flask_login import LoginManager, current_user
from src.main import main

app = Flask(__name__)
app.config.from_object(config("APP_SETTINGS"))

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

from src.auth.views import auth_bp

app.register_blueprint(auth_bp)

@app.route("/")
def index():
    return main()
