from flask import render_template, url_for, redirect
from flask_login import login_user, login_required, logout_user, current_user
from . import main

@main.route('/')
def index():
    return redirect(url_for('auth.signin'))

@main.route('/home')
# @login_required
def home():
    return render_template('home.html')

# @main.route('/posts')
# # @login_required
# def posts(): 
#     return render_template('post.html')

# @main.route('/profile')
# # @login_required
# def profile(): 
#     return render_template('profile.html')

# @main.route('/connections')
# # @login_required
# def connections(): 
#     return render_template('connections.html')

