from App.models import User, Admin, Staff
    

def validate_Staff(email, password):
    staff = Staff.query.filter_by(email=email).first()
    if staff and staff.check_password(password):
        return staff
    return None


def validate_Admin(email, password):
    admin = Admin.query.filter_by(email=email).first()
    if admin and admin.check_password(password):
        return admin
    return None

def get_user(email, password):
    user = validate_Staff(email, password)
    if user != None:
        return user
    user = validate_Admin(email, password)
    if user !=None:
        return user
    return None

def get_uid(email):
    user = Staff.query.filter_by(email=email).first()
    if not user: 
        return None
    return user.u_ID