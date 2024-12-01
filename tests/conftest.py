import pytest
import os
from app import create_app, db
from app.auth.models import Alum, Student
from app.posts.models import Post
from flask_login import login_user
import base64

@pytest.fixture
def auth_headers(client, request):
    """Create a test user and return authentication headers"""
    # Create a test student or alum
    user = Student(
        username='testuser',
        email='test@example.com',
        first_name='Test',
        last_name='User'
    )
    user.set_password('testpassword')  # Use set_password method
    db.session.add(user)
    db.session.commit()

    # Simulate login
    with client.session_transaction() as sess:
        # This simulates logging in the user
        sess['user_id'] = user.student_id

    # Create basic auth headers
    credentials = base64.b64encode(b'testuser:testpassword').decode('utf-8')
    
    return {
        'Authorization': f'Basic {credentials}',
        'Content-Type': 'application/json'
    }

@pytest.fixture(scope="function")
def client():
    """Fixture for setting up a Flask test client."""
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    flask_app = create_app()

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            # Drop all tables and recreate them before each test
            db.drop_all()
            db.create_all()
            yield testing_client

@pytest.fixture(scope="module")
def init_database():
    """Fixture for initializing the database with sample data."""
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    flask_app = create_app()

    with flask_app.app_context():
        db.create_all()

        # Uncomment and modify as needed for test user
        # alum = Alum(
        #     first_name="Delanyo",
        #     last_name="Nutakor",
        #     email="dnutak26@colby.edu",
        #     password_hash="testpasswordhash"
        # )
        # db.session.add(alum)
        # db.session.commit()

        yield db

        db.drop_all()

@pytest.fixture(scope="function")
def alum_user(init_database):
    """Fixture to return a test alum user."""
    alum = Alum.query.filter_by(email="dnutak26@colby.edu").first()
    return alum