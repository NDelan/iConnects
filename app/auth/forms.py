from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
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


class Alum(db.Model):
    __tablename__ = 'alum'
    id = db.Column(db.Integer, primary_key=True)
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