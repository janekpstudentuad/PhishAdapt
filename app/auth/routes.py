# Import Blueprint class instance
from app.auth import bp

# Import required libraries
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
import sqlalchemy as sa
from urllib.parse import urlsplit # Required for login reoute redirect

# Import required forms
from app.auth.forms import LoginForm
from app.auth.forms import ResetPasswordRequestForm, ResetPasswordForm

# Import functions from other Blueprints
from app.auth.email import send_password_reset_email

# Import classes from other functions
from app import db
from app.models import User

# Blueprint route for login page
@bp.route('/login', methods=['GET', 'POST'])
def login():
    # Redirect user to profile page if already authenticated
    if current_user.is_authenticated:
        return redirect(url_for('main.user', username=current_user.username))
    # Instantiate instance of login form
    form = LoginForm()
    # Attempt to login user if request to page submitted includes a completed form
    if form.validate_on_submit():
        # Set user as provided in form
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        # Provide error message if username cannot be found or password does not match db entry and redirect to login page
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        # Login user if all details correct as per db entry
        login_user(user, remember=form.remember_me.data)
        # Set page for redirect on successful login (user profile)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('main.user', username=user.username)
        # Redirect user
        return redirect(next_page)
    # Render login page if request contains no form data
    return render_template('auth/login.html', title='Sign In', form=form)

# Blueprint route for logout functionality
@bp.route('/logout', methods=['GET', 'POST'])
def logout():
    # Logout user
    logout_user()
    # Redirect to login page on logout
    return redirect(url_for('auth.login'))

# Blueprint route for page to request a password request
@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
     # Redirect user to profile page if already authenticated
    if current_user.is_authenticated:
        next_page = url_for('main.user', username=current_user.username)
    # Instantiate instance of ResetPasswordRequestForm
    form = ResetPasswordRequestForm()
    # Send email to user if request to page submitted includes a completed form
    if form.validate_on_submit():
        # Set user as provided in form
        user = db.session.scalar(sa.select(User).where(User.email == form.email.data))
        if user:
            # Send email if user found in db
            send_password_reset_email(user)
        # Provide information message to user
        flash('Check your email for the instructions to reset your password')
        # Redirect to login page
        return redirect(url_for('auth.login'))
    # Render reset_password_request page if request contains no form data
    return render_template('auth/reset_password_request.html', title='Reset Password', form=form)
        
# Blueprint route for reset password page
@bp.route('reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        # Redirect user to profile page if already authenticated
        next_page = url_for('main.user', username=current_user.username)
    # Set user as provided in decoded JWT token
    user = User.verify_reset_password_token(token)
    # Redirect to login page if JWT token does not contain a valid user
    if not user:
        return redirect(url_for('auth.login'))
    # Instantiate instance of ResetPasswordForm
    form = ResetPasswordForm()
    # Reset user password if request to page submitted includes a completed form
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        # Provide information message to user
        flash('Your password has been reset.')
        # Redirect to login page
        return redirect(url_for('auth.login'))
    # Render reset_password_request page if request contains no form data
    return render_template('auth/reset_password.html', form=form)