# Import required libraries
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import Length

# Form for user edit profile functionality
class EditProfileForm(FlaskForm):
    firstname = StringField('First name', validators=[Length(min=0, max=16)])
    lastname = StringField('Last name', validators=[Length(min=0, max=16)])
    submit = SubmitField('Submit')

# Form for user edit training preferences functionality
class EditTrainingPreferences(FlaskForm):
    instructor = BooleanField('Tick here to add Instructor-led training to your training preferences: ')
    group = BooleanField('Tick here to add Group-based training to your training preferences: ')
    game = BooleanField('Tick here to add Gamification to your training preferences: ')
    elearn = BooleanField('Tick here to add e-Learning to your training preferences: ')
    quiz = BooleanField('Tick here to add Quizzes to your training preferences: ')
    demo = BooleanField('Tick here to add Demonstrations to your training preferences: ')
    video = BooleanField('Tick here to add Videos to your training preferences: ')
    text = BooleanField('Tick here to add Articles to your training preferences: ')
    visual = BooleanField('Tick here to add Visual training to your training preferences: ')
    coach = BooleanField('Tick here to add Coaching to your training preferences: ')
    audio = BooleanField('Tick here to add Audio training to your training preferences: ')
    submit = SubmitField('Submit')