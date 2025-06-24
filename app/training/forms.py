from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField

class TrainingPreferencesForm(FlaskForm):
    instructor = BooleanField()
    group = BooleanField()
    game = BooleanField()
    elearn = BooleanField()
    quiz = BooleanField()
    demo = BooleanField()
    video = BooleanField()
    text = BooleanField()
    visual = BooleanField()
    coach = BooleanField()
    audio = BooleanField()
    submit = SubmitField('Submit')