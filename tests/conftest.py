import pytest
import os
from app import create_app, db
from app.auth.models import Alum
from app.posts.models import Post

@pytest.fixture(scope="module")
def test_client():
    """Fixture for setting up a Flask test client."""
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    flask_app = create_app()

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            db.create_all()
            yield testing_client
            db.drop_all()

@pytest.fixture(scope="module")
def init_database():
    """Fixture for initializing the database with sample data."""
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    flask_app = create_app()

    with flask_app.app_context():
        db.create_all()

        alum = Alum(
            first_name="Test",
            last_name="Alum",
            email="testalum@example.com",
            password_hash="testpasswordhash"
        )
        db.session.add(alum)
        db.session.commit()

        yield db

        db.drop_all()

@pytest.fixture(scope="function")
def alum_user(init_database):
    """Fixture to return a test alum user."""
    alum = Alum.query.filter_by(email="testalum@example.com").first()
    return alum