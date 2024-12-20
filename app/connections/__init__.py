"""
This module initializes the Blueprint for the 'connections' feature of the Flask application.
"""

from flask import Blueprint

# Initialize the Blueprint
connections = Blueprint('connections', __name__, template_folder='templates')
