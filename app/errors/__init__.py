# Import Blueprint library
from flask import Blueprint

# Initialise errors Blueprint
bp = Blueprint('errors', __name__)

# Import routes (required here, prevents circular import issues)
from app.errors import handlers