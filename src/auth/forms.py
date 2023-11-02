from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired
from src import db
from src.models import User

class Register(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired()],
        
    )
    
    email = EmailField(
        "Email",
        validators=[Email(), DataRequired()]
        
        )
    
    password = PasswordField(
        "Password",
        validators=[DataRequired()]
        )
    
    confirm = PasswordField(
        "Confirm Passowrd",
        validators=[EqualTo("password"), DataRequired()] 
    )

    role = RadioField(
        "Role",
        validators=[DataRequired()],
        choices=[("uczen","Uczeń"),("nauczyciel","Nauczyciel")]
    )
        
    
    def validate(self, extra_validators):
        default_validation =  super().validate(extra_validators)

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
        "Username",
        validators=[DataRequired()],
        
    )
    
    password = PasswordField(
        "Password",
        validators=[DataRequired()]
        )