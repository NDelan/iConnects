"""
This module defines the routes for the main blueprint.
"""

from flask import render_template, url_for, redirect

# Disable the cyclic import warning for this line
from . import main  # pylint: disable=cyclic-import

@main.route('/')
def index():
    """
    Redirects to the sign-in page of the authentication blueprint.
    """
    return redirect(url_for('auth.signin'))

@main.route('/home')
def home():
    """
    Renders the home page.
    """
    return render_template('home.html')
