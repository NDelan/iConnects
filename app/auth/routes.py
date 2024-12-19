"""
This module manages the routing for the authentication
"""
import io
from werkzeug.security import generate_password_hash
from flask import jsonify, render_template, redirect, url_for, flash, request, current_app, send_file
from flask_login import login_user, login_required, current_user
from google.oauth2 import id_token
from google.auth.transport import requests
from app import db
from .models import Student, Alum
from . import auth



def get_google_client_id():
    """returns the google client id"""
    return current_app.config['GOOGLE_CLIENT_ID']

@auth.route('/')
@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    """signs a user user"""
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        student = Student.query.filter_by(username=username).first()
        alum = Alum.query.filter_by(username=username).first()

        if student and student.check_password(password):
            flash('You have successfully signed in!')
            login_user(student)
            return redirect(url_for('main.home'))
        if alum and alum.check_password(password):
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
    """manages google sign in """
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
    """manages user sign up"""
    if request.method == "POST":
        username = request.form.get('username')
        password_hash=generate_password_hash(request.form.get('password'))
        if (Student.query.filter_by(username=username).first() or 
            Alum.query.filter_by(username=username).first()):
            flash('Username already exists')
            return render_template('signin.html')
        
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

@auth.route('/api/user_info')
@login_required
def get_user_info():
    """retrieves user info"""
    user = current_user  # The logged-in user (Student or Alum)

    def serialize_user(user):
        return {
            "name": f"{user.first_name} {user.last_name}",
            "title": user.username,
            "profile_picture_url": user.get_profile_picture_url()
        }

    if user.is_student:  # If the user is a Student
        alums = Alum.query.limit(50).all()  # Limit to 50 results
        other_users_info = [serialize_user(alum) for alum in alums]
        response_data = {"user_type": "student", "others": other_users_info}
        return jsonify(response_data)

    if user.is_alum:  # If the user is an Alum
        students = Student.query.limit(50).all()  # Limit to 50 results
        other_users_info = [serialize_user(student) for student in students]
        return jsonify({"user_type": "alum", "others": other_users_info})

    return jsonify({"error": "User is neither a Student nor an Alum"}), 400

@auth.route('/profile_picture/<int:user_id>')
def serve_profile_picture(user_id):
    user = Student.query.get(user_id) or Alum.query.get(user_id)
    if user and user.profile_picture_data:
        return send_file(
            io.BytesIO(user.profile_picture_data),
            mimetype=user.profile_picture_content_type
        )
    return url_for('static', filename='images/profile.jpg')  # Default image