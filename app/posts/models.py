from datetime import datetime
from app import db
from app.auth.models import Alum
from flask_login import UserMixin

class Post(UserMixin, db.Model):
    __tablename__ = 'posts'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Main fields
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    image_path = db.Column(db.String(255), nullable=True)
    video_path = db.Column(db.String(255), nullable=True)
    event_name = db.Column(db.String(100), nullable=True)
    event_date = db.Column(db.Date, nullable=True)
    event_description = db.Column(db.Text, nullable=True)
    
    # Foreign key to the Alum (user) table
    user_id = db.Column(db.Integer, db.ForeignKey('alum.alum_id'), nullable=False)
    author = db.relationship('Alum', backref='posts', lazy=True)

    def __repr__(self):
        return f"<Post {self.title}>"