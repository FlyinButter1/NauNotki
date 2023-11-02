from flask.cli import FlaskGroup

from src import app, db

from src.models import *

cli = FlaskGroup(app)


if __name__ == "__main__":
    cli()
    
    
