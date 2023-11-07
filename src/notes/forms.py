from flask_wtf import FlaskForm
from wtforms import StringField, RadioField
from wtforms.validators import DataRequired
from wtforms import ValidationError
import re

# censorship list shamelessly stolen from polish wikipedia, source in file
censorship_list = [i[:-2] for i in open("src/notes/static/censorship_filter.txt", 'r').readlines()[1:] if len(i) >= 3]

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

def censorship_validator_string(field: str):
    if any([re.match(i, field) for i in censorship_list]):
        return False
    return True

class Add(FlaskForm):
    subject = StringField(
        "Przedmiot",
        validators=[DataRequired(), censorship_validator]
    )
    grade = StringField(
        "Klasa",
        validators=[DataRequired(), grade_validator]
    )
    school_type = RadioField(
        "Rodzaj szkoły",
        validators=[DataRequired()],
        choices=[
            ("przedszkole", "Przedszkole"),
            ("podstawowa", "Szkoła podstawowa"),
            ("liceum", "Liceum ogólnokształcące"),
            ("technikum", "Technikum"),
            ("zawodowka", "Szkoła zawodowa I lub II stopnia"),
            ("studia", "Szkoła wyższa"),
            ("inne", "Inne")
        ]
    )
    chapter = StringField(
        "Temat",
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

