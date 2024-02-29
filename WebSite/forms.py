from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField , BooleanField,PasswordField, EmailField, IntegerField, FloatField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired , NumberRange, Length

class SignUpForm(FlaskForm):
    email = EmailField('Email',validators=[DataRequired()])
    username = StringField('UserName',validators=[DataRequired(),Length(min=2)])
    password1 = PasswordField('Enter your password',validators=[DataRequired(),Length(min=6)])
    password2 = PasswordField('Confirm your password',validators=[DataRequired(),Length(min=6)])
    submit = SubmitField('Sign Up')

class Loginform(FlaskForm):
    email = EmailField("Email",validators=[DataRequired()])
    password = PasswordField("Enter your password",validators=[DataRequired()])
    submit = SubmitField("Login")