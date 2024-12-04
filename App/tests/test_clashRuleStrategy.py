import pytest
from datetime import date
from App.models.clashRuleStrategy import ClashRuleStrategy

class MockClashRuleStrategy(ClashRuleStrategy):
    def check_clash(self, date: date, assessments: list) -> bool:
        return any(assessment['date'] == date for assessment in assessments)

@pytest.fixture
def mock_clash_rule_strategy():
    return MockClashRuleStrategy()

def test_check_clash_no_clash(mock_clash_rule_strategy):
    assessments = [{'date': date(2023, 10, 1)}, {'date': date(2023, 10, 2)}]
    assert not mock_clash_rule_strategy.check_clash(date(2023, 10, 3), assessments)

def test_check_clash_with_clash(mock_clash_rule_strategy):
    assessments = [{'date': date(2023, 10, 1)}, {'date': date(2023, 10, 2)}]
    assert mock_clash_rule_strategy.check_clash(date(2023, 10, 1), assessments)

def test_check_clash_empty_assessments(mock_clash_rule_strategy):
    assessments = []
    assert not mock_clash_rule_strategy.check_clash(date(2023, 10, 1), assessments)

def test_check_clash_multiple_clashes(mock_clash_rule_strategy):
    assessments = [{'date': date(2023, 10, 1)}, {'date': date(2023, 10, 1)}]
    assert mock_clash_rule_strategy.check_clash(date(2023, 10, 1), assessments)