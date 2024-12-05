# import pytest
# from datetime import date
# from App.models.semester import *
# from App.controllers.semester import *
# '''
# Unit Tests
# '''
# @pytest.mark.unit
# def test_semester_initialization():
#     semester = Semester(
#     startDate=date(2024, 1, 15),
#     endDate=date(2024, 5, 30),
#     semNum=2,
# )
#     assert semester.startDate == date(2024,1,15)
#     assert semester.endDate == date(2024, 5, 30)
#     assert semester.semNum == 2
    
# @pytest.mark.unit
# def test_semester_to_json():
#     semester = Semester(
#     startDate=date(2024, 1, 15),
#     endDate=date(2024, 5, 30),
#     semNum=2,
#     maxAssessments=10
# )
#     expectedDict = {
#     "id": None,
#     "startDate": date(2024, 1, 15),
#     "endDate": date(2024, 5, 30),
#     "semNum": 2,
#     "maxAssessments": 10
# }   
#     assert expectedDict == semester.to_json()

# @pytest.mark.integration    
# def test_add_sem(test_app, session):
#     add_sem(date(2024, 1, 15),date(2024, 5, 30), 2, 10)
#     semester = Semester.query.get(1)
    
#     assert semester.startDate == date(2024,1,15)
#     assert semester.endDate == date(2024, 5, 30)
#     assert semester.semNum == 2
#     assert semester.maxAssessments == 10
    
    
import pytest
from datetime import date
from App.models.semester import *
from App.controllers.semester import *

'''
Unit Tests
'''

@pytest.mark.unit
def test_semester_initialization():
    """Test initialization without maxAssessments field"""
    semester = Semester(
        startDate=date(2024, 1, 15),
        endDate=date(2024, 5, 30),
        semNum=2
    )
    assert semester.startDate == date(2024, 1, 15)
    assert semester.endDate == date(2024, 5, 30)
    assert semester.semNum == 2


@pytest.mark.unit
def test_semester_to_json():
    """Test the to_json method with maxAssessments"""
    semester = Semester(
        startDate=date(2024, 1, 15),
        endDate=date(2024, 5, 30),
        semNum=2,
        maxAssessments=10
    )
    expectedDict = {
        "id": None,
        "startDate": date(2024, 1, 15),
        "endDate": date(2024, 5, 30),
        "semNum": 2,
        "maxAssessments": 10
    }
    assert expectedDict == semester.to_json()


'''
Integration Tests
'''

@pytest.mark.integration    
def test_add_sem(test_app, session):
    """Test adding a semester with maxAssessments"""
    add_sem(date(2024, 1, 15), date(2024, 5, 30), 2, 10)
    semester = Semester.query.get(1)
    
    assert semester.startDate == date(2024, 1, 15)
    assert semester.endDate == date(2024, 5, 30)
    assert semester.semNum == 2
    assert semester.maxAssessments == 10
