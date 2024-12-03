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
        yield db
        db.drop_all()
