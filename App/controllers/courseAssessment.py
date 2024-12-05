from App.models import CourseAssessment
from App.models import Assessment
from App.models import Course
from App.models import TwoDayRule, OneWeekRuleStrategy
from App.database import db
from datetime import date, datetime, time


def validate_assessment_dates(start_date, end_date, start_time, end_time):
    """Validate assessment dates and times"""
    if not all([start_date, end_date, start_time, end_time]):
        return True  # Allow null dates/times
        
    # Convert strings to date/time objects if needed
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    if isinstance(start_time, str):
        start_time = datetime.strptime(start_time, '%H:%M').time()
    if isinstance(end_time, str):
        end_time = datetime.strptime(end_time, '%H:%M').time()

    # Compare dates
    if start_date > end_date:
        return False
        
    # If same day, compare times
    if start_date == end_date and start_time >= end_time:
        return False
        
    return True

def add_CourseAsm(courseCode, a_ID, startDate, endDate, startTime, endTime, clashDetected, clashRule=None):
    # Extract the level from the course code and convert to int
    level = int(courseCode[4])
    
    newAsg = CourseAssessment(courseCode, a_ID, startDate, endDate, startTime, endTime, clashDetected)
    if clashRule:
        newAsg.clashRule = clashRule
    db.session.add(newAsg)
    db.session.commit()
    
    # After adding, check for clashes with other assessments
    if startDate and endDate:  # Only check if dates are set
        other_assessments = get_CourseAsm_level(level)  # Pass the level number
        has_clash = check_clash(other_assessments, newAsg.id)
        if has_clash != clashDetected:
            newAsg.clashDetected = has_clash
            db.session.commit()
            
    return newAsg


def list_Assessments():
    return Assessment.query.all()  

def get_Assessment_id(aType):
    assessment=Assessment.query.filter_by(category=aType).first()
    return assessment.a_ID

def get_Assessment_type(id):
    assessment=Assessment.query.filter_by(a_ID=id).first()
    return assessment.category.name

def get_CourseAsm_id(id):
    return CourseAssessment.query.filter_by(id=id).first()   

def get_CourseAsm_code(code):
    # Make sure we're getting a string course code
    if hasattr(code, 'courseCode'):  # If we got a Course object
        code = code.courseCode
    return CourseAssessment.query.filter_by(courseCode=code).all()

def get_CourseAsm_level(level):
    # Convert level to int if it's a string (like from courseCode[4])
    if isinstance(level, str):
        level = int(level)
    
    # Get all courses for this level
    courses = Course.query.filter_by(level=level).all()
    assessments = []
    for course in courses:
        # Pass the course code string rather than the Course object
        assessments.extend(get_CourseAsm_code(course.courseCode))
    return assessments

def delete_CourseAsm(course_assessment):
    if not db.session.is_active:
        db.session.add(course_assessment)
    else:
        course_assessment = db.session.merge(course_assessment)
        
    db.session.delete(course_assessment)
    db.session.commit()
    return True   

def setClashStrategy(assessmentID, strategyName):
    assessment = CourseAssessment.query.get(assessmentID)
    if not assessment:
        return None
        
    strategies = {
        "TwoDayRule": TwoDayRule(),
        "WeekRule": OneWeekRuleStrategy()
    }
    
    strategy = strategies.get(strategyName)
    if strategy:
        assessment.setClashRule(strategy)
        return assessment
    return None

def check_clash(assessments, assessmentID):
    assessment = CourseAssessment.query.get(assessmentID)
    if not assessment or not assessment.startDate or not assessment.endDate:
        return False
        
    if not assessment.clashRule:
        return False
        
    strategy = None
    if assessment.clashRule == "OneWeekRuleStrategy":
        strategy = OneWeekRuleStrategy()
    elif assessment.clashRule == "TwoDayRule":
        strategy = TwoDayRule()
        
    if strategy:
        relevant_assessments = [a for a in assessments 
                              if a.id != assessment.id 
                              and a.startDate and a.endDate]  # Only compare with dated assessments
        return strategy.check_clash(assessment.startDate, relevant_assessments)
        
    return False


def check_clashes(courseAssessmentID):
    courseAssessment = CourseAssessment.query.get(courseAssessmentID)
    print(courseAssessment)

def get_clashes():
    return CourseAssessment.query.filter_by(clashDetected=True).all()

def modify_assessment(id, asmType, startDate, endDate, startTime, endTime, clashRule=None):
    assessment = get_CourseAsm_id(id)
    if assessment:
        assessment.a_ID = asmType
        if startDate and endDate and startTime and endTime:
            assessment.startDate = datetime.strptime(startDate, '%Y-%m-%d').date()
            assessment.endDate = datetime.strptime(endDate, '%Y-%m-%d').date()
            
            try:
                assessment.startTime = datetime.strptime(startTime, '%H:%M:%S').time()
            except ValueError:
                assessment.startTime = datetime.strptime(startTime, '%H:%M').time()

            try:
                assessment.endTime = datetime.strptime(endTime, '%H:%M:%S').time()
            except ValueError:
                assessment.endTime = datetime.strptime(endTime, '%H:%M').time()

        if clashRule:
            if clashRule == "TwoDayRule":
                assessment.setClashRule(TwoDayRule())
            elif clashRule == "WeekRule":
                assessment.setClashRule(OneWeekRuleStrategy())

        db.session.commit()
        return assessment
    return None
