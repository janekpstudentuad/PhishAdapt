from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField

class TrainingPreferencesForm(FlaskForm):
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