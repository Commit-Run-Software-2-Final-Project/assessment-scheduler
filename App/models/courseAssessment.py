from App.database import db
from .clashRuleStrategy import ClashRuleStrategy
from .twoDayRule import TwoDayRule
from .weekRule import OneWeekRuleStrategy
from datetime import datetime, date, time

class CourseAssessment(db.Model):
    __tablename__ = 'courseAssessment'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    courseCode = db.Column(db.String(9), db.ForeignKey('course.courseCode'), nullable=False)
    a_ID = db.Column(db.Integer, db.ForeignKey('assessment.a_ID'), nullable=False)
    startDate = db.Column(db.Date, nullable=True)
    endDate = db.Column(db.Date, nullable=True)
    startTime = db.Column(db.Time, nullable=True)
    endTime = db.Column(db.Time, nullable=True)
    clashDetected = db.Column(db.Boolean, default=False)
    clashRule = db.Column(db.String(50), nullable=True)

    def __init__(self, courseCode, a_ID, startDate, endDate, startTime, endTime, clashDetected):
        self.courseCode = courseCode
        self.a_ID = a_ID
        
        # Convert date strings to date objects if they're not None
        if startDate:
            if isinstance(startDate, str):
                self.startDate = datetime.strptime(startDate, '%Y-%m-%d').date()
            elif isinstance(startDate, date):
                self.startDate = startDate
            else:
                raise ValueError("startDate must be a string or date object")
                
        if endDate:
            if isinstance(endDate, str):
                self.endDate = datetime.strptime(endDate, '%Y-%m-%d').date()
            elif isinstance(endDate, date):
                self.endDate = endDate
            else:
                raise ValueError("endDate must be a string or date object")

        # Convert time strings to time objects if they're not None
        if startTime:
            if isinstance(startTime, str):
                self.startTime = datetime.strptime(startTime, '%H:%M').time()
            elif isinstance(startTime, time):
                self.startTime = startTime
            else:
                raise ValueError("startTime must be a string or time object")
                
        if endTime:
            if isinstance(endTime, str):
                self.endTime = datetime.strptime(endTime, '%H:%M').time()
            elif isinstance(endTime, time):
                self.endTime = endTime
            else:
                raise ValueError("endTime must be a string or time object")

        self.clashDetected = clashDetected

    def to_json(self):
        return {
            "assessmentNo": self.id,
            "courseCode": self.courseCode,
            "a_ID": self.a_ID,
            "startDate": self.startDate.isoformat() if self.startDate else None,
            "endDate": self.endDate.isoformat() if self.endDate else None,
            "startTime": self.startTime.isoformat() if self.startTime else None,
            "endTime": self.endTime.isoformat() if self.endTime else None,
            "clashDetected": self.clashDetected
        }

    def setClashRule(self, clashRule):
        if not isinstance(clashRule, ClashRuleStrategy):
            raise TypeError("clashRule must be an instance of ClashRuleStrategy")
        
        self.clashRule = clashRule.__class__.__name__
        print(clashRule.__class__.__name__)
    
    def getClashRule(self):
        if self.clashRule == "TwoDayRule":
            return TwoDayRule()
        elif self.clashRule == "OneWeekRuleStrategy":
            return OneWeekRuleStrategy()
        else:
            return None

    def addCourseAsg(self, courseCode, a_ID, startDate, endDate, startTime, endTime, clashDetected):
        newAsg = CourseAssessment(courseCode, a_ID, startDate, endDate, startTime, endTime, clashDetected)
        db.session.add(newAsg)
        db.session.commit()
        return newAsg