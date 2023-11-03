from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired, ValidationError
from src.models import User
from flask import url_for
from wtforms import ValidationError
import re
censorship_list = [i[:-2] for i in open("notes/static/censorship_filter.txt", 'r').readlines()[1:] if len(i) >= 3]
def grade_validator(form, field):
    try:  # exception-driven development ftw
        value = int(field.data)
        if value < 0:
            raise ValidationError("Field must be non-negative.")
    except ValueError:
        raise ValidationError("Field must be numeric.")

def censorship_validator(form, field):
    if any([re.match(i, field.data) for i in censorship_list]):
        raise ValidationError("Field must not contain offensive terminology.")

class Add(FlaskForm):
        
    subject = StringField(
        "Subject",
        validators=[DataRequired(), censorship_validator]
    )
    grade = StringField(
        "Grade",
        validators=[DataRequired(), grade_validator]
    )
    school_type = RadioField(
        "School type",
        validators=[DataRequired()],
        choices=[
            ("przedszkole","Przedszkole"),
            ("podstawowa","Szkoła podstawowa"),
            ("liceum","Liceum ogólnokształcące"),
            ("technikum","Technikum"),
            ("zawodowka","Szkoła zawodowa I lub II stopnia"),
            ("studia","Szkoła wyższa"),
            ("inne", "Inne")
        ]
    )
    chapter = StringField(
        "Chapter",
        validators=[DataRequired(), censorship_validator]
    )
    content = StringField(
        "Content",
        validators=[DataRequired(), censorship_validator]
    )
    privacy = RadioField(
        "Privacy",
        validators=[DataRequired()],
        choices=[
            ('1', 'private'),
            ('0', 'public')
        ]
    )

