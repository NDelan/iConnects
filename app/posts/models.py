from datetime import datetime
from app import db
from app.auth.models import Alum

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    image_data = db.Column(db.LargeBinary, nullable=True)
    image_content_type = db.Column(db.String(50), nullable=True)
    video_data = db.Column(db.LargeBinary, nullable=True)
    video_content_type = db.Column(db.String(50), nullable=True)

    event_name = db.Column(db.String(100), nullable=True)
    event_date = db.Column(db.Date, nullable=True)
    event_description = db.Column(db.Text, nullable=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('alum.alum_id'), nullable=False)
    author = db.relationship('Alum', backref='posts', lazy=True)

    def __repr__(self):
        return f"<Post {self.title}>"