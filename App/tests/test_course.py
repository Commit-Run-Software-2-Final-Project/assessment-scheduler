# App/tests/conftest.py
import pytest
from App.database import db
from App import create_app
from App.models import Course  # Import all your models here

@pytest.fixture(scope='session')
def app():
    """Create and configure a test app instance"""
    app = create_app('testing')
    return app

@pytest.fixture(scope='session')
def client(app):
    """Create a test client using the app fixture"""
    return app.test_client()

@pytest.fixture(scope='session')
def _db(app):
    """Create database tables for the entire test session"""
    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()

@pytest.fixture(scope='function')
def session(app, _db):
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
import pytest
from App.models import Course
from App.controllers.course import add_Course, list_Courses, get_course
from App.database import db

def test_add_course_new(app, session):
    """Test adding a completely new course"""
    with app.app_context():
        # Call the function to add a new course
        new_course = add_Course("COMP3613", "Software Engineering II", 
                                 "Basics of software engineering", 3, 1, 0)
        
        # Verify course details
        assert new_course.courseCode == "COMP3613"
        assert new_course.courseTitle == "Software Engineering II"
        
        # Verify the course was actually added to the database
        retrieved_course = Course.query.get("COMP3613")
        assert retrieved_course is not None

def test_add_course_existing(app, session):
    """Test adding a course that already exists"""
    with app.app_context():
        # First, add the initial course
        initial_course = add_Course("COMP3613", "Software Engineering II", 
                                     "Basics of software engineering", 3, 1, 0)
        
        # Try to add the same course again
        returned_course = add_Course("COMP3613", "Software Engineering II", 
                                      "Basics of software engineering", 3, 1, 0)
        
        # Verify the returned course is the same as the initial course
        assert returned_course.courseCode == initial_course.courseCode

def test_list_courses(app, session):
    """Test listing all courses"""
    with app.app_context():
        # Add some courses
        add_Course("COMP3613", "Software Engineering II", "Description 1", 3, 1, 0)
        add_Course("COMP3603", "Human-Computer Interaction", "Description 2", 3, 2, 0)
        
        # Get the list of courses
        courses = list_Courses()
        
        # Verify the number of courses
        assert len(courses) >= 2

def test_get_course(app, session):
    """Test retrieving a specific course"""
    with app.app_context():
        # Add a course first
        add_Course("COMP3613", "Software Engineering II", 
                   "Basics of software engineering", 3, 1, 0)
        
        # Retrieve the course
        course = get_course("COMP3613")
        
        # Verify the course details
        assert course is not None
        assert course.courseCode == "COMP3613"
        assert course.courseTitle == "Software Engineering II"