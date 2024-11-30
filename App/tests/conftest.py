import pytest
from App import create_app
from App.database import db

@pytest.fixture
def app():
    app = create_app("test")  
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all() 

@pytest.fixture
def db_session(app):
    yield db.session
    db.session.remove()
