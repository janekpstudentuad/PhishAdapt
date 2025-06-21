from app.main import bp
from flask import redirect, render_template, url_for

@bp.route('/')
@bp.route('/index')
def index():
    return redirect(url_for('auth.login'))