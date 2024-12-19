"""
This module initializes the Blueprint for the 'connections' feature of the Flask application.
"""

from flask import Blueprint

connections = Blueprint('connections', __name__, template_folder='templates')

from . import routes  # pylint: disable=wrong-import-position
