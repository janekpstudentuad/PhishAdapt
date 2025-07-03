# Import required libraries
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange

# Form for user seach on admin console page
class UserSearch(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    search = SubmitField('Search')

# Form for registering new users
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

# Form for running baseline campaign
class BaselineCampaign(FlaskForm):
    send = SubmitField('Send Campaign!')

# Form to generate departmental dropdown list for Campaign filter
class DepartmentalGroups(FlaskForm):
    department = SelectField(choices = [], validators=[DataRequired()])
    send = SubmitField('Send Campaign!')

# Form to generate risk score dropdown lists for Campaign filter
class RiskGroups(FlaskForm):
    operator = SelectField(choices = [], validators=[DataRequired()])
    score = IntegerField(validators=[DataRequired(), NumberRange(min=0, max=100, message='Enter a value between 0 and 100')])
    send = SubmitField('Send Campaign!')

# Form to generate dropdown lists for user list filter
class FilterUsers(FlaskForm):
    department = SelectField('Department', choices = [])
    score_operator = SelectField('Risk score', choices = [])
    score = IntegerField()
    training_preference = SelectField('Training Preference')
    submit = SubmitField('Filter')

# Form for editing existing user information
class EditUser(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email address', validators=[DataRequired(), Email()])
    jobtitle = StringField('Job Title', validators=[DataRequired()])
    current_team = StringField('Current Team')
    new_team = SelectField('New Team', choices = [], validators=[DataRequired()])
    current_department = StringField('Current Department')
    new_department = SelectField('New Department', choices = [], validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    isadmin = BooleanField('Admin?')
    update = SubmitField('Update user')

# Form for deleting existing user
class DeleteUser(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    delete = SubmitField('Delete User')


# Form to generate name dropdown list for Campaign Result filter
class FilterCampaigns(FlaskForm):
    campaign = SelectField('Campaign Name', choices=[])
    submit = SubmitField('Filter')
    send = SubmitField('Send')

# Form for admin reset password function
class ResetUserPassword(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    update = SubmitField('Update password')