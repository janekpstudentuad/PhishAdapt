# Import required libraries
from flask import render_template, current_app

# Import functions from other Blueprints
from app.email import send_email

# Function for sending email to user with password reset link
def send_password_reset_email(user):
    # Set JWT for requesting user
    token = user.get_reset_password_token()
    # Set variables for send_email function
    send_email('[PhishAdapt] reset your password',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               ## Add text email option if email server/client requires
               # text_body=render_template('email/reset_password.txt', user=user, token=token),
               html_body=render_template('email/reset_password.html', user=user, token=token))