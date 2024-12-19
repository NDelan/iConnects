"""
This creates a blueprint for the auth subpackage
"""
from . import routes
from flask import Blueprint

auth = Blueprint('auth', __name__, template_folder='templates')


