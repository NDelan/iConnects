from flask import Blueprint

profile = Blueprint('profile', __name__, template_folder='templates')

from . import routes  # Import routes to register with the blueprint
