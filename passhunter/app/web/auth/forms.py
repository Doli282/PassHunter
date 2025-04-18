"""Forms for the authentication of the PassHunter web application."""
from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional

from app.validators import validate_email


class LoginForm(FlaskForm):
    """Form for logging in"""
    email = EmailField('Email', validators=[DataRequired(), Length(max=255,
                                                                   message='The maximal length of accepted input is 255 characters.'),
                                            Email(message='Input must adhere to email structure.')],
                       description='Email address for logging in')
    password = PasswordField('Password', validators=[DataRequired()], description='Password to log in')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    """Form for registering a new user"""
    email = EmailField('Email', validators=[DataRequired(), Length(max=255,
                                                                   message='The maximal length of accepted input is 255 characters.'),
                                            Email(message='Input must adhere to email structure.'), validate_email],
                       description='Email address for logging in')
    name = StringField('Name', validators=[Optional(), Length(max=255,
                                                              message='The maximal length of accepted input is 255 characters.')],
                       description='Name of the user')
    password = PasswordField('Password', validators=[DataRequired()], description='Password to log in')
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password',
                                                                                             message="Provided passwords must be the same.")],
                                     description='Confirm the password')
    submit = SubmitField('Register')
