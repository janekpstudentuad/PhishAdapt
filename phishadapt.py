# Import app and db class instances
from app import create_app

# Import libraries and class instances for Flask Shell
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from app.models import User, Organisation

# Create web application instance
app = create_app()

# Set variables for use with Flask Shell
@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Organisation': Organisation}