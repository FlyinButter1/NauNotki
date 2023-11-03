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
        "Old password",
        validators=[DataRequired()]
        )
    
    newpassword = PasswordField(
        "New password",
        validators=[DataRequired()]
        )
    
    confirm = PasswordField(
        "Confirm new password",
        validators=[EqualTo("newpassword"), DataRequired(), notEqual('oldpassword', message = f"New password can't be the same as the old password")] 
    )