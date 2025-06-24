from flask import render_template, url_for, redirect
from flask_login import login_required, current_user
from app.training import bp
from app.models import User, Profile
from app import db
from app.training.forms import TrainingPreferencesForm

@bp.route('/content')
@login_required
def content():
    return render_template('training/content.html', title="Training content")

@bp.route('/clicked/<token>', methods=['GET', 'POST'])
def clicked(token):
    if current_user.is_authenticated:
        next_page = url_for('main.user', username=current_user.username)
    user = User.verify_training_token(token)
    if not user:
        return redirect(url_for('auth.login'))
    form = TrainingPreferencesForm()
    profile = Profile.query.filter_by(user_id=user.id).first()
    if not profile:
        profile = Profile(user_id=user.id, risk=10)
        db.session.add(profile)
    else:
        profile.risk = min(profile.risk + 10, 100)
    
    db.session.commit()

    return render_template('training/clicked.html', title="Invitation to training", form=form)