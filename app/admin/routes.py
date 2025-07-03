# Import Blueprint class instance
from app.admin import bp

# Import required libraries
from flask import render_template, flash, redirect, url_for, abort, request
from flask_login import current_user, login_required
import operator
from datetime import datetime
from sqlalchemy import func

# Import required forms
from app.admin.forms import UserSearch, RegistrationForm, ResetUserPassword, EditUser, DeleteUser, BaselineCampaign, DepartmentalGroups, RiskGroups, FilterUsers, FilterCampaigns

# Import classes from other functions
from app import db
from app.models import User, Organisation, Profile, Campaign, CampaignResult

# Import functions from other Blueprints
from app.admin.email import send_voicemail, send_training_invitation

# Blueprint route for admin console page
@bp.route('/console', methods=['GET', 'POST'])
@login_required
def console():
    # Check if logged-in user is registered as an admin and return 403 (Forbidden) error message if not
    if not current_user.is_admin:
        abort(403)
    # Instantiate instance of user search form
    form = UserSearch()
    # Attempt to set a user object to edit if request to page submitted includes a completed form
    if form.validate_on_submit():
        target = form.username.data
        # Redirect to admin edit user
        return redirect(url_for('admin.edit_user', target=target))
    # Render admin console page if request contains no form data
    return render_template('admin/console.html', title='Admin console', form=form)

# Blueprint route for admin register new user page
@bp.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    # Check if logged-in user is registered as an admin and return 403 (Forbidden) error message if not
    if not current_user.is_admin:
        abort(403)
    # Instantiate instance of user registration form
    form = RegistrationForm()
    # Generate options for dropdown Department list and set to form field
    departments = db.session.query(Organisation.department).distinct().all()
    form.department.choices = [(dept.department, dept.department) for dept in departments]
    # Generate options for dropdown Team list and set to form field
    teams = db.session.query(Organisation.team).distinct().all()
    form.team.choices = [(team.team, team.team) for team in teams]
    # Instantiate new User object and attributes using form data if request to page submitted includes a completed form
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
        # Set user password as per form data
        user.set_password(form.password.data)
        # Enter user information into user table
        db.session.add(user)
        db.session.commit()
        # Create user profile for new user
        profile = Profile(user_id=user.id, risk=0)
        db.session.add(profile)
        db.session.commit()
        # Display info message on completion
        username = form.username.data
        flash(f'{username} is now a registered user.')
        # Redirect to main admin console page on completion
        return redirect(url_for('admin.console'))
    # Render register new user page if request contains no form data
    return render_template('admin/register.html', title='Register', form=form)

# Blueprint route for admin reset password functionality
@bp.route('/reset_user_password', methods=['GET', 'POST'])
@login_required
def reset_user_password():
    # Check if logged-in user is registered as an admin and return 403 (Forbidden) error message if not
    if not current_user.is_admin:
        abort(403)
    # Instantiate reset user password form
    form = ResetUserPassword()
    if form.validate_on_submit():
         # Format user input from form
        username = form.username.data.strip()
        # Set provided user name as variable
        user = db.session.query(User).filter_by(username=username).first()
        # Display error message if user not found in user db
        if not user:
            flash(f'User {username} not found.', 'warning')
            # Redirect to admin console
            return redirect(url_for('admin.console'))
        # Set password for supplied user
        user.set_password(form.password.data)
        db.session.commit()
        # Display info message on completion
        flash(f"The password for '{username}' has been changed!")
        # Redirect to admin console page on completion
        return redirect(url_for('admin.console'))
    # Render admin reset user password page if request contains no form data
    return render_template('admin/reset_user_password.html', title='Reset User password', form=form)

# Blueprint route for admin edit user functionality
@bp.route('/edit_user/<target>', methods=['GET', 'POST'])
@login_required
def edit_user(target):
    # Check if logged-in user is registered as an admin and return 403 (Forbidden) error message if not
    if not current_user.is_admin:
        abort(403)
    # Set user for editing as variable
    user = db.session.query(User).filter_by(username=target).first()
    # Display error message if user name provided (from UserSearch form on Console page) is invalid
    if not user:
        flash(f'User {target} not found.', 'warning')
        # Redirect to admin console page
        return redirect(url_for('admin.console'))
    # Instantiate admin edit user form
    form=EditUser()
    # Generate options for dropdown Department list and set to form field
    departments = db.session.query(Organisation.department).distinct().all()
    form.new_department.choices = [(dept.department, dept.department) for dept in departments]
    # Generate options for dropdown Team list and set to form field
    teams = db.session.query(Organisation.team).distinct().all()
    form.new_team.choices = [(team.team, team.team) for team in teams]
    # Set attributes for user as per form if request made via submit button
    if request.method=='POST':
        if form.update.data:
            user.firstname = form.firstname.data
            user.lastname = form.lastname.data
            user.email = form.email.data
            user.jobtitle = form.jobtitle.data
            user.team = form.new_team.data
            user.department = form.new_department.data
            user.is_admin = form.isadmin.data
            # Update db values with form data
            db.session.commit()
            # Display info message on completion
            flash(f"User '{user.username}' has been updated successfully.", 'success')
            # Redirect to adming console page on completion
            return redirect(url_for('admin.console'))        
    # Autofill form with existing user data if request made via user search function
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
    # Render admin edit user page if request is made via user search function
    return render_template('admin/target_edit.html', title=f'Edit User {user.username}', form=form, user=user)

# Blueprint route for delete user functionality
@bp.route('/delete_user', methods=['GET', 'POST'])
@login_required
def delete_user():
    # Check if logged-in user is registered as an admin and return 403 (Forbidden) error message if not
    if not current_user.is_admin:
        abort(403)
    # Instantiate admin delete user form
    form = DeleteUser()
    if form.validate_on_submit():
        # Format user input from form
        username = form.username.data.strip()
        # Set provided user name as variable
        user = db.session.query(User).filter_by(username=username).first()
        # Display error message if user not found in user db
        if not user:
            flash(f'User {username} not found.', 'warning')
            # Redirect to admin console
            return redirect(url_for('admin.console'))        
        # Set profile information if user name valid
        profile = db.session.query(Profile).filter_by(user_id=user.id).first()
        # Delete profile if it exists
        if profile:
            db.session.delete(profile)
        # Delete user and commit db changes
        db.session.delete(user)
        db.session.commit()
        # Display info message on completion
        flash(f"User '{username}' and associated profile deleted successfully.", 'success')
        # Redirect to admin console page
        return redirect(url_for('admin.console'))
    # Render admin delete user page if request contains no form data
    return render_template('admin/delete_user.html', title='Delete User', form=form)

# Blueprint route for displaying list of users and associated profile information
@bp.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    # Check if logged-in user is registered as an admin and return 403 (Forbidden) error message if not
    if not current_user.is_admin:
        abort(403)
    # Instantiate form for user filtering
    form = FilterUsers()
    # Generate options for dropdown Department list and set to form field
    departments = db.session.query(Organisation.department).distinct().all()
    form.department.choices = [('All', 'All')] + [(dept.department, dept.department) for dept in departments]
    # Generate options for dropdown risk score operator list and set to form field
    form.score_operator.choices = [('All', 'All'), ('>', '>'), ('>=', '>='), ('<', '<'), ('<=', '<='), ('==', '==')]
    # Generate options for user training preference training from available options in profile table and set to form field
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
    # Query db to get profile info dor user
    query = db.session.query(User).join(Profile)
    # Apply filters set to user list if submit button used to make request to route
    if request.method == 'POST':
        if form.department.data != 'All':
            query = query.filter(User.department == form.department.data)        
        if form.score_operator.data != 'All' and form.score.data is not None:
            # Map risk score operator dropdown list choices to arithmetic expressions
            op_map = {'>': operator.gt, '>=': operator.ge, '<': operator.lt, '<=': operator.le, '==': operator.eq}
            query = query.filter(op_map[form.score_operator.data](Profile.risk, form.score.data))        
        if form.training_preference.data != 'All':
            pref_field = getattr(Profile, form.training_preference.data, None)
            if pref_field is not None:
                query = query.filter(pref_field == True)                
        users = query.all()
    # Return list of all users if no filters set
    else:
        users = query.all()
    # Render targeted voicemail campaign page if request contains no filtering data   
    return render_template('admin/users.html', title='Users', users=users, form=form)

# Blueprint route for Campaign page
@bp.route('/campaigns')
@login_required
def campaigns():
    # Check if logged-in user is registered as an admin and return 403 (Forbidden) error message if not
    if not current_user.is_admin:
        abort(403)
    # Render campaigns page
    return render_template('admin/campaigns.html', title='Training Campaigns')

# Blueprint route for baseline campaigns page
@bp.route('/campaigns/baselines')
@login_required
def baselines():
    # Check if logged-in user is registered as an admin and return 403 (Forbidden) error message if not
    if not current_user.is_admin:
        abort(403)
    # Render baseline campaigns page
    return render_template('admin/baselines.html', title='Baseline Training Campaigns')

# Blueprint route for voicemail baseline campaign page
@bp.route('/campaigns/baselines/voicemail', methods=['GET', 'POST'])
@login_required
def baseline_voicemail():
    # Check if logged-in user is registered as an admin and return 403 (Forbidden) error message if not
    if not current_user.is_admin:
        abort(403)
    # Instantiate instace of baseline campaign form
    form = BaselineCampaign()
    # Create new Campaign object and add to campaign table if request to page submitted includes a completed form
    if form.validate_on_submit():
        campaign = Campaign(name=f'Baseline Voicemail {datetime.now().strftime("%d%m%Y")}')
        db.session.add(campaign)
        db.session.commit()
        # Get list of all users in db
        users = db.session.query(User).all()
        # Send voicemail baseline campaign email to all users in list
        for user in users:
            send_voicemail(user, campaign)
            # Add entry to campaign result table for user
            result = CampaignResult(campaign_id=campaign.id, user_id=user.id, username=user.username)
            db.session.add(result)
        db.session.commit()
        # Display info message on completion
        flash('Baseline voicemail campagn has been sent to all users!')
        # Redirect to main admin console page on completion
        return redirect(url_for('admin.console'))
    # Render baseline voicemail campaign page if request contains no form data
    return render_template('admin/baseline_voicemail.html', title='Baseline Voicemail Campaign', form=form)

# Blueprint route for targeted campaigns page
@bp.route('/campaigns/targeted_campaigns')
@login_required
def targeted_campaigns():
    # Check if logged-in user is registered as an admin and return 403 (Forbidden) error message if not
    if not current_user.is_admin:
        abort(403)
    # Blueprint route for targeted campaigns page
    return render_template('admin/targeted_campaigns.html', title='Targeted Training Campaigns')

# Blueprint route for departmental targeted voicemail campaigns page
@bp.route('/campaigns/target_campaigns/group_voicemail', methods=['GET', 'POST'])
@login_required
def group_voicemail():
    # Check if logged-in user is registered as an admin and return 403 (Forbidden) error message if not
    if not current_user.is_admin:
        abort(403)
    # Instantiate form for Department selection
    form = DepartmentalGroups()
    # Generate options for dropdown Department list and set to form field
    departments = db.session.query(Organisation.department).distinct().all()
    form.department.choices = [(dept.department, dept.department) for dept in departments]
    # Create new Campaign object and add to campaign table if request to page submitted includes a completed form
    if form.validate_on_submit():
        department = form.department.data
        campaign = Campaign(name=f'Targeted {department} Voicemail {datetime.now().strftime("%d%m%Y")}')
        db.session.add(campaign)
        db.session.commit()
        # Get list of targeted users in db
        users = db.session.query(User).where(User.department == department).all()
        for user in users:
            # Send targeted voicemail campaign email to all users in list
            send_voicemail(user, campaign)
            # Add entry to campaign result table for user
            result = CampaignResult(campaign_id=campaign.id, user_id=user.id, username=user.username)
            db.session.add(result)
        db.session.commit()
        # Display info message on completion
        flash(f'Targeted voicemail campagn has been sent to all users in {department}!')
        # Redirect to main admin console page on completion
        return redirect(url_for('admin.console'))
    # Render targeted voicemail campaign page if request contains no form data
    return render_template('admin/group_voicemail.html', title='Voicemail Phishing Campaign for Departmental Groups', form=form)

# Blueprint route for risk score targeted voicemail campaigns page
@bp.route('/campaigns/target_campaigns/risk_voicemail', methods=['GET', 'POST'])
@login_required
def risk_voicemail():
    # Check if logged-in user is registered as an admin and return 403 (Forbidden) error message if not
    if not current_user.is_admin:
        abort(403)
    # Instantiate form for Risk Score selection
    form=RiskGroups()
    # Generate options for dropdown risk score operator list and set to form field
    form.operator.choices = [('>', '>'), ('>=', '>='), ('<', '<'), ('<=', '<='), ('==', '==')]
    # Create new Campaign object and add to campaign table if request to page submitted includes a completed form
    if form.validate_on_submit():
        # Map dropdown list choices to arithmetic expressions
        op_map = {'>': operator.gt, '>=': operator.ge, '<': operator.lt, '<=': operator.le, '==': operator.eq}
        op_func = op_map[form.operator.data]
        # Set score as per form data
        score = form.score.data
        # Create new Campaign object and add to campaign table
        campaign = Campaign(name=f'Risk Score {form.operator.data} {score} Voicemail {datetime.now().strftime("%d%m%Y")}')
        db.session.add(campaign)
        db.session.commit()
        # Get list of targeted users in db
        users = db.session.query(User).join(Profile).filter(op_func(Profile.risk, score)).all()
        for user in users:
            # Send targeted voicemail campaign email to all users in list
            send_voicemail(user, campaign)
            # Add entry to campaign result table for user
            result = CampaignResult(campaign_id=campaign.id, user_id=user.id, username=user.username)
            db.session.add(result)
        db.session.commit()
        # Display info message on completion
        flash(f'Targeted voicemail campagn has been sent to all users with a risk score {form.operator.data} {score}!')
        # Redirect to main admin console page on completion
        return redirect(url_for('admin.console'))
    # Render targeted voicemail campaign page if request contains no form data
    return render_template('admin/risk_voicemail.html', title='Voicemail Phishing Campaign for Groups by Risk Score', form=form)

# Blueprint route for displaying a list of executed camppaigns
@bp.route('/executed_campaigns', methods=['GET', 'POST'])
@login_required
def executed_campaigns():
    # Check if logged-in user is registered as an admin and return 403 (Forbidden) error message if not
    if not current_user.is_admin:
        abort(403)
    # Instatiate form for filtering campaign list
    form = FilterCampaigns()
    # Generate options for dropdown campaigns list and set to form field
    campaigns = db.session.query(Campaign.name).distinct().all()
    form.campaign.choices = [(campaign.name, campaign.name) for campaign in campaigns]
    # Query db to obtain campaign results per campaign
    results_query = (
        db.session.query(CampaignResult, Campaign, User)
        .join(Campaign, CampaignResult.campaign_id == Campaign.id)
        .join(User, CampaignResult.user_id == User.id)
    )
    # Return list of campaign results if request contains filtering data
    if form.validate_on_submit():
        selected_campaign = form.campaign.data
        results_query = results_query.filter(Campaign.name == selected_campaign)
    # Return list of all campaign results if no filtering data present
    results = results_query.all()
    # Count number of emails sent across campaign(s) displayed
    total_sent = results_query.count()
    # Count number of user clicks across campaign(s) displayed
    clicked_count = results_query.filter(CampaignResult.clicked == True).count()
    # Calculate click rate across campaign(s) displayed
    click_rate = (clicked_count / total_sent * 100) if total_sent else 0
    # Render executed campaigns page
    return render_template(
        'admin/executed_campaigns.html',
        title='Executed Campaigns',
        form=form,
        results=results,
        total_sent=total_sent,
        clicked_count=clicked_count,
        click_rate=round(click_rate, 2)
    )

# Blueprint route for sending training invitation functionality
@bp.route('/training_invitations', methods=['GET', 'POST'])
@login_required
def training_invitation():
    # Check if logged-in user is registered as an admin and return 403 (Forbidden) error message if not
    if not current_user.is_admin:
        abort(403)
    # Instantiate form for campaign filtering
    form = FilterCampaigns()
    # Query db to display all campaigns 
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
    # Generate options for dropdown campaign filter list and set to form field
    form.campaign.choices = [(str(c.id), c.name) for c in campaigns]
    # Obtain campaign results for selected campaign if request contains filter data
    if form.validate_on_submit():
        selected_campaign_id = int(form.campaign.data)
        campaign_results = (
            db.session.query(CampaignResult)
            .filter(CampaignResult.campaign_id == selected_campaign_id)
            .filter(CampaignResult.clicked.is_(True))
            .all()
        )
        # Generate list of users from campaign results table for selected campaign
        users_to_email = [result.user for result in campaign_results]
        # Send email to each user in list
        for user in users_to_email:
            send_training_invitation(user)
        # Display info message on completion
        flash(f"{len(users_to_email)} training invitations sent.")
        # Redirect to admin console page on completion
        return redirect(url_for('admin.console'))
    # Render admin send training invitations page if request contains no form data
    return render_template('admin/training_invitation.html', title='Send training invitations', form=form)
