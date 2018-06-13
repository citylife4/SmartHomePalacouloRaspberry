from flask_wtf import FlaskForm, Form
#from wtforms import Form, StringField, PasswordField, validators, SubmitField
from wtforms import StringField, PasswordField, validators, SubmitField
from wtforms import DateField
from datetime import date

from wtforms.validators import DataRequired, EqualTo, Email

from homedash.models import User


class LoginForm(Form):
    username = StringField('Username', [validators.DataRequired(), validators.input_required()])
    password = PasswordField('Password', [validators.DataRequired(), validators.input_required()])

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            print("TODO: ERROR")
            #aise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            print("TODO: ERROR")
            #raise ValidationError('Please use a different email address.')


class DateForm(Form):
    dt = DateField('Pick a Date', format="%m/%d/%Y")
