# Import Blueprint library
from flask import Blueprint

# Initialise admin Blueprint
bp = Blueprint('admin', __name__)

# Import routes (required here, prevents circular import issues)
from app.admin import routes