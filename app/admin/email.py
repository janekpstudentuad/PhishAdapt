# Import required libraries
from flask import render_template, current_app

# Import functions from other Blueprints
from app.email import send_email
from app.utils.jwt_tokens import get_training_token

# Import classes from other functions
from app.models import Profile

# Function for sending voicemail training campaign email to user with user-specific link
def send_voicemail(user, campaign):
    # Create JWT token
    token = get_training_token(user.id, campaign.id)
    # Set variables for send_email function
    send_email(f'Voicemail for {user.username}',
               sender='voicemail@company.com',
               recipients=[user.email],
               html_body=render_template('email/baseline_voicemail.html', user=user, token=token))

# Function for sending training invitation email to user with user-specific link
def send_training_invitation(user):
    # Obtain user profile details
    profile = Profile.query.filter_by(user_id=user.id).first()
    # Set variables for send_email function
    send_email(f'Training recommendations for {user.username}',
                sender='voicemail@company.com',
                recipients=[user.email],
                html_body=render_template('email/training_invite.html', user=user, profile=profile))