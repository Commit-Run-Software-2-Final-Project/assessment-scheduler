import pytest
from App.models import Staff, Status, CourseStaff
from App.database import db
from App import create_app

'''
Unit Tests
'''
@pytest.mark.unit
def test_staff_initialization():
    staff = Staff(
        fName="John",
        lName="Doe",
        u_ID="1",
        status="Lecturer 1",
        email="john.doe@example.com",
        password="securepassword"
    )
    assert staff.fName == "John"
    assert staff.lName == "Doe"
    assert staff.status == Status.LECTURER
    assert staff.cNum == 2
@pytest.mark.unit
def test_staff_to_json():
    staff = Staff(
        fName="John",
        lName="Doe",
        u_ID="1",
        status="Lecturer 1",
        email="john.doe@example.com",
        password="securepassword"
    )
    staff_json = staff.to_json()
    assert staff_json["firstname"] == "John"
    assert staff_json["lastname"] == "Doe"
    assert staff_json["status"] == Status.LECTURER
    assert staff_json["coursesNum"] == 2
    assert staff_json["coursesAssigned"] == []
@pytest.mark.unit
def test_login_success(mocker):
    mocker.patch("flask_login.login_user", return_value=True)
    staff = Staff(
        fName="Jane",
        lName="Doe",
        u_ID="2",
        status="Lecturer 1",
        email="jane.doe@example.com",
        password="securepassword"
    )
    assert staff.login() == True
@pytest.mark.unit
def test_login_failure(mocker):
    mocker.patch("flask_login.login_user", return_value=False)
    staff = Staff(
        fName="Jane",
        lName="Doe",
        u_ID="2",
        status="Lecturer 1",
        email="jane.doe@example.com",
        password="securepassword"
    )
    assert staff.login() == False

'''
Integration Tests
'''
@pytest.mark.integration
def test_login_staff_success(test_app, session):
    from App.controllers.staff import register_staff, login_staff
    
    with test_app.app_context():
        register_staff(
            firstName="John",
            lastName="Doe",
            u_ID="1",
            status="Instructor",
            email="john.doe@example.com",
            pwd="securepassword"
        )
        
        result = login_staff(email="john.doe@example.com", password="securepassword")
        assert result == True
        
@pytest.mark.integration
def test_register_staff_duplicate_email(test_app, session):
    from App.controllers.staff import register_staff
    register_staff(
        firstName="John",
        lastName="Doe",
        u_ID="1",
        status="Instructor",
        email="duplicate@example.com",
        pwd="securepassword"
    )
    duplicate, message = register_staff(
        firstName="Jane",
        lastName="Doe",
        u_ID="2",
        status="Instructor",
        email="duplicate@example.com",
        pwd="anotherpassword"
    )
    assert message == "Email already registered"
    assert duplicate is None
@pytest.mark.integration
def test_login_staff_success(test_app, session):
    from App.controllers.staff import register_staff, login_staff
    register_staff(
        firstName="John",
        lastName="Doe",
        u_ID="1",
        status="Instructor",
        email="john.doe@example.com",
        pwd="securepassword"
    )
    result = login_staff(email="john.doe@example.com", password="securepassword")
    assert result == True
@pytest.mark.integration
def test_login_staff_failure(test_app, session):
    from App.controllers.staff import login_staff
    result = login_staff(email="nonexistent@example.com", password="wrongpassword")
    assert result == "Login failed"
@pytest.mark.integration
def test_add_course_staff(test_app, session):
    from App.controllers.staff import add_CourseStaff
    course_staff = add_CourseStaff(u_ID=1, courseCode="COMP3601")
    assert course_staff is not None
    assert course_staff.u_ID == 1
    assert course_staff.courseCode == "COMP3601"
@pytest.mark.integration
def test_get_registered_courses(test_app, session):
    from App.controllers.staff import add_CourseStaff, get_registered_courses
    add_CourseStaff(u_ID=1, courseCode="COMP3601")
    add_CourseStaff(u_ID=1, courseCode="COMP3613")
    courses = get_registered_courses(u_ID=1)
    assert "COMP3601" in courses
    assert "COMP3613" in courses
