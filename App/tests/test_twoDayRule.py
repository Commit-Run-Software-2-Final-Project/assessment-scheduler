import pytest
from datetime import date
from ..models.twoDayRule import TwoDayRule

class MockAssessment:
    def __init__(self, startDate):
        self.startDate = startDate
@pytest.mark.unit
def test_no_clash():
    rule = TwoDayRule()
    assessments = [MockAssessment(date(2023, 10, 10))]
    assert not rule.check_clash(date(2023, 10, 7), assessments)
@pytest.mark.unit
def test_clash_within_two_days():
    rule = TwoDayRule()
    assessments = [MockAssessment(date(2023, 10, 10))]
    assert rule.check_clash(date(2023, 10, 9), assessments)
@pytest.mark.unit
def test_clash_exactly_two_days():
    rule = TwoDayRule()
    assessments = [MockAssessment(date(2023, 10, 10))]
    assert rule.check_clash(date(2023, 10, 8), assessments)
@pytest.mark.unit
def test_no_clash_more_than_two_days():
    rule = TwoDayRule()
    assessments = [MockAssessment(date(2023, 10, 10))]
    assert not rule.check_clash(date(2023, 10, 5), assessments)
@pytest.mark.unit
def test_multiple_assessments_no_clash():
    rule = TwoDayRule()
    assessments = [MockAssessment(date(2023, 10, 9)), MockAssessment(date(2023, 10, 15))]
    assert not rule.check_clash(date(2023, 10, 12), assessments)
@pytest.mark.unit
def test_multiple_assessments_with_clash():
    rule = TwoDayRule()
    assessments = [MockAssessment(date(2023, 10, 10)), MockAssessment(date(2023, 10, 15))]
    assert rule.check_clash(date(2023, 10, 9), assessments)