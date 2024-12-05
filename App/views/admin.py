from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_jwt_extended import jwt_required
from App.controllers import Course, CourseAssessment
from App.models import Admin
from App.database import db
from werkzeug.utils import secure_filename
import os, csv
from datetime import datetime

from App.controllers.course import (
    add_Course,
    list_Courses,
    get_course,
    delete_Course,
    edit_course
)

from App.controllers.semester import(
    add_sem
)

from App.controllers.courseAssessment import(
    get_clashes,
    get_CourseAsm_id
)

admin_views = Blueprint('admin_views', __name__, template_folder='../templates')

# Gets Semester Details Page
@admin_views.route('/semester', methods=['GET'])
@jwt_required(Admin)
def get_upload_page():
    return render_template('semester.html')

@admin_views.route('/uploadFiles', methods=['GET'])
@jwt_required(Admin)
def get_uploadFiles_page():
    return render_template('uploadFiles.html')

# Gets Course Listings Page
@admin_views.route('/coursesList', methods=['GET'])
@jwt_required(Admin)
def index():
    return render_template('courses.html')    

# Retrieves semester details and stores it in global variables 
@admin_views.route('/newSemester', methods=['POST'])
@jwt_required(Admin)
def new_semester_action():
    if request.method == 'POST':
        try:
            # Get form data
            semBegins = request.form.get('teachingBegins')
            semEnds = request.form.get('teachingEnds')
            semChoice = request.form.get('semester')
            
            # Additional server-side validation
            if not all([semBegins, semEnds, semChoice]):
                flash('All fields are required')
                return redirect(url_for('admin_views.get_upload_page'))
                
            # Create new semester
            add_sem(semBegins, semEnds, semChoice)
            flash('Semester details saved successfully')
            return render_template('uploadFiles.html')
            
        except Exception as e:
            flash(f'Error: {str(e)}')
            return redirect(url_for('admin_views.get_upload_page'))

    return redirect(url_for('admin_views.get_upload_page'))

# Gets csv file with course listings, parses it to store course data and stores it in application
@admin_views.route('/uploadcourse', methods=['POST'])
@jwt_required(Admin)
def upload_course_file():
    if request.method == 'POST': 
        file = request.files['file'] 

        # Check if file is present
        if (file.filename == ''):
            message = 'No file selected!' 
            return render_template('uploadFiles.html', message = message) 
        else:
            # Secure filename
            filename = secure_filename(file.filename)
        
            # Save file to uploads folder
            file.save(os.path.join('App/uploads', filename)) 
            
            # Retrieves course details from file and stores it in database ie. store course info 
            fpath = 'App/uploads/' + filename
            with open(fpath, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    #create object
                    course = add_Course(courseCode=row['Course Code'], courseTitle=row['Course Title'], description=row['Course Description'], level=int(row['Level']), semester=int(row['Semester']), aNum=int(row['Assessment No.']))

            # Redirect to view course listings!   
            return redirect(url_for('admin_views.get_courses'))    
            
# Pull course list from database
@admin_views.route('/get_courses', methods=['GET'])
@jwt_required(Admin)
def get_courses():
    courses = list_Courses()
    return render_template('courses.html', courses=courses)

# Gets Add Course Page
@admin_views.route('/newCourse', methods=['GET'])
@jwt_required(Admin)
def get_new_course():
    return render_template('addCourse.html')  

# Retrieves course info and stores it in database ie. add new course
@admin_views.route('/addNewCourse', methods=['POST'])
@jwt_required(Admin)
def add_course_action():
    if request.method == 'POST':
        courseCode = request.form.get('course_code')
        title = request.form.get('title')
        description = request.form.get('description')
        data = request.form
        level = request.form.get('level')
        semester = request.form.get('semester')
        numAssessments = request.form.get('numAssessments')
         
        course = add_Course(courseCode,title,description,level,semester,numAssessments)

        # Redirect to view course listings!  
        return redirect(url_for('admin_views.get_courses')) 
        
# Gets Update Course Page
@admin_views.route('/modifyCourse/<string:courseCode>', methods=['GET'])
@jwt_required(Admin)
def get_update_course(courseCode):
    course = get_course(courseCode) # Gets selected course
    return render_template('updateCourse.html', course=course)  

# Selects new course details and updates existing course in database
@admin_views.route('/updateCourse', methods=['POST'])
@jwt_required(Admin)
def update_course():
    if request.method == 'POST':
        try:
            courseCode = request.form.get('code')
            
            # Validate course exists
            if not courseCode:
                flash("No course selected for update", "error")
                return redirect(url_for('admin_views.get_courses'))
                
            title = request.form.get('title')
            description = request.form.get('description')
            level = request.form.get('level')
            semester = request.form.get('semester')
            numAssessments = request.form.get('assessment')

            if not all([courseCode, title, description, level, semester, numAssessments]):
                flash("All fields are required", "error")
                return redirect(url_for('admin_views.get_update_course', courseCode=courseCode))

            # Check if course exists before updating
            existing_course = get_course(courseCode)
            if not existing_course:
                flash("Course not found", "error")
                return redirect(url_for('admin_views.get_courses'))

            course, message = edit_course(courseCode, title, description, level, semester, numAssessments)
            
            if course:
                flash(message, "success")
            else:
                flash(message, "error")
                return redirect(url_for('admin_views.get_update_course', courseCode=courseCode))

        except Exception as e:
            flash(f"An error occurred: {str(e)}", "error")
            return redirect(url_for('admin_views.get_update_course', courseCode=courseCode))

    return redirect(url_for('admin_views.get_courses'))

@admin_views.route("/deleteCourse/<string:courseCode>", methods=["POST"])
@jwt_required(Admin)
def delete_course_action(courseCode):
    if not courseCode:
        flash("Please select a course first", "error")
        return redirect(url_for('admin_views.get_courses'))
        
    if request.method == 'POST':
        try:
            course = get_course(courseCode)
            if not course:
                flash("Course not found", "error")
                return redirect(url_for('admin_views.get_courses'))
                
            success, message = delete_Course(courseCode)
            
            if success:
                flash(message, "success")
            else:
                flash(message, "error")
                
        except Exception as e:
            flash(f"An error occurred while deleting course: {str(e)}", "error")
            
    return redirect(url_for('admin_views.get_courses'))

@admin_views.route("/clashes", methods=["GET"])
@jwt_required(Admin)
def get_clashes_page():
    #for search
    all_assessments=CourseAssessment.query.all()
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    searchResults=[]
    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        for a in all_assessments:
            if start_date <= a.startDate <= end_date or start_date <= a.endDate <= end_date:
                searchResults.append(a)
    #for table
    assessments=get_clashes()
    return render_template('clashes.html',assessments=assessments,results=searchResults)



@admin_views.route("/acceptOverride/<int:aID>", methods=['POST'])
@jwt_required(Admin)
def accept_override(aID):
    ca=get_CourseAsm_id(aID)
    if ca:
        ca.clashDetected=False
        db.session.commit()
        print("Accepted override.")
    return redirect(url_for('admin_views.get_clashes_page'))

@admin_views.route("/rejectOverride/<int:aID>", methods=['POST'])
@jwt_required(Admin)
def reject_override(aID):
    ca=get_CourseAsm_id(aID)
    if ca:
        ca.clashDetected=False
        ca.startDate=None
        ca.endDate=None
        ca.startTime=None
        ca.endTime=None
        db.session.commit()
        print("Rejected override.")
    return redirect(url_for('admin_views.get_clashes_page'))