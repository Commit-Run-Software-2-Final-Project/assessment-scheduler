from flask import Blueprint, flash, redirect, request, jsonify, render_template, url_for, make_response
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, current_user
from flask_login import logout_user
from App.controllers.auth import login
from App.models.user import User
from App.models.staff import Staff
from App.models.admin import Admin
from App.database import db

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')

@auth_views.route('/login', methods=['GET'])
def get_login_page():
    return render_template('login.html')
    
@auth_views.route('/login', methods=['POST'])
def login_action():
    email = request.form.get('email')
    password = request.form.get('password')
    response = login_user(email, password)
    if isinstance(response, tuple) and response[1] == 401:
        flash('Invalid email or password')
        return redirect(url_for('auth_views.get_login_page'))
    return response

def login_user(email, password):
    admin_user = db.session.query(Admin).filter(Admin.email == email).first()
    if admin_user and admin_user.check_password(password):
        response = make_response(redirect(url_for('admin_views.get_upload_page')))    
        token = create_access_token(identity=email)
        response.set_cookie('access_token', token)
        return response
    
    user = db.session.query(Staff).filter(Staff.email == email).first()
    if user and user.check_password(password):
        response = make_response(redirect(url_for('staff_views.get_calendar_page')))
        token = create_access_token(identity=email)
        response.set_cookie('access_token', token)
        return response
        
    return ('Invalid username or password', 401)

@auth_views.route('/logout', methods=['GET'])
@jwt_required()
def logout():
    email=get_jwt_identity()
    print(email)
    logout_user()
    return render_template('login.html')
