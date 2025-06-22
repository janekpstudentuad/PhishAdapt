from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length

class EditProfileForm(FlaskForm):
    firstname = StringField('First name', validators=[Length(min=0, max=16)])
    lastname = StringField('Last name', validators=[Length(min=0, max=16)])
    submit = SubmitField('Submit')