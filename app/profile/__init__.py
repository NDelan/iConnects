"""Profile Blueprint Initialization."""

from flask import Blueprint

profile = Blueprint('profile', __name__, template_folder='templates')

# Import routes to register with the blueprint
from . import routes # pylint: disable=wrong-import-position
