from App.models import CourseAssessment, Assessment, Course
from App.models.assessment.assessment_strategy import AssessmentStrategy
from App.models.stratergies.group_one_strategy import GroupOneStrategy
from App.models.stratergies.group_two_strategy import GroupTwoStrategy
from App.database import db
from datetime import date, time

def get_strategy(course_code: str) -> AssessmentStrategy:
    """Determine which strategy to use based on course code"""
    """EXAMPLE SUBJECT TO CHANGE"""
    # if len(course_code) >= 4 and course_code[:4] in ['COMP', 'INFO', 'TECH']:
    #     return GroupOneStrategy()
    # return GroupTwoStrategy()

def add_CourseAsm(courseCode, a_ID, startDate, endDate, startTime, endTime, clashDetected=False):
    try:
        # Create new assessment
        newAsg = CourseAssessment(courseCode, a_ID, startDate, endDate, startTime, endTime, clashDetected)
        
        # Get appropriate strategy and validate
        strategy = get_strategy(courseCode)
        
        if not strategy.validate_assessment(newAsg):
            return None
            
        # Check for conflicts
        newAsg.clashDetected = strategy.check_conflicts(newAsg)
        
        # Save to database
        db.session.add(newAsg)
        db.session.commit()
        return newAsg
        
    except Exception as e:
        db.session.rollback()
        print(f"Error adding course assessment: {str(e)}")
        return None

def list_Assessments():
    return Assessment.query.all()

def get_Assessment_id(aType):
    assessment = Assessment.query.filter_by(category=aType).first()
    return assessment.a_ID if assessment else None

def get_Assessment_type(id):
    assessment = Assessment.query.filter_by(a_ID=id).first()
    return assessment.category.name if assessment else None

def get_CourseAsm_id(id):
    return CourseAssessment.query.filter_by(id=id).first()

def get_CourseAsm_code(code):
    return CourseAssessment.query.filter_by(courseCode=code).all()

def get_CourseAsm_level(level):
    courses = Course.query.filter_by(level=level).all()
    assessments = []
    for c in courses:
        course_assessments = get_CourseAsm_code(c.courseCode)
        assessments.extend(course_assessments)
    return assessments

def delete_CourseAsm(courseAsm):
    try:
        db.session.delete(courseAsm)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting course assessment: {str(e)}")
        return False

def get_clashes():
    return CourseAssessment.query.filter_by(clashDetected=True).all()

# For backward compatibility
def addCourseAsg(courseCode, a_ID, startDate, endDate, startTime, endTime, clashDetected=False):
    return add_CourseAsm(courseCode, a_ID, startDate, endDate, startTime, endTime, clashDetected)