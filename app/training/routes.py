from flask import render_template
from flask_login import login_required
from app.training import bp

@bp.route('/catalog')
@login_required
def catalog():
    return render_template('training/catalog.html', title="Training catalog")