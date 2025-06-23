from flask import render_template
from flask_login import login_required
from app.training import bp

@bp.route('/content')
@login_required
def content():
    return render_template('training/content.html', title="Training content")