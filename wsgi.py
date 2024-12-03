import click, sys, csv
from flask import Flask
from flask.cli import with_appcontext, AppGroup
from App.database import db, get_migrate
from App.main import create_app
from App.models import Staff, Course, Assessment, Programme, Admin, OneWeekRuleStrategy, TwoDayRule, CourseAssessment
from App.controllers import Course, setClashStrategy
from datetime import date, time

from App.controllers.course import (
    add_Course
)

# This commands file allow you to create convenient CLI commands for testing controllers!!
app = create_app()


@click.command(name='set_clash_rule')
@click.argument('assessment_id')
@click.argument('rule')
@with_appcontext
def set_clash_rule(assessment_id, rule):
    # Retrieve the CourseAssessment by ID
    course_assessment = CourseAssessment.query.get(assessment_id)
    
    if course_assessment is None:
        click.echo(f"CourseAssessment with ID {assessment_id} not found.")
        return

    # Set the clash rule based on the provided argument
    if rule == 'OneWeekRule':
        clash_rule = OneWeekRuleStrategy()
    elif rule == 'TwoDayRule':
        clash_rule = TwoDayRule()
    else:
        click.echo(f"Unknown clash rule: {rule}")
        return

    # Set the clash rule strategy
    course_assessment.setClashRule(clash_rule)
    db.session.commit()

    click.echo(f"Clash rule {rule} set for CourseAssessment ID {assessment_id}.")
@app.cli.command("teststuff")
def testing():
    course_code = "CS101"
    course_title = "Introduction to Computer Science"
    description = "A beginner course on computer science concepts."
    level = 100
    semester = 1
    a_num = 0

    course = Course(courseCode=course_code,
                    courseTitle=course_title,
                    description=description,
                    level=level,
                    semester=semester,
                    aNum=a_num)
    
    db.session.add(course)
    db.session.commit()

    #print(f"Course created with courseCode: {course.courseCode}")

    course_code = "CS101"
    assessment_id = 123
    start_date = date(2024, 11, 27)
    end_date = date(2024, 11, 28)
    start_time = time(10, 0)  # 10:00 AM
    end_time = time(12, 0) 
    clash_detected = False
    
    course_assessment = CourseAssessment(courseCode=course_code,
                                         a_ID=assessment_id,
                                         startDate=start_date,
                                         endDate=end_date,
                                         startTime=start_time,
                                         endTime=end_time,
                                         clashDetected=clash_detected)

    # print(f"TwoDayRule class name: {TwoDayRule.__name__}")
    # print(f"OneWeekRuleStrategy class name: {OneWeekRuleStrategy.__name__}")
    
    db.session.add(course_assessment)
    db.session.commit()
    
    #course_assessment.setClashRule(TwoDayRule())
    db.session.commit()
    setClashStrategy(1, "WeekRule")
    print(f"CourseAssessment created with ID {course_assessment.id}")
   
# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
  db.drop_all()
  # db.init_app(app)
  db.create_all()
  # bob = Staff("bob", "test", 300456, "Lecturer 1", "bob@gmail.com", "bobpass")
  bob = Admin(u_ID=999, email="bob@gmail.com", password="bobpass")
  db.session.add(bob)
  db.session.commit()
  print(bob)
  print('database initialized')

# This command retrieves all staff objects
@app.cli.command('get-users')
def get_users():
  staff = Staff.query.all()
  for s in staff:
    print(s.to_json())
  print('end of staff objects')

# This command creates all the Assessment objects
@app.cli.command("asm")
def load_Asm():
  db.create_all()
  asm1 = Assessment(category='EXAM')
  db.session.add(asm1)
  db.session.commit()

  asm2 = Assessment(category='ASSIGNMENT')
  db.session.add(asm2)
  db.session.commit()

  asm3 = Assessment(category='QUIZ')
  db.session.add(asm3)
  db.session.commit()

  asm4 = Assessment(category='PROJECT')
  db.session.add(asm4)
  db.session.commit()

  asm5 = Assessment(category='DEBATE')
  db.session.add(asm5)
  db.session.commit()

  asm6 = Assessment(category='PRESENTATION')
  db.session.add(asm6)
  db.session.commit()

  asm7 = Assessment(category='ORALEXAM')
  db.session.add(asm7)
  db.session.commit()

  asm8 = Assessment(category='PARTICIPATION')
  db.session.add(asm8)
  db.session.commit()
  print('All assessments added')

# This command creates all the Programme objects
@app.cli.command("pgr")
def load_Pgr():
  db.create_all()
  pgr1 = Programme(p_name='Computer Science Major')
  db.session.add(pgr1)
  db.session.commit()

  pgr2 = Programme(p_name='Computer Science Minor')
  db.session.add(pgr2)
  db.session.commit()

  pgr3 = Programme(p_name='Computer Science Special')
  db.session.add(pgr3)
  db.session.commit()

  pgr4 = Programme(p_name='Information Technology Major')
  db.session.add(pgr4)
  db.session.commit()

  pgr5 = Programme(p_name='Information Technology Minor')
  db.session.add(pgr5)
  db.session.commit()

  pgr6 = Programme(p_name='Information Technology Special')
  db.session.add(pgr6)
  db.session.commit()

  print('All programmes added')  

# This command assigns courses to staff
@app.cli.command("add-course")
@click.argument("staff_ID")
def assign_course(staff_ID):
  bob = Staff.query.filter_by(u_ID=staff_ID).first()
  
  if not bob:
      print(f'Staff with ID: {staff_ID} not found!')
      return
    
  bob.coursesAssigned = ["COMP1601", "COMP1602", "COMP1603"]
  db.session.add(bob)
  db.session.commit()
  print(bob)
  print('courses added')

#load course data from csv file
@app.cli.command("load-courses")
def load_course_data():
  with open('courses.csv') as file: #csv files are used for spreadsheets
    reader = csv.DictReader(file)
    for row in reader: 
      new_course = Course(courseCode=row['courseCode'], courseTitle=row['courseTitle'], description=row['description'], 
        level=row['level'], semester=row['semester'], preReqs=row['preReqs'], p_ID=row['p_ID'],)  #create object
      db.session.add(new_course) 
    db.session.commit() #save all changes OUTSIDE the loop
  print('database intialized')