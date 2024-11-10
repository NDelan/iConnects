from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class Student(UserMixin, db.Model):
    __tablename__ = 'student'
    student_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    initial = db.Column(db.String(3), nullable=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(30), nullable=False)
    mentor = db.Column(db.Integer, db.ForeignKey("alum.alum_id"), nullable=True)

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


class Alum(UserMixin, db.Model):
    __tablename__ = 'alum'
    alum_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    initial = db.Column(db.String(3), nullable=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(30), nullable=False)

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