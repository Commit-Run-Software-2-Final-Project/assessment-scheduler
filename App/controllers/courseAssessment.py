from App.models import CourseAssessment
from App.models import Assessment
from App.models import Course
from App.models import TwoDayRule, OneWeekRuleStrategy
from App.database import db


def add_CourseAsm(courseCode, a_ID, startDate, endDate, startTime, endTime, clashDetected, clashRule=None):
    newAsg = CourseAssessment(courseCode, a_ID, startDate, endDate, startTime, endTime, clashDetected)
    if clashRule:
        newAsg.clashRule = clashRule
    db.session.add(newAsg)  #add to db
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
    return CourseAssessment.query.filter_by(courseCode=code).all()

def get_CourseAsm_level(level):
    courses = Course.query(level=level).all()
    assessments=[]
    for c in courses:
        assessments = assessments + get_CourseAsm_code(c)
    return assessments

def delete_CourseAsm(course_assessment):
    # Merge the object into the current session if it's detached
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
    if not assessment:
        return False
        
    # Get the appropriate strategy
    if not assessment.clashRule:
        return False
        
    strategy = None
    if assessment.clashRule == "OneWeekRuleStrategy":
        strategy = OneWeekRuleStrategy()
    elif assessment.clashRule == "TwoDayRule":
        strategy = TwoDayRule()
        
    if strategy:
        # Check for clashes against all relevant assessments
        return strategy.check_clash(assessment.startDate, [a for a in assessments if a.id != assessment.id])
        
    return False


def check_clashes(courseAssessmentID):
    courseAssessment = CourseAssessment.query.get(courseAssessmentID)
    print(courseAssessment)

def get_clashes():
    return CourseAssessment.query.filter_by(clashDetected=True).all()
