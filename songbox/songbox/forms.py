"""Signup & login forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional


class SignupForm(FlaskForm):
    """User Signup Form."""
    name = StringField('Name',
                       validators=[DataRequired()])
    email = StringField('Email',
                        validators=[Length(min=6),
                                    Email(message='Enter a valid email.'),
                                    DataRequired()])
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         Length(min=6, message='Select a stronger password.')])
    confirm = PasswordField('Confirm The Password',
                            validators=[DataRequired(),
                                        EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    """User Login Form."""
    email = StringField('Email', validators=[DataRequired(),
                                             Email(message='Enter a valid email.')])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class PlaylistForm(FlaskForm):
    """ Playlist Form"""
    sequence = IntegerField('Song Sequence No.',
                       validators=[DataRequired()])
    name = StringField('Playlist Name',
                       validators=[DataRequired()])
    song_id = IntegerField('Song ID No.',
                       validators=[DataRequired()])
    user_id = IntegerField('User ID No.',
                       validators=[DataRequired()])

