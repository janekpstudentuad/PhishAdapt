from app.admin import bp
from flask import render_template, flash, redirect, url_for
from app.admin.forms import RegistrationForm
from flask_login import current_user, login_required
import sqlalchemy as sa
from app import db
from app.models import User, Organisation

@bp.route('/console')
@login_required
def console():
    return render_template('admin/console.html', title='Admin console')

@bp.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    form = RegistrationForm()
    departments = db.session.query(Organisation.department).distinct().all()
    form.department.choices = [(dept.department, dept.department) for dept in departments]
    teams = db.session.query(Organisation.team).distinct().all()
    form.team.choices = [(team.team, team.team) for team in teams]
    if form.validate_on_submit():
        user = User(
            username=form.username.data, 
            firstname=form.firstname.data, 
            lastname=form.lastname.data, 
            email=form.email.data, 
            jobtitle=form.jobtitle.data, 
            team=form.team.data, 
            department=form.department.data, 
            is_admin=form.isadmin.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        username = form.username.data
        flash(f'{username} is now a registered user.')
        return redirect(url_for('admin.console'))
    return render_template('admin/register.html', title='Register', form=form)