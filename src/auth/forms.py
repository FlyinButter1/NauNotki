from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, RadioField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired
from src import db
from src.models import User
from src.notes.forms import censorship_validator

class Register(FlaskForm):
    username = StringField(
        "",
        validators=[DataRequired()],
        render_kw={'placeholder': 'Enter username'}
    )
    
    email = EmailField(
        "",
        validators=[Email(), DataRequired()],
        render_kw={'placeholder': 'Enter email'}
        )
    
    password = PasswordField(
        "",
        validators=[DataRequired()]
        )
    
    confirm = PasswordField(
        "",
        validators=[EqualTo("password"), DataRequired()],
        render_kw={'placeholder': 'Enter password again'}
    )

    role = SelectField(
        "Rola",
        validators=[DataRequired()],
        choices=[("uczen","Uczeń"),("nauczyciel","Nauczyciel")]
    )

    # the None default for extra_validators is there only for IDE to stop reporting nonexistent errors
    def validate(self, extra_validators=None) -> bool:
        default_validation = super().validate(extra_validators)

        if not default_validation:
            return False
        
        if not User.query.filter_by(username = self.username.data).first() is None:
            self.username.errors.append("Username in use")
            return False
        if not User.query.filter_by(email = self.email.data).first() is None:
            self.username.errors.append("Email in use")
            return False
        return True

class Login(FlaskForm):
        
    username = StringField(
        "",
        validators=[DataRequired()],
        
    )
    
    password = PasswordField(
        "",
        validators=[DataRequired()]
        )
