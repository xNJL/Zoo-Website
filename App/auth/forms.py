from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from ..__init__ import db


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         EqualTo('confirm', message='Passwords must match.')])
    confirm = PasswordField('Confirm password', validators=[DataRequired()])
    user_type = BooleanField('Staff')
    submit = SubmitField('Register')

    def validate_username(self, username):
        sql = f"SELECT * FROM fake_db.USER WHERE USERNAME ='{username.data}'"
        result = db.query(sql).fetchone()
        if result is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        sql = f"SELECT * FROM fake_db.USER WHERE EMAIL ='{email.data}'"
        result = db.query(sql).fetchone()
        if result is not None:
            raise ValidationError('Please use a different email address.')

    def validate_password(self, password):
        if len(password.data) < 8:
            raise ValidationError('Password must be at least 8 characters')