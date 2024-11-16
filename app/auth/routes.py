# from flask import render_template, url_for, redirect
# from . import auth

# @auth.route('/signin')
# def signin():
#     return render_template('signin.html')


from flask import render_template, redirect, url_for, flash, request
from .models import Student, Alum
from werkzeug.security import generate_password_hash
from app import db
from . import auth
from flask_login import login_user, login_required, logout_user, current_user
from app import login_manager
import os 

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')

@auth.route('/')
@auth.route('/signin', methods=['GET', 'POST'])
def signin(): 
    if request.method == "POST":
        username = request.form.get('username')
        password_hash = request.form.get('password')
        student = Student.query.filter_by(username=username).first()
        alum = Alum.query.filter_by(username=username).first()
        if student:
            if student.check_password(password_hash):
                flash('You have successfully signed in!')
                login_user(student)
                return redirect(url_for('main.home'))
            else:
                flash('Invalid password')
        elif alum:
            if alum.check_password(password_hash):
                flash('You have successfully signed in!')
                login_user(alum)
                return redirect(url_for('main.home'))
            else:
                flash('Invalid password')
        else:
            flash('Username does not exist')
            return render_template('signup.html')
    return render_template('signin.html',GOOGLE_CLIENT_ID=GOOGLE_CLIENT_ID)


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



