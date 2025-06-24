from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo
import sqlalchemy as sa
from app import db
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email address', validators=[DataRequired(), Email()])
    jobtitle = StringField('Job Title', validators=[DataRequired()])
    team = SelectField('Team', choices = [], validators=[DataRequired()])
    department = SelectField('Department', choices = [], validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    isadmin = BooleanField('Admin?')
    submit = SubmitField('Register')

class BaselineCampaign(FlaskForm):
    send = SubmitField('Send Campaign!')