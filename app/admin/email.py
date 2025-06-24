from flask import render_template, current_app
from app.email import send_email

def send_baseline_voicemail(user):
    token = user.get_training_token()
    send_email(f'Voicemail for {user.username}',
               sender='voicemail@company.com',
               recipients=[user.email],
               # text_body=render_template('email/reset_password.txt', user=user, token=token),
               html_body=render_template('email/baseline_voicemail.html', user=user, token=token))