import pytest
from App.models.programme import *

'''
Unit Tests
'''
@pytest.mark.unit
def test_programme_initialization():
    programme = Programme("Computer Science")
    
    assert programme.p_name == "Computer Science"
    assert programme.p_ID == None

@pytest.mark.unit    
def test_programme_to_json():
    programme = Programme("Computer Science")
    programmedict = {
    "p_ID" : None,
    "name" : "Computer Science"
    }
    assert programme.to_json() == programmedict