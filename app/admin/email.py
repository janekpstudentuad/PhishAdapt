from flask import render_template, current_app
from app.email import send_email
from app.utils.jwt_tokens import get_training_token
from app.models import Profile

def send_voicemail(user, campaign):
    token = get_training_token(user.id, campaign.id)
    send_email(f'Voicemail for {user.username}',
               sender='voicemail@company.com',
               recipients=[user.email],
               html_body=render_template('email/baseline_voicemail.html', user=user, token=token))

def send_training_invitation(user):
    profile = Profile.query.filter_by(user_id=user.id).first()
    send_email(f'Training recommendations for {user.username}',
    sender='voicemail@company.com',
    recipients=[user.email],
    html_body=render_template('email/training_invite.html', user=user, profile=profile))