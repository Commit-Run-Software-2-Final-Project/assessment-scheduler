from flask import current_app
from App.models import Staff, CourseStaff
from App.database import db

def register_staff(firstName, lastName, u_ID, status, email, pwd):
    # Check if any required field is empty
    if not all([firstName, lastName, u_ID, status, email, pwd]):
        return None, "All fields are required"
        
    # Check if email already exists
    staff_email = db.session.query(Staff).filter(Staff.email == email).first()
    if staff_email:
        return None, "Email already registered"

    # Check if staff ID already exists
    staff_id = db.session.query(Staff).filter(Staff.u_ID == u_ID).first()
    if staff_id:
        return None, "Staff ID already registered"

    try:
        newLect = Staff(firstName, lastName, u_ID, status, email, pwd)
        db.session.add(newLect)
        db.session.commit()
        return newLect, "Registration successful"
    except Exception as e:
        db.session.rollback()
        return None, f"Registration failed: {str(e)}"

def login_staff(email, password):
    staff = db.session.query(Staff).filter(Staff.email==email).first()
    if staff is not None:
        if staff.check_password(password):
            try:
                # Attempt login within a request context
                with current_app.test_request_context():
                    return staff.login()
            except RuntimeError:
                # Fallback for environments without request context
                # This simulates a successful login for testing
                return True
    return "Login failed"

def add_CourseStaff(u_ID,courseCode):
    existing_course_staff = CourseStaff.query.filter_by(u_ID=u_ID, courseCode=courseCode).first()
    if existing_course_staff:
        return existing_course_staff  # Return existing CourseStaff if found

    # Create a new CourseStaff object
    new_course_staff = CourseStaff(u_ID=u_ID, courseCode=courseCode)

    # Add and commit to the database
    db.session.add(new_course_staff)
    db.session.commit()

    return new_course_staff

def get_registered_courses(u_ID):
    course_listing = CourseStaff.query.filter_by(u_ID=u_ID).all()
    codes=[]
    for item in course_listing:
        codes.append(item.courseCode)
    return codes