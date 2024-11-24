from App.controllers.stratergies.assesmentStrategy import AssessmentStrategy
from App.database import db
from datetime import date, time
from typing import Dict, Any


class CourseAssessment(db.Model):
    __tablename__ = 'courseAssessment'
    
    # Primary Key and Foreign Keys from diagram
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    courseCode = db.Column(db.String(9), db.ForeignKey('course.courseCode'), nullable=False)
    a_ID = db.Column(db.Integer, db.ForeignKey('assessment.a_ID'), nullable=False)
    
    # Date and Time fields
    startDate = db.Column(db.Date, nullable=True)
    endDate = db.Column(db.Date, nullable=True)
    startTime = db.Column(db.Time, nullable=True)
    endTime = db.Column(db.Time, nullable=True)
    clashDetected = db.Column(db.Boolean, default=False)
    
    # Strategy pattern - This will be handled in memory, not stored in DB
    _assessment_strategy = None

    def __init__(self, courseCode: str, a_ID: int, startDate: date, 
                 endDate: date, startTime: time, endTime: time, 
                 clashDetected: bool = False):
        self.courseCode = courseCode
        self.a_ID = a_ID
        self.startDate = startDate
        self.endDate = endDate
        self.startTime = startTime
        self.endTime = endTime
        self.clashDetected = clashDetected

    def set_strategy(self, strategy: AssessmentStrategy) -> None:
        """Set the assessment strategy to be used"""
        self._assessment_strategy = strategy

    def schedule_assessment(self) -> bool:
        """
        Schedule the assessment using the current strategy.
        Returns True if scheduling is successful, False otherwise.
        """
        if not self._assessment_strategy:
            raise ValueError("Assessment strategy not set")
            
        # First validate the assessment
        if not self._assessment_strategy.validate_assessment(self):
            return False
            
        # Then check for conflicts
        self.clashDetected = self._assessment_strategy.check_conflicts(self)
        
        # If no validation issues, save to database
        if not self.clashDetected:
            db.session.add(self)
            db.session.commit()
            return True
            
        return False

    def to_json(self) -> Dict[str, Any]:
        """Convert the assessment to a JSON-serializable dictionary"""
        return {
            "assessmentNo": self.id,
            "courseCode": self.courseCode,
            "a_ID": self.a_ID,
            "startDate": self.startDate,
            "endDate": self.endDate,
            "startTime": self.startTime,
            "endTime": self.endTime,
            "clashDetected": self.clashDetected
        }

    @classmethod
    def addCourseAsg(cls, courseCode: str, a_ID: int, startDate: date, 
                     endDate: date, startTime: time, endTime: time, 
                     clashDetected: bool = False) -> 'CourseAssessment':
        """Class method to create and add a new course assessment"""
        newAsg = cls(courseCode, a_ID, startDate, endDate, 
                    startTime, endTime, clashDetected)
        db.session.add(newAsg)
        db.session.commit()
        return newAsg