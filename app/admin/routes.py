from app.admin import bp
from flask import render_template, flash, redirect, url_for, abort, request
from app.admin.forms import RegistrationForm, BaselineCampaign, DepartmentalGroups, RiskGroups, FilterUsers, UserSearch, EditUser, DeleteUser, FilterCampaigns, ResetUserPassword
from flask_login import current_user, login_required
import sqlalchemy as sa
from app import db
from app.models import User, Organisation, Profile, Campaign, CampaignResult
from app.admin.email import send_voicemail, send_training_invitation
import operator
from datetime import datetime
from sqlalchemy import func

@bp.route('/console', methods=['GET', 'POST'])
@login_required
def console():
    if not current_user.is_admin:
        abort(403)
    form = UserSearch()
    if form.validate_on_submit():
        target = form.username.data
        return redirect(url_for('admin.edit_user', target=target))
    return render_template('admin/console.html', title='Admin console', form=form)

@bp.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if not current_user.is_admin:
        abort(403)
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
        profile = Profile(user_id=user.id, risk=0)
        db.session.add(profile)
        db.session.commit()
        username = form.username.data
        flash(f'{username} is now a registered user.')
        return redirect(url_for('admin.console'))
    return render_template('admin/register.html', title='Register', form=form)

@bp.route('/campaigns')
@login_required
def campaigns():
    if not current_user.is_admin:
        abort(403)
    return render_template('admin/campaigns.html', title='Training Campaigns')

@bp.route('/campaigns/baselines')
@login_required
def baselines():
    if not current_user.is_admin:
        abort(403)
    return render_template('admin/baselines.html', title='Baseline Training Campaigns')

@bp.route('/campaigns/baselines/voicemail', methods=['GET', 'POST'])
@login_required
def baseline_voicemail():
    if not current_user.is_admin:
        abort(403)
    form = BaselineCampaign()
    if form.validate_on_submit():
        campaign = Campaign(name=f'Baseline Voicemail {datetime.now().strftime("%d%m%Y")}')
        db.session.add(campaign)
        db.session.commit()
        users = db.session.query(User).all()
        for user in users:
            send_voicemail(user, campaign)
            result = CampaignResult(campaign_id=campaign.id, user_id=user.id, username=user.username)
            db.session.add(result)
        db.session.commit()
        flash('Baseline voicemail campagn has been sent to all users!')
        return redirect(url_for('admin.console'))
    return render_template('admin/baseline_voicemail.html', title='Baseline Voicemail Campaign', form=form)

@bp.route('/campaigns/targeted_campaigns')
@login_required
def targeted_campaigns():
    if not current_user.is_admin:
        abort(403)
    return render_template('admin/targeted_campaigns.html', title='Targeted Training Campaigns')

@bp.route('/campaigns/target_campaigns/group_voicemail', methods=['GET', 'POST'])
@login_required
def group_voicemail():
    if not current_user.is_admin:
        abort(403)
    form = DepartmentalGroups()
    departments = db.session.query(Organisation.department).distinct().all()
    form.department.choices = [(dept.department, dept.department) for dept in departments]
    if form.validate_on_submit():
        department = form.department.data
        campaign = Campaign(name=f'Targeted {department} Voicemail {datetime.now().strftime("%d%m%Y")}')
        db.session.add(campaign)
        db.session.commit()
        users = db.session.query(User).where(User.department == department).all()
        for user in users:
            send_voicemail(user, campaign)
            result = CampaignResult(campaign_id=campaign.id, user_id=user.id, username=user.username)
            db.session.add(result)
        db.session.commit()
        flash(f'Targeted voicemail campagn has been sent to all users in {department}!')
        return redirect(url_for('admin.console'))
    return render_template('admin/group_voicemail.html', title='Voicemail Phishing Campaign for Departmental Groups', form=form)

@bp.route('/campaigns/target_campaigns/risk_voicemail', methods=['GET', 'POST'])
@login_required
def risk_voicemail():
    if not current_user.is_admin:
        abort(403)
    form=RiskGroups()
    form.operator.choices = [('>', '>'), ('>=', '>='), ('<', '<'), ('<=', '<='), ('==', '==')]
    if form.validate_on_submit():
        op_map = {'>': operator.gt, '>=': operator.ge, '<': operator.lt, '<=': operator.le, '==': operator.eq}
        op_func = op_map[form.operator.data]
        score = form.score.data
        campaign = Campaign(name=f'Risk Score {form.operator.data} {score} Voicemail {datetime.now().strftime("%d%m%Y")}')
        db.session.add(campaign)
        db.session.commit()       
        users = db.session.query(User).join(Profile).filter(op_func(Profile.risk, score)).all()
        for user in users:
            send_voicemail(user, campaign)
            result = CampaignResult(campaign_id=campaign.id, user_id=user.id, username=user.username)
            db.session.add(result)
        db.session.commit()
        flash(f'Targeted voicemail campagn has been sent to all users with a risk score {form.operator.data} {score}!')
        return redirect(url_for('admin.console'))
    return render_template('admin/risk_voicemail.html', title='Voicemail Phishing Campaign for Groups by Risk Score', form=form)

@bp.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    if not current_user.is_admin:
        abort(403)
    form = FilterUsers()
    departments = db.session.query(Organisation.department).distinct().all()
    form.department.choices = [('All', 'All')] + [(dept.department, dept.department) for dept in departments]
    form.score_operator.choices = [('All', 'All'), ('>', '>'), ('>=', '>='), ('<', '<'), ('<=', '<='), ('==', '==')]
    preference_choices = [
        ('instructor', 'Instructor-led'),
        ('group', 'Group-based'),
        ('game', 'Games'),
        ('elearn', 'e-Learning'),
        ('quiz', 'Quizzes'),
        ('demo', 'Demonstration'),
        ('video', 'Video'),
        ('text', 'Articles'),
        ('visual', 'Visual-based'),
        ('coach', 'Coaching'),
        ('audio', 'Audio-based')
    ]
    form.training_preference.choices = [('All', 'All')] + preference_choices
    query = db.session.query(User).join(Profile)
    if request.method == 'POST':
        if form.department.data != 'All':
            query = query.filter(User.department == form.department.data)        
        if form.score_operator.data != 'All' and form.score.data is not None:
            op_map = {'>': operator.gt, '>=': operator.ge, '<': operator.lt, '<=': operator.le, '==': operator.eq}
            query = query.filter(op_map[form.score_operator.data](Profile.risk, form.score.data))        
        if form.training_preference.data != 'All':
            pref_field = getattr(Profile, form.training_preference.data, None)
            if pref_field is not None:
                query = query.filter(pref_field == True)                
        users = query.all()
    else:
        users = query.all()        
    return render_template('admin/users.html', title='Users', users=users, form=form)

@bp.route('/edit_user/<target>', methods=['GET', 'POST'])
@login_required
def edit_user(target):
    if not current_user.is_admin:
        abort(403)
    user = db.session.query(User).filter_by(username=target).first()
    if not user:
        flash(f'User {target} not found.', 'warning')
        return redirect(url_for('admin.console'))    
    form=EditUser()
    departments = db.session.query(Organisation.department).distinct().all()
    form.new_department.choices = [(dept.department, dept.department) for dept in departments]
    teams = db.session.query(Organisation.team).distinct().all()
    form.new_team.choices = [(team.team, team.team) for team in teams]
    if request.method=='POST':
        if form.update.data:
            user.firstname = form.firstname.data
            user.lastname = form.lastname.data
            user.email = form.email.data
            user.jobtitle = form.jobtitle.data
            user.team = form.new_team.data
            user.department = form.new_department.data
            user.is_admin = form.isadmin.data
            db.session.commit()
            flash(f"User '{user.username}' has been updated successfully.", 'success')
            return redirect(url_for('admin.console'))        
    else:
        form.username.data = user.username
        form.firstname.data = user.firstname
        form.lastname.data = user.lastname
        form.email.data = user.email
        form.jobtitle.data = user.jobtitle
        form.current_team.data = user.team
        form.new_team.data = user.team
        form.current_department.data = user.department
        form.new_department.data = user.department
        form.isadmin.data = user.is_admin
    return render_template('admin/target_edit.html', title=f'Edit User {user.username}', form=form, user=user)

@bp.route('/delete_user', methods=['GET', 'POST'])
@login_required
def delete_user():
    if not current_user.is_admin:
        abort(403)
    form = DeleteUser()
    if form.validate_on_submit():
        username = form.username.data.strip()
        user = db.session.query(User).filter_by(username=username).first()
        if not user:
            flash(f'User {username} not found.', 'warning')
            return redirect(url_for('admin.console'))        
        profile = db.session.query(Profile).filter_by(user_id=user.id).first()
        if profile:
            db.session.delete(profile)        
        db.session.delete(user)
        db.session.commit()
        flash(f"User '{username}' and associated profile deleted successfully.", 'success')
        return redirect(url_for('admin.console'))
    return render_template('admin/delete_user.html', title='Delete User', form=form)

@bp.route('/executed_campaigns', methods=['GET', 'POST'])
@login_required
def executed_campaigns():
    if not current_user.is_admin:
        abort(403)
    form = FilterCampaigns()
    campaigns = db.session.query(Campaign.name).distinct().all()
    form.campaign.choices = [(campaign.name, campaign.name) for campaign in campaigns]
    results_query = (
        db.session.query(CampaignResult, Campaign, User)
        .join(Campaign, CampaignResult.campaign_id == Campaign.id)
        .join(User, CampaignResult.user_id == User.id)
    )
    if form.validate_on_submit():
        selected_campaign = form.campaign.data
        results_query = results_query.filter(Campaign.name == selected_campaign)
    results = results_query.all()
    total_sent = results_query.count()
    clicked_count = results_query.filter(CampaignResult.clicked == True).count()
    click_rate = (clicked_count / total_sent * 100) if total_sent else 0
    return render_template(
        'admin/executed_campaigns.html',
        title='Executed Campaigns',
        form=form,
        results=results,
        total_sent=total_sent,
        clicked_count=clicked_count,
        click_rate=round(click_rate, 2)
    )

@bp.route('/reset_user_password', methods=['GET', 'POST'])
@login_required
def reset_user_password():
    if not current_user.is_admin:
        abort(403)
    form = ResetUserPassword()
    if form.validate_on_submit():
        username = form.username.data.strip()
        user = db.session.query(User).filter_by(username=username).first()
        if not user:
            flash(f'User {username} not found.', 'warning')
            return redirect(url_for('admin.console'))
        user.set_password(form.password.data)
        db.session.commit()
        flash(f"The password for '{username}' has been changed!")
        return redirect(url_for('admin.console'))
    return render_template('admin/reset_user_password.html', title='Reset User password', form=form)

@bp.route('/training_invitations', methods=['GET', 'POST'])
@login_required
def training_invitation():
    if not current_user.is_admin:
        abort(403)
    form = FilterCampaigns()
    subquery = (
        db.session.query(
            Campaign.name,
            func.max(Campaign.id).label("latest_id")
        )
        .group_by(Campaign.name)
        .subquery()
    )
    campaigns = (
        db.session.query(Campaign)
        .join(subquery, Campaign.id == subquery.c.latest_id)
        .all()
    )
    form.campaign.choices = [(str(c.id), c.name) for c in campaigns]
    if form.validate_on_submit():
        selected_campaign_id = int(form.campaign.data)
        campaign_results = (
            db.session.query(CampaignResult)
            .filter(CampaignResult.campaign_id == selected_campaign_id)
            .filter(CampaignResult.clicked.is_(True))
            .all()
        )
        users_to_email = [result.user for result in campaign_results]
        for user in users_to_email:
            send_training_invitation(user)
        flash(f"{len(users_to_email)} training invitations sent.")
        return redirect(url_for('admin.console'))
    return render_template('admin/training_invitation.html', title='Send training invitations', form=form)
