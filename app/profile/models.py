# pylint: disable=too-few-public-methods
"""
This module defines the database models for projects, experiences, achievements, and connections.
It also contains the necessary relationships and logic for user connections.
"""

from datetime import datetime
from app import db
from app.auth.models import Student


class Project(db.Model):
    """
    Represents a project that a student or alum is involved in.
    """
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(200))
    description = db.Column(db.Text)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    is_current = db.Column(db.Boolean, default=False)

    # Foreign keys
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'))
    alum_id = db.Column(db.Integer, db.ForeignKey('alum.alum_id'))
    # Define the relationship to either student or alum
    student = db.relationship('Student', backref=db.backref('projects', lazy=True))
    alum = db.relationship('Alum', backref=db.backref('projects', lazy=True))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Experience(db.Model):
    """
    Represents an experience (e.g., job or internship) of a student or alum.
    """
    __tablename__ = 'experiences'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(200))  # Company/Organization name
    description = db.Column(db.Text)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    is_current = db.Column(db.Boolean, default=False)

    # Foreign keys
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'))
    alum_id = db.Column(db.Integer, db.ForeignKey('alum.alum_id'))

    # Relationship to either student or alum
    student = db.relationship('Student', backref=db.backref('experiences', lazy=True))
    alum = db.relationship('Alum', backref=db.backref('experiences', lazy=True))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Achievement(db.Model):
    """
    Represents an achievement (e.g., award or recognition) for a student or alum.
    """
    __tablename__ = 'achievements'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(200))
    description = db.Column(db.Text)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    is_current = db.Column(db.Boolean, default=False)

    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'))
    alum_id = db.Column(db.Integer, db.ForeignKey('alum.alum_id'))

    # Relationship to either student or alum
    student = db.relationship('Student', backref=db.backref('achievements', lazy=True))
    alum = db.relationship('Alum', backref=db.backref('achievements', lazy=True))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Connection(db.Model):
    """
    Represents a connection (friendship or networking link) between a student and an alum.
    """
    __tablename__ = 'connections'

    id = db.Column(db.Integer, primary_key=True)
    # The user who initiated the connection
    initiator_student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'))
    initiator_alum_id = db.Column(db.Integer, db.ForeignKey('alum.alum_id'))
    # The user who received/accepted the connection
    receiver_student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'))
    receiver_alum_id = db.Column(db.Integer, db.ForeignKey('alum.alum_id'))

    status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Define relationships
    initiator_student = db.relationship('Student', foreign_keys=[initiator_student_id],
                                      backref=db.backref('initiated_connections', lazy=True))
    initiator_alum = db.relationship('Alum', foreign_keys=[initiator_alum_id],
                                   backref=db.backref('initiated_connections', lazy=True))
    receiver_student = db.relationship('Student', foreign_keys=[receiver_student_id],
                                     backref=db.backref('received_connections', lazy=True))
    receiver_alum = db.relationship('Alum', foreign_keys=[receiver_alum_id],
                                  backref=db.backref('received_connections', lazy=True))

    @staticmethod
    def are_connected(user1, user2):
        """
        Check if two users are connected.
        """
        if isinstance(user1, Student):
            user1_type = 'student'
            user1_id = user1.student_id
        else:
            user1_type = 'alum'
            user1_id = user1.alum_id

        if isinstance(user2, Student):
            user2_type = 'student'
            user2_id = user2.student_id
        else:
            user2_type = 'alum'
            user2_id = user2.alum_id
        # Check both directions of connection
        connection = Connection.query.filter(
            (
                (
                    (Connection.initiator_student_id == user1_id if user1_type == 'student'
                    else Connection.initiator_alum_id == user1_id) &
                    (Connection.receiver_student_id == user2_id if user2_type == 'student'
                    else Connection.receiver_alum_id == user2_id)
                ) |
                (
                    (Connection.initiator_student_id == user2_id if user2_type == 'student'
                    else Connection.initiator_alum_id == user2_id) &
                    (Connection.receiver_student_id == user1_id if user1_type == 'student'
                    else Connection.receiver_alum_id == user1_id)
                )
            )
        ).filter_by(status='accepted').first()

        return connection is not None
