import werkzeug
from flask_login import current_user
from flask import render_template, Blueprint, abort

from werkzeug.exceptions import HTTPException

from src import app

main_bp = Blueprint('main', __name__, template_folder='templates', static_folder="static", static_url_path='/main-static')
@main_bp.route("/")
def main() -> str:  # main page render function isolated in file to get current status
    temp_username = current_user.username if current_user.is_authenticated else ""
    return render_template("main.html", username=temp_username)

# error handlers
@main_bp.route("/error/<path:error>")
def check_error(error):
    try:
        abort(int(error))
    except werkzeug.exceptions.HTTPException:
        abort(int(error))
    except Exception:
        abort(400)

@app.errorhandler(404)
def error_404(e):
    return render_template("error_handler.html", error=404, content=
    "This site does not exist")

@app.errorhandler(403)
def error_403(e):
    return render_template("error_handler.html", error=403, content=
    "You are not logged in or you have attempted to access files that are not yours.")

@app.errorhandler(418)
def error_418(e):
    return render_template("error_handler.html", error=418, content=
    "I'm a teapot.")

@app.errorhandler(400)
def error_400(e):
    return render_template("error_handler.html", error=400, content=
    "You have entered nonsensical data into your request.")

@app.errorhandler(500)
def error_500(e):
    return render_template("error_handler.html", error=500, content=
    "the error is on the server side. Refer to our GitHub issues page.")

@app.errorhandler(HTTPException)
def generic_error(e):
    return render_template("error_handler.html", error=e.code, content=e.description)
