from app.main import bp
from flask import redirect, render_template, url_for, flash, request
from flask_login import login_required, current_user
from app import db
import sqlalchemy as sa
from app.models import User, Profile
from app.main.forms import EditProfileForm, EditTrainingPreferences
import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

@bp.route('/')
@bp.route('/index')
def index():
    return redirect(url_for('auth.login'))

@bp.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    profile = db.session.scalar(sa.select(Profile).where(Profile.user_id == user.id))
    risk = profile.risk if profile and profile.risk is not None else 0

    fig, ax = plt.subplots(figsize=(5, 1.2))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.add_patch(Rectangle((0, 0), 40, 1, color = 'green'))
    ax.add_patch(Rectangle((40, 0), 30, 1, color = 'orange'))
    ax.add_patch(Rectangle((70, 0), 30, 1, color = 'red'))

    ax.plot([risk, risk], [0, 1], color='black', linewidth=5)

    ax.text(50, 1.1, f'Risk score: {risk}', ha='center', fontsize=12, fontweight='bold')

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', transparent=True, dpi=100, bbox_inches='tight')
    buf.seek(0)
    gauge_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)

    return render_template('user.html', user=user, profile=profile, title='User Profile', gauge_image=gauge_base64)

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
    return render_template('edit_profile.html', title='Edit Profile', form=form, user=user)

@bp.route('/edit_training_preferences', methods=['GET', 'POST'])
@login_required
def edit_training_preferences():
    form = EditTrainingPreferences()
    profile = Profile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        profile = Profile(user_id=current_user.id)
        db.session.add(profile)
        db.session.commit()
    if form.validate_on_submit():
        profile.instructor = form.instructor.data
        profile.group = form.group.data
        profile.game = form.game.data
        profile.elearn = form.elearn.data
        profile.quiz = form.quiz.data
        profile.demo = form.demo.data
        profile.video = form.video.data
        profile.text = form.text.data
        profile.visual = form.visual.data
        profile.coach = form.coach.data
        profile.audio = form.audio.data
        
        db.session.commit()
        flash('Your training preferences have been saved!')
        return redirect(url_for('main.user', username=current_user.username))
    
    return render_template('edit_training_preferences.html', title='Edit Training Preferences', form=form, profile=profile)