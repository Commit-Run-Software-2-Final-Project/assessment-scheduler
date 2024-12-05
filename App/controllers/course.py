from App.models import Course
from App.database import db

def add_Course(courseCode, courseTitle, description, level, semester, aNum):
    try:
        if not all([courseCode, courseTitle, description, level, semester, aNum]):
            return None, "All fields are required"
        
        # Check if course already exists
        existing_course = Course.query.get(courseCode)
        if existing_course:
            return None, "Course code already exists"
            
        # Validate numeric fields
        try:
            level = int(level)
            semester = int(semester)
            aNum = int(aNum)
        except ValueError:
            return None, "Level, semester, and number of assessments must be numeric"
            
        # Validate ranges
        if not (1 <= level <= 3):
            return None, "Level must be between 1 and 3"
        if not (1 <= semester <= 3):
            return None, "Semester must be between 1 and 3"
        if not (0 <= aNum <= 10):
            return None, "Number of assessments must be between 0 and 10"
            
        newCourse = Course(courseCode, courseTitle, description, level, semester, aNum)
        db.session.add(newCourse)
        db.session.commit()
        return newCourse, "Course added successfully"
    except Exception as e:
        db.session.rollback()
        return None, f"Failed to add course: {str(e)}"

def list_Courses():
    return Course.query.all() 

def get_course(courseCode):
    return Course.query.filter_by(courseCode=courseCode).first()

def edit_course(courseCode, title, description, level, semester, numAssessments):
    try:
        course = Course.query.get(courseCode)
        if not course:
            return None, "Course not found"
        
        course.courseTitle = title
        course.description = description
        course.level = level
        course.semester = semester
        course.aNum = numAssessments
        
        db.session.commit()
        return course, "Course updated successfully"
    except Exception as e:
        db.session.rollback()
        return None, f"Failed to update course: {str(e)}"

def delete_Course(courseCode):
    try:
        course = Course.query.get(courseCode)
        if not course:
            return False, "Course not found"
            
        db.session.delete(course)
        db.session.commit()
        return True, "Course deleted successfully"
    except Exception as e:
        db.session.rollback()
        return False, f"Failed to delete course: {str(e)}"
