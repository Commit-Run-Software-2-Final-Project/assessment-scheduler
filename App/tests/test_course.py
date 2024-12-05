# App/tests/conftest.py
import pytest
from App.database import db
from App import create_app
from App.models import Course 

from App.controllers.course import add_Course, list_Courses, get_course


'''
Unit Tests
'''

@pytest.fixture(scope='function')
def _db(test_app):
    """Create database tables for the entire test session"""
    with test_app.app_context():
        db.create_all()
        yield db
        db.drop_all()

@pytest.fixture(scope='function')
def session(test_app, _db):
    """Create a new database session for each test function"""
    connection = _db.engine.connect()
    transaction = connection.begin()
    
    try:
        # Create a new session
        session = _db.session
        yield session
    finally:
        # Roll back the transaction and close the connection
        transaction.rollback()
        connection.close()

# App/tests/test_course.py


@pytest.mark.unit
def test_add_course_new(test_app, session):
    """Test adding a completely new course"""
    with test_app.app_context():
        new_course, message = add_Course(
            "COMP3613", "Software Engineering II", "Basics of software engineering", 3, 1, 1
        )
        assert new_course.courseCode == "COMP3613"
        assert new_course.courseTitle == "Software Engineering II"
        assert Course.query.get("COMP3613") is not None


@pytest.mark.unit
def test_add_course_existing(test_app, session):
    """Test adding a course that already exists"""
    with test_app.app_context():
        add_Course("COMP3613", "Software Engineering II", "Basics of software engineering", 3, 1, 1)
        course, message = add_Course(
            "COMP3613", "Software Engineering II", "Basics of software engineering", 3, 1, 1
        )
        assert message == "Course code already exists"
        assert course is None

@pytest.mark.unit
def test_add_course_invalid_data(test_app, session):
    """Test adding a course with invalid data"""
    with test_app.app_context():
        with pytest.raises(ValueError, match="Missing required fields: courseCode"):
            add_Course(None, "Invalid Course", "No course code", 3, 1, 1)

        with pytest.raises(ValueError, match="Invalid numeric values for level"):
            add_Course("COMP9999", "Invalid Course", "Invalid level", -1, 1, 1)


@pytest.mark.unit
def test_list_courses(test_app, session):
    """Test listing all courses"""
    with test_app.app_context():
        add_Course("COMP3613", "Software Engineering II", "Description 1", 3, 1, 1)
        add_Course("COMP3603", "Human-Computer Interaction", "Description 2", 3, 2, 1)
        courses = list_Courses()
        assert len(courses) == 2

@pytest.mark.unit
def test_get_course(test_app, session):
    """Test retrieving a specific course"""
    with test_app.app_context():
        add_Course("COMP3613", "Software Engineering II", "Basics of software engineering", 3, 1, 1)
        course = get_course("COMP3613")
        assert course.courseCode == "COMP3613"
        
@pytest.mark.unit
def test_course_to_json():
    """Test the to_json method of the Course model"""
    course = Course("COMP3613", "Software Engineering II", "Basics of software engineering", 3, 1, 1)
    course_json = course.to_json()
    
    assert course_json["courseCode"] == "COMP3613"
    assert course_json["courseTitle"] == "Software Engineering II"
    assert course_json["description"] == "Basics of software engineering"
    assert course_json["level"] == 3
    assert course_json["semester"] == 1
    assert course_json["aNum"] == 1


'''
Integration tests
'''

@pytest.mark.integration
def test_integration_add_and_get_course(test_app, session):
    """Integration test for adding and retrieving a course"""
    with test_app.app_context():
        add_Course("COMP3613", "Software Engineering II", "Basics of software engineering", 3, 1, 1)
        course = get_course("COMP3613")
        assert course.courseTitle == "Software Engineering II"


@pytest.mark.integration
def test_integration_add_and_list_courses(test_app, session):
    """Integration test for adding multiple courses and listing them"""
    with test_app.app_context():
        add_Course("COMP3613", "Software Engineering II", "Description 1", 3, 1, 1)
        add_Course("COMP3603", "Human-Computer Interaction", "Description 2", 3, 2, 1)
        courses = list_Courses()
        course_codes = {course.courseCode for course in courses}
        assert "COMP3613" in course_codes
        assert "COMP3603" in course_codes


@pytest.mark.integration
def test_delete_course(test_app, session):
    """Test deleting a course"""
    with test_app.app_context():
        # Add a course first
        add_Course("COMP3613", "Software Engineering II", 
                   "Basics of software engineering", 3, 1, 1)
        
        # Verify the course exists
        course = Course.query.get("COMP3613")
        assert course is not None
        
        # Delete the course
        result = Course.query.get("COMP3613")
        session.delete(result)
        session.commit()
        deleted_course = Course.query.get("COMP3613")
        assert deleted_course is None

@pytest.mark.integration
def test_delete_nonexistent_course(test_app, session):
    """Test deleting a course that does not exist"""
    with test_app.app_context():
        # Attempt to delete a non-existent course
        non_existent = Course.query.get("NONEXIST")
        assert non_existent is None

@pytest.mark.integration
def test_add_course_invalid_data(test_app, session):
    """Test adding a course with missing or invalid data"""
    with test_app.app_context():
        # Missing fields should raise ValueError
        with pytest.raises(ValueError, match="Missing required fields: courseCode"):
            add_Course(None, "Invalid Course", "No course code", 3, 1, 1)

        # Invalid numeric values should raise ValueError
        with pytest.raises(ValueError, match="Invalid numeric values for level"):
            add_Course("COMP9999", "Invalid Course", "Invalid level", -1, 1, 1)

