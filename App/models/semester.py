from App.database import db
from datetime import datetime

class Semester(db.Model):
    __tablename__ = 'semester'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    startDate = db.Column(db.Date, nullable=False)
    endDate = db.Column(db.Date, nullable=False)
    semNum = db.Column(db.Integer, nullable=False)
    maxAssessments = db.Column(db.Integer, default=10)

    def __init__(self, startDate, endDate, semNum, maxAssessments=10):
        self.startDate = startDate
        self.endDate = endDate
        self.semNum = int(semNum)
        self.maxAssessments = maxAssessments

    def to_json(self):
        return {
            "id": self.id,
            "startDate": self.startDate,
            "endDate": self.endDate,
            "semNum": self.semNum,
            "maxAssessments": self.maxAssessments
        }