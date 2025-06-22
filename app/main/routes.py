from app.main import bp
from flask import redirect, render_template, url_for, flash, request
from flask_login import login_required, current_user
from app import db
import sqlalchemy as sa
from app.models import User
from app.main.forms import EditProfileForm

@bp.route('/')
@bp.route('/index')
def index():
    return redirect(url_for('auth.login'))

@bp.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    return render_template('user.html', user=user, title='User Profile')

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