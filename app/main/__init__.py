# Import Blueprint library
from flask import Blueprint

# Initialise main Blueprint
bp = Blueprint('main', __name__)

# Import routes (required here, prevents circular import issues)
from app.main import routes