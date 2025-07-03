# Import Blueprint class instance
from app.main import bp

# Import required libraries
from flask import redirect, render_template, url_for, flash, request
from flask_login import login_required, current_user
import sqlalchemy as sa
import io # For use with user profile (displaying risk score gauge)
import base64 # For use with user profile (displaying risk score gauge)
import matplotlib # For use with user profile (displaying risk score gauge)
matplotlib.use('Agg') # Needed for matplotlib to function in headless environment
import matplotlib.pyplot as plt # For use with user profile (displaying risk score gauge)
from matplotlib.patches import Rectangle # For use with user profile (displaying risk score gauge)

# Import classes from other functions
from app import db
from app.models import User, Profile

# Import required forms
from app.main.forms import EditProfileForm, EditTrainingPreferences

# Blueprint route for index/home page
@bp.route('/')
@bp.route('/index')
def index():
    # Redirect to login page
    return redirect(url_for('auth.login'))

# Blueprint route for user profile page
@bp.route('/user/<username>')
@login_required
def user(username):
    # Set user variable for use with retrieving profile details
    user = db.first_or_404(sa.select(User).where(User.username == username))
    # Select profile from db
    profile = db.session.scalar(sa.select(Profile).where(Profile.user_id == user.id))
    # Set risk to 0 if no risk in profile otherwise retrieve risk score from profile
    risk = profile.risk if profile and profile.risk is not None else 0

    # Set plot size for displaying risk score gauge
    fig, ax = plt.subplots(figsize=(5, 1.2))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Set colour scheme and limits for gauge display
    ax.add_patch(Rectangle((0, 0), 40, 1, color = 'green'))
    ax.add_patch(Rectangle((40, 0), 30, 1, color = 'orange'))
    ax.add_patch(Rectangle((70, 0), 30, 1, color = 'red'))

    # Set gauge line properties
    ax.plot([risk, risk], [0, 1], color='black', linewidth=5)

    # Set display text for risk score gauge
    ax.text(50, 1.1, f'Risk score: {risk}', ha='center', fontsize=12, fontweight='bold')

    # Concert matplotlib object to base64 for embedding into page
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', transparent=True, dpi=100, bbox_inches='tight')
    buf.seek(0)
    gauge_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)

    # Render user profile page
    return render_template('user.html', user=user, profile=profile, title='User Profile', gauge_image=gauge_base64)

# Blueprint route for user edit profile page
@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    # Instantiate instance of edit profile form
    form = EditProfileForm()
    # Change profile details as per form input if request to page submitted includes a completed form
    if form.validate_on_submit():
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        db.session.commit()
        # Display information message to user
        flash('Your changes have been saved.')
        # Redirect to profile page on completion
        return redirect(url_for('main.edit_profile'))
    # Prefill form with existing information if request to page not made through submit button
    elif request.method == 'GET':
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
    # Render user edit profile page if request contains no form data
    return render_template('edit_profile.html', title='Edit Profile', form=form, user=user)

# Blueprint route for user edit training preferences page
@bp.route('/edit_training_preferences', methods=['GET', 'POST'])
@login_required
def edit_training_preferences():
    # Select profile from db
    profile = Profile.query.filter_by(user_id=current_user.id).first()
    # Instantiate instance of edit training preferences form, prefill with existing profile preferences
    form = EditTrainingPreferences(obj=profile)
    # Create profile entry in db for user if one does not already exist
    if not profile:
        profile = Profile(user_id=current_user.id)
        db.session.add(profile)
        db.session.commit()
    # Set user training preferences as per form input if request to page submitted includes a completed form
    if form.validate_on_submit():
        profile.game = form.game.data
        profile.quiz = form.quiz.data
        profile.video = form.video.data
        profile.text = form.text.data

        ### Fields below to be added when new content added to platform
        # profile.instructor = form.instructor.data
        # profile.group = form.group.data
        # profile.elearn = form.elearn.data
        # profile.demo = form.demo.data
        # profile.visual = form.visual.data
        # profile.coach = form.coach.data
        # profile.audio = form.audio.data
        
        db.session.commit()

        # Display info message to user
        flash('Your training preferences have been saved!')
        # Redirect user back to user profile page on completion
        return redirect(url_for('main.user', username=current_user.username))
    
    # Render edit training preference page if request contains no form data
    return render_template('edit_training_preferences.html', title='Edit Training Preferences', form=form, profile=profile)

# Blueprint route for personalised training page
@bp.route('/user/<username>/personalised_training')
@login_required
def personalised_training(username):
    # Set user variable for use with retrieving profile details
    user = db.first_or_404(sa.select(User).where(User.username == username))
    # Select profile from db
    profile = Profile.query.filter_by(user_id=user.id).first()
    # Render personalised training page
    return render_template('personalised_training.html', user=user, title='Personalised training recommendations', profile=profile)