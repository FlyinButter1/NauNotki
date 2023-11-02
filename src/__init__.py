from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from decouple import config
from flask_login import LoginManager



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
    return "strona główna"