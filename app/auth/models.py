"""
This module creates the Student and Alum tables
"""
from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db

class Student(db.Model, UserMixin):
    """Creates a Student instance"""
    __tablename__ = 'student'
    student_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    initial = db.Column(db.String(3), nullable=True)
    profile_picture_data = db.Column(db.LargeBinary, nullable=True)
    profile_picture_content_type = db.Column(db.String(50), nullable=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(30), nullable=False)
    mentor = db.Column(db.Integer, db.ForeignKey("alum.alum_id"), nullable=True)
    headline = db.Column(db.String(120), nullable=True)

    def set_password(self, password):
        """Create hashed password and store it in the database"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check password_hash with the password provided by the user"""
        return check_password_hash(self.password_hash, password)
    
    def check_username(self, username):
        """Check username with the username provided by the user"""
        return self.username == username
    
    def set_username(self, username):
        """Set username to a new value"""
        self.username = username

    def set_mentor(self, mentor):
        """Set mentor to a new value"""
        self.mentor = mentor

    def get_mentor(self):
        """Returns the mentor of the student"""
        return self.mentor
    
    def get_headline(self):
        """Returns the profile headline of the student"""
        return self.headline
    
    def set_headline(self, headline):
        """Sets the profile headline of the student"""
        self.headline = headline

    def get_id(self):
        """returns the student id"""
        return self.student_id
    
    def get_profile_picture_url(self):
        """Generate a URL to serve the profile picture."""
        if self.profile_picture_data:
            return url_for('profile.serve_profile_picture', user_id=self.student_id)
        return url_for('static', filename='images/profile.jpg')
    
    @property
    def is_student(self):
        """checks if an instance is of type Student"""
        return True

    @property
    def is_alum(self):
        """checks if an instance is of type Alum"""
        return False

class Alum(db.Model, UserMixin):
    """Create an Alum instance"""
    __tablename__ = 'alum'
    alum_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    initial = db.Column(db.String(3), nullable=True)
    profile_picture_data = db.Column(db.LargeBinary, nullable=True)
    profile_picture_content_type = db.Column(db.String(50), nullable=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(30), nullable=False)
    headline = db.Column(db.String(120), nullable=True)

    def set_password(self, password):
        """Create hashed password and store it in the database"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check password_hash with the password provided by the user"""
        return check_password_hash(self.password_hash, password)
    
    def check_username(self, username):
        """Check username with the username provided by the user"""
        return self.username == username
    
    def set_username(self, username):
        """Set username to a new value"""
        self.username = username

    def get_headline(self):
        """Returns the profile headline of the student"""
        return self.headline
    
    def set_headline(self, headline):
        """Sets the profile headline of the student"""
        self.headline = headline

    def get_id(self):
        return self.alum_id
    
    def get_profile_picture_url(self):
        """Generate a URL to serve the profile picture."""
        if self.profile_picture_data:
            return url_for('auth.serve_profile_picture', user_id=self.get_id())
        return url_for('static', filename='images/profile.jpg')

    @property
    def is_student(self):
        """checks if an instance is of type Student"""
        return False

    @property
    def is_alum(self):
        """checks if an instance is of type Alum"""
        return True