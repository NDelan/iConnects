"""
This module initializes the main blueprint for the Flask application.
"""

from flask import Blueprint

main = Blueprint('main', __name__, template_folder='templates')

from . import routes  # pylint: disable=wrong-import-position
