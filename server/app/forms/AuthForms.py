"""Signup & login forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional


class SignupForm(FlaskForm):
    class Meta:
      csrf = False

    email = StringField('email',
      validators=[Length(min=6),
      Email(message='Enter a valid email.'),
      DataRequired()])
    password = PasswordField('password',
      validators=[DataRequired(),
      Length(min=6, message='Select a stronger password.')])
    confirm = PasswordField('confirm',
      validators=[DataRequired(),
      EqualTo('password', message='Passwords must match.')])
    isAgree = BooleanField('isAgree')


class LoginForm(FlaskForm):
    class Meta:
      csrf = False

    email = StringField('email', validators=[DataRequired(),
      Email(message='Enter a valid email.')])
    password = PasswordField('password', validators=[DataRequired()])