from App.database import db
from datetime import datetime


class Semester(db.Model):
    __tablename__='semester'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    startDate = db.Column(db.Date, nullable=False)
    endDate = db.Column(db.Date, nullable=False) 
    semNum = db.Column(db.Integer, nullable=False)

<<<<<<< HEAD
    def __init__(self, startDate, endDate, semNum):
        self.startDate = datetime.strptime(startDate, '%Y-%m-%d').date()
        self.endDate = datetime.strptime(endDate, '%Y-%m-%d').date()
        self.semNum = int(semNum)

    def to_json(self):
        return {
            "id": self.id,
            "startDate": self.startDate,
            "endDate": self.endDate,
            "semNum": self.semNum
        }
    
    
    
=======
    def __init__(self, startDate, endDate, semNum, maxAssessments):
        self.startDate = startDate
        self.endDate = endDate
        self.semNum = semNum
        self.maxAssessments = maxAssessments

    def to_json(self):
        return{
            "id":self.id,
            "startDate":self.startDate,
            "endDate":self.endDate,
            "semNum":self.semNum,
            "maxAssessments":self.maxAssessments
        }
>>>>>>> 3692f5a1238c8c25b244b3f5474bf384f9de02c6
