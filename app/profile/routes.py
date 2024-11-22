from flask import render_template, url_for, redirect
from flask_login import login_user, login_required, logout_user
from . import profile

@profile.route('/profile', methods=['GET', 'POST'])
# @login_required
def create_profile(): 
    return render_template('profile.html')