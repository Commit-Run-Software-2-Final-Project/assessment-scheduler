import pytest
from App.database import db
from App.models import User, Staff, Admin
from werkzeug.security import check_password_hash
from App.controllers.user import validate_Staff, validate_Admin, get_user, get_uid
from App.models.staff import Status
from App.main import create_app

'''
Unit Tests
'''
# Sample test user data
TEST_USER = {
    "u_ID": 1,
    "email": "test@example.com",
    "password": "password123"
}

@pytest.fixture
def test_user():
    """Fixture for creating a test user."""
    return User(u_ID=TEST_USER["u_ID"], email=TEST_USER["email"], password=TEST_USER["password"])

def test_user_password_hashing(test_user):
    """Test password hashing and checking."""
    assert test_user.password != TEST_USER["password"]  # Ensure the password is hashed
    assert test_user.check_password(TEST_USER["password"])  # Ensure the password check works
    assert not test_user.check_password("wrongpassword")  # Ensure wrong passwords fail

def test_user_to_json(test_user):
    """Test the `to_json` method."""
    user_json = test_user.to_json()
    assert user_json["u_ID"] == TEST_USER["u_ID"]
    assert user_json["email"] == TEST_USER["email"]
    assert "password" in user_json

def test_user_str(test_user):
    """Test the `__str__` method."""
    assert str(test_user) == f"Staff(id={TEST_USER['u_ID']}, email={TEST_USER['email']})"



'''
Integration Tests
'''

@pytest.fixture
def setup_app(app):
    """Set up the test app and database."""
    app.config.from_object('App.default_config')  # Replace with actual TestingConfig path
    with app.app_context():
        db.create_all()
        # Create test users
        staff = Staff(fName="John", lName="Doe", status=Status.HOD, u_ID=1, email="staff@example.com", password="staffpassword")
        admin = Admin(u_ID=2, email="admin@example.com", password="adminpassword")
        db.session.add(staff)
        db.session.add(admin)
        db.session.commit()
    yield app
    with app.app_context():
        db.drop_all()

def test_validate_Staff(setup_app):
    """Test validating staff user."""
    staff = validate_Staff("staff@example.com", "staffpassword")
    assert staff is not None
    assert staff.email == "staff@example.com"

    invalid_staff = validate_Staff("staff@example.com", "wrongpassword")
    assert invalid_staff is None

def test_validate_Admin(setup_app):
    """Test validating admin user."""
    admin = validate_Admin("admin@example.com", "adminpassword")
    assert admin is not None
    assert admin.email == "admin@example.com"

    invalid_admin = validate_Admin("admin@example.com", "wrongpassword")
    assert invalid_admin is None

def test_get_user(setup_app):
    """Test retrieving a user."""
    staff = get_user("staff@example.com", "staffpassword")
    assert staff is not None
    assert staff.email == "staff@example.com"

    admin = get_user("admin@example.com", "adminpassword")
    assert admin is not None
    assert admin.email == "admin@example.com"

    invalid_user = get_user("nonexistent@example.com", "password")
    assert invalid_user is None

def test_get_uid(setup_app):
    """Test retrieving user ID by email."""
    uid = get_uid("staff@example.com")
    assert uid == 1

    no_uid = get_uid("nonexistent@example.com")
    assert no_uid is None