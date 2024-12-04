import pytest
from unittest.mock import MagicMock
from App.controllers.admin import login_admin
from App.models.admin import Admin
from App.database import db
from App.main import create_app

'''
Unit Tests
'''

@pytest.fixture
def mock_db_session(mocker):
    """Mock the database session."""
    return mocker.patch('App.database.db.session')

@pytest.fixture
def mock_admin_class(mocker):
    """Mock the Admin class."""
    return mocker.patch('App.models.admin.Admin')

@pytest.mark.unit
def test_login_success(mock_db_session, mock_admin_class):
    mock_admin = MagicMock()
    mock_admin.check_password.return_value = True
    mock_admin.login.return_value = "Logged in"
    
    # Mock the query call to return the mock_admin
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_admin

    # Ensure that the call to login_admin is within a request context
    with mock_admin_class() as admin:
        result = login_admin("admin@example.com", "securepassword")
    
    assert result == "Logged in"
    mock_admin.check_password.assert_called_once_with("securepassword")
    mock_admin.login.assert_called_once()

@pytest.mark.unit
def test_login_failure_incorrect_email(mock_db_session, mock_admin_class):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None

    result = login_admin("wrongemail@example.com", "securepassword")
    
    assert result == "Login failed"

@pytest.mark.unit
def test_login_failure_incorrect_password(mock_db_session, mock_admin_class):
    mock_admin = MagicMock()
    mock_admin.check_password.return_value = False
    
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_admin

    result = login_admin("admin@example.com", "wrongpassword")
    
    assert result == "Login failed"
    mock_admin.check_password.assert_called_once_with("wrongpassword")
    mock_admin.login.assert_not_called()


'''
Integration Tests
'''


@pytest.mark.integration
def test_login_admin_success(test_app, client):
    # Arrange: Add an admin to the database
    with test_app.app_context():
        admin = Admin(u_ID=1, email="admin@example.com", password="securepassword")
        admin.set_password("securepassword")
        db.session.add(admin)
        db.session.commit()
        db.session.refresh(admin)

    # Act: Call the login_admin function via the test client
    response = client.post('/login', data=dict(email="admin@example.com", password="securepassword"))
    
    # Assert: Check the result
    assert response.status_code == 302
    assert response.location == '/semester'  

@pytest.mark.integration
def test_login_admin_failure_incorrect_email(test_app):
    # Arrange: Add an admin to the database
    with test_app.app_context():
        admin = Admin(u_ID=1, email="admin@example.com", password="securepassword")
        admin.set_password("securepassword")
        db.session.add(admin)
        db.session.commit()

    # Act: Attempt to log in with an incorrect email
    from App.controllers.admin import login_admin
    result = login_admin("nonexistent@example.com", "securepassword")

    # Assert: Check the result
    assert result == "Login failed"

@pytest.mark.integration
def test_login_admin_failure_incorrect_password(test_app):
    # Arrange: Add an admin to the database
    with test_app.app_context():
        admin = Admin(u_ID=1, email="admin@example.com", password="securepassword")
        admin.set_password("securepassword")
        db.session.add(admin)
        db.session.commit()

    # Act: Attempt to log in with an incorrect password
    from App.controllers.admin import login_admin
    result = login_admin("admin@example.com", "wrongpassword")

    # Assert: Check the result
    assert result == "Login failed"
