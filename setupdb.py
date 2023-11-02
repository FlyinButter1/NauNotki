from src import db, app
from src.models import *

with app.app_context(): 
    db.create_all()