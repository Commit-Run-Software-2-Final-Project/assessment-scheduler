import pytest
from datetime import date, timedelta
from App.models.weekRule import OneWeekRuleStrategy

class Assessment:
    def __init__(self, startDate):
        self.startDate = startDate

@pytest.fixture
def one_week_rule_strategy():
    return OneWeekRuleStrategy()

def test_no_clash_with_empty_assessments(one_week_rule_strategy):
    assert one_week_rule_strategy.check_clash(date.today(), []) == True

def test_no_clash_with_assessments_outside_one_week(one_week_rule_strategy):
    assessments = [
        Assessment(date.today() - timedelta(days=8)),
        Assessment(date.today() + timedelta(days=8))
    ]
    assert one_week_rule_strategy.check_clash(date.today(), assessments) == True

def test_clash_with_assessment_within_one_week_before(one_week_rule_strategy):
    assessments = [
        Assessment(date.today() - timedelta(days=6))
    ]
    assert one_week_rule_strategy.check_clash(date.today(), assessments) == False

def test_clash_with_assessment_within_one_week_after(one_week_rule_strategy):
    assessments = [
        Assessment(date.today() + timedelta(days=6))
    ]
    assert one_week_rule_strategy.check_clash(date.today(), assessments) == False

def test_clash_with_multiple_assessments_within_one_week(one_week_rule_strategy):
    assessments = [
        Assessment(date.today() - timedelta(days=6)),
        Assessment(date.today() + timedelta(days=5))
    ]
    assert one_week_rule_strategy.check_clash(date.today(), assessments) == False

def test_no_clash_with_assessments_exactly_one_week_away(one_week_rule_strategy):
    assessments = [
        Assessment(date.today() - timedelta(days=7)),
        Assessment(date.today() + timedelta(days=7))
    ]
    assert one_week_rule_strategy.check_clash(date.today(), assessments) == True