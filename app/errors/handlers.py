# Import Blueprint class instance
from app.errors import bp

# Import required libraries
from flask import render_template

# Import classes from other functions
from app import db

# Blueprint route for error 403 (forbidden) page
@bp.app_errorhandler(403)
def forbidden(error):
    # Roll back any pending db changes
    db.session.rollback()
    # Render 403 page
    return render_template('errors/403.html'), 403

# Blueprint route for error 404 (page not found) page
@bp.app_errorhandler(404)
def not_found_error(error):
    # Render 404 page
    return render_template('errors/404.html'), 404


# Blueprint route for error 500 (internal server error) page
@bp.app_errorhandler(500)
def internal_error(error):
    # Roll back any pending db changes
    db.session.rollback()
    # Render 500 page
    return render_template('errors/500.html'), 500