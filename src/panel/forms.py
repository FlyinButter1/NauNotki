from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

def notEqual(second_field, message):
    

    def _notEqual(form, field):
        if field.data == form[second_field].data:
            raise ValidationError(message)

    return _notEqual

class ChangePassword(FlaskForm):
    oldpassword = PasswordField(
        "Stare hasło",
        validators=[DataRequired()]
        )
    
    newpassword = PasswordField(
        "Nowe hasło",
        validators=[DataRequired()]
        )
    
    confirm = PasswordField(
        "Potwierdź nowe hasło",
        validators=[EqualTo("newpassword"), DataRequired(), notEqual('oldpassword', message = f"Nowe hasło nie może być takie same jak stare hasło.")] 
    )