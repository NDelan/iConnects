# from flask import render_template, url_for, redirect
# from . import auth

# @auth.route('/signin')
# def signin():
#     return render_template('signin.html')


from flask import render_template, redirect, url_for, flash, request, session, current_app
from .models import Student, Alum
from werkzeug.security import generate_password_hash
from app import db
from . import auth
from flask_login import login_user, login_required, logout_user, current_user
from app import login_manager
import app
from google.oauth2 import id_token
from google.auth.transport import requests


GOOGLE_CLIENT_ID = current_app.config['GOOGLE_CLIENT_ID']

@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == "POST": # handles normal sign in 
        username = request.form.get('username')
        password = request.form.get('password')
        student = Student.query.filter_by(username=username).first()
        alum = Alum.query.filter_by(username=username).first()

        if student and student.check_password(password):
            flash('You have successfully signed in!')
            login_user(student)
            return redirect(url_for('main.home'))
        elif alum and alum.check_password(password):
            flash('You have successfully signed in!')
            login_user(alum)
            return redirect(url_for('main.home'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('auth.signin'))

    return render_template('signin.html', GOOGLE_CLIENT_ID=GOOGLE_CLIENT_ID)



@auth.route('/google_signin', methods=['POST'])
def google_signin():

    if 'credential' in request.form:  # Handles Google credential token
        token = request.form.get('credential')  # Get the ID token from the form
        try:
            # Verify Google ID token
            idinfo = id_token.verify_oauth2_token(
                token, request.reRequest(), current_app.config['GOOGLE_CLIENT_ID']
            )
            email = idinfo.get('email')  # Extract email
            name = idinfo.get('name')  # Extract name

            # Check if the user exists in the database
            student = Student.query.filter_by(email=email).first()
            alum = Alum.query.filter_by(email=email).first()

            if student or alum:
                flash('Welcome back!')
                login_user(student or alum)
            else:
                flash('Google account not associated with a user. Please sign up first.')
                return redirect(url_for('auth.signup'))

            return redirect(url_for('main.home'))
        except ValueError:
            flash('Invalid Google token. Please try again.')
            return redirect(url_for('auth.signin'))

    flash('No Google credential received.')
    return render_template('signin.html', GOOGLE_CLIENT_ID=GOOGLE_CLIENT_ID)

@auth.route('/signup', methods=['GET', 'POST'])
def signup(): 
    if request.method == "POST":
        username = request.form.get('username')
        password_hash=generate_password_hash(request.form.get('password'))
        if Student.query.filter_by(username=username).first() or Alum.query.filter_by(username=username).first():
            flash('Username already exists')
            return render_template('signin.html')
        else:
            if request.form['type'] == "alum":
                alum = Alum(
                    first_name = request.form.get('firstname'),
                    last_name = request.form.get('lastname'),
                    initial = request.form.get('middlename'),
                    username = request.form.get('username'),
                    email = request.form.get('email'),
                    password_hash = password_hash
                )
                db.session.add(alum)
            elif request.form['type'] == "student":
                student = Student(
                    first_name = request.form.get('firstname'),
                    last_name = request.form.get('lastname'),
                    initial = request.form.get('initial'),
                    username = request.form.get('username'),
                    email = request.form.get('email'),
                    password_hash = password_hash
                )
                db.session.add(student)
            db.session.commit()

            flash('You have successfully signed up!')
            return render_template('signin.html')
        
    return render_template('signup.html')



