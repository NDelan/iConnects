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


def get_google_client_id():
    return current_app.config['GOOGLE_CLIENT_ID']

@auth.route('/')
@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == "POST":
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
    print("the callback worked")

    return render_template('signin.html', GOOGLE_CLIENT_ID = get_google_client_id())



@auth.route('/google_signin', methods=['GET', 'POST'])
def google_signin():
    if 'credential' in request.json:  # Handles Google credential token
        data = request.get_json()
        token = data['credential']
        try:
            idinfo = id_token.verify_oauth2_token(
                token, requests.Request(), current_app.config['GOOGLE_CLIENT_ID']
            )
            email = idinfo.get('email')  # Extract email

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
            print("invalid token")
            return redirect(url_for('auth.signin'))

    flash('No Google credential received.')
    return render_template('signin.html', get_google_client_id())

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



