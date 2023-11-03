from flask_login import current_user
from flask import render_template
def main() -> str:  # main page render function isolated in file to get current status
    temp_username = current_user.username if current_user.is_authenticated else ""
    return render_template("main.html", username=temp_username)
