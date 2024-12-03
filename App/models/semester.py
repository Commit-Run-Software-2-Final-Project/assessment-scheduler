from App.database import db
from datetime import datetime


class Semester(db.Model):
    __tablename__='semester'
    id = db.Column(db.Integer, primary_key= True, autoincrement=True)
    startDate = db.Column(db.Date,nullable=False)
    endDate = db.Column(db.Date,nullable=False)
    semNum = db.Column(db.Integer,nullable=False)
    maxAssessments = db.Column(db.Integer,nullable=False)

    def __init__(self, startDate, endDate, semNum, maxAssessments):
        # Convert string dates to Python date objects
        self.startDate = datetime.strptime(startDate, '%Y-%m-%d').date()
        self.endDate = datetime.strptime(endDate, '%Y-%m-%d').date()
        self.semNum = int(semNum)
        self.maxAssessments = int(maxAssessments)

def to_json(self):
    return{
        "id":self.id,
        "startDate":self.startDate,
        "endDate":self.endDate,
        "semNum":self.semNum,
        "maxAssessments":self.maxAssessments
    }