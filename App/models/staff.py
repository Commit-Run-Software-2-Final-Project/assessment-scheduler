import flask_login
from App.database import db
from .user import User
import enum
from flask_login import UserMixin

class Status(enum.Enum):
    PTINSTRUCT = "Part-Time Instructor"
    INSTRUCTOR = "Instructor"
    HOD = "Head of Department"
    LECTURER = "Lecturer"
    TA = "Teaching Assisstant"
    TUTOR = "Tutor"
    PTTUTOR = "Part-Time Tutor"

class Staff(User,UserMixin):
  __tablename__ = 'staff'
  fName = db.Column(db.String(120), nullable=False)
  lName = db.Column(db.String(120), nullable=False)
  cNum = db.Column(db.Integer, nullable=False, default=0) #changes depending on status
  status = db.Column(db.Enum(Status), nullable = False) #defines the contract position of a teaching staff member
  #creates reverse relationship from Staff back to Course to access courses assigned to a specific lecturer
  coursesAssigned = db.relationship('CourseStaff', backref='courses', lazy='joined')

  def __init__(self, fName, lName, u_ID, status, email, password):
    super().__init__(u_ID, password, email)
    self.fName = fName
    self.lName = lName
    if status == "Lecturer 1" or  "Lecturer 2" or  "Lecturer 3": #assign number of courses to staff depending on status
      self.status = Status.LECTURER 
      self.cNum = 2
    else: 
      self.cNum = 3 #Instructor
    
    
  def get_id(self):
    return self.u_ID 

  def to_json(self):
    return {
        "staff_ID": self.u_ID,
        "firstname": self.fName,
        "lastname": self.lName,
        "status": self.status,
        "email": self.email,
        "coursesNum": self.cNum,
        "coursesAssigned": [course.to_json() for course in self.coursesAssigned]
    }
    
  def login(self):
    return flask_login.login_user(self)

