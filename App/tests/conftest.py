import os
import pytest
from App import create_app
from App.database import db

@pytest.fixture
def test_app():
    os.environ["ENV"] = "TEST"  # Set environment to TEST
    app = create_app()  # Create the Flask app instance
    with app.app_context():
        db.create_all()  # Initialize the database
        yield app  # Yield the app for testing
        db.drop_all()  # Cleanup after tests
    

@pytest.fixture
def session(test_app):
    yield db.session
    db.session.remove()
    
@pytest.fixture
def client(test_app):
    return test_app.test_client()

