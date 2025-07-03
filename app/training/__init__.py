# Import Blueprint library
from flask import Blueprint

# Initialise training Blueprint
bp = Blueprint('training', __name__)

# Import routes (required here, prevents circular import issues)
from app.training import routes