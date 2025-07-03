# Import Blueprint library
from flask import Blueprint

# Initialise auth Blueprint
bp = Blueprint('auth', __name__)

# Import routes (required here, prevents circular import issues)
from app.auth import routes