# Import Blueprint class instance
from app.training import bp

# Import required libraries
from flask import render_template, url_for, redirect, flash
from flask_login import login_required, current_user

# Import classes from other functions
from app.models import User, Profile, CampaignResult
from app import db

# Import required forms
from app.main.forms import EditTrainingPreferences

# Import functions from other Blueprints
from app.utils.jwt_tokens import verify_training_token

# Blueprint route for training content page
@bp.route('/content')
@login_required
def content():
    # Render training content page
    return render_template('training/content.html', title="Training content")

@bp.route('/clicked/<token>', methods=['GET', 'POST'])
def clicked(token):
    # Check if user is already authenticated
    if current_user.is_authenticated:
        next_page = url_for('main.user', username=current_user.username)
    # Verify that JWT in URL is valid
    user_id, campaign_id = verify_training_token(token)
    # Redirect user to login page if no user ID or campaign ID supplied
    if not user_id or not campaign_id:
        return redirect(url_for('auth.login'))
    # Get user info from db
    user = db.session.get(User, user_id)
    # Redirect user to login page if no valid user ID supplied
    if not user:
        return redirect(url_for('auth.login'))
    # Query db to find campaign details
    result = CampaignResult.query.filter_by(user_id=user_id, campaign_id=campaign_id).first()
    # Set data in "clicked" column of campaign results table to True for user
    # and bump risk ONLY when arriving via GET AND this is the first time clicked.
    if request.method == 'GET' and result and not result.clicked:
        result.clicked = True

    # Select profile from db
    profile = Profile.query.filter_by(user_id=user.id).first()

    # Create profile entry in db for user if one does not already exist and set initial risk score
    if not profile:
        profile = Profile(user_id=user.id, risk=10)
        db.session.add(profile)
    # Increase user risk score if profile already exists, cannot exceed 100
    else:
        profile.risk = min((profile.risk or 0) + 10, 100)

    db.session.commit()

    # Ensure a profile exists for form binding (no risk change here)
    profile = Profile.query.filter_by(user_id=user.id).first()
    if not profile:
        profile = Profile(user_id=user.id, risk=0)  # do NOT bump risk here
        db.session.add(profile)
        db.session.commit()

    # Instantiate edit training preferences form
    form = EditTrainingPreferences()
    
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
        # Redirect user back to login page on completion
        return redirect(url_for('auth.login'))

    # Render edit training preference page if request contains no form data
    return render_template('training/clicked.html', title="Invitation to training", form=form)