from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

class SignUpForm(FlaskForm):
    username = StringField(label="username")
    password1 = PasswordField(label="password1")
    password2 = PasswordField(label="password2")
    submit = SubmitField(label="submit")