from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from .models import User

class RegisterForm(FlaskForm):
    email = EmailField(validators=[InputRequired(), Length(
        min=5, max=50)], render_kw={"placeholder": "example@email.com"})
    
    username = StringField(validators=[InputRequired(), Length(
        min=3, max=30)], render_kw={"placeholder": "Username"})
    
    password1 = PasswordField(validators=[InputRequired(), Length(
        min=5, max=30)], render_kw={"placeholder": "Password"})
    
    password2 = PasswordField(validators=[InputRequired(), Length(
    min=5, max=30)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        
        if existing_user_username:
            raise ValidationError(
                "That username already exists. Please choose a different one."
            )
        
class LoginForm(FlaskForm):
    email = EmailField(validators=[InputRequired(), Length(
        min=5, max=50)], render_kw={"placeholder": "example@email.com"})
    
    password = PasswordField(validators=[InputRequired(), Length(
        min=5, max=30)], render_kw={"placeholder": "Password"})


    submit = SubmitField("Register")
