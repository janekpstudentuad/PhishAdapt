from flask import render_template, url_for, redirect
from flask_login import login_required, current_user
from app.training import bp
from app.models import User

@bp.route('/content')
@login_required
def content():
    return render_template('training/content.html', title="Training content")

@bp.route('/clicked/<token>')
def clicked(token):
    if current_user.is_authenticated:
        next_page = url_for('main.user', username=current_user.username)
    user = User.verify_training_token(token)
    if not user:
        return redirect(url_for('auth.login'))
    return render_template('training/clicked.html', title="Invitation to training")