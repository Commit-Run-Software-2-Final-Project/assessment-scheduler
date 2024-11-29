from abc import ABC, abstractmethod
from .clashRuleStrategy import ClashRuleStrategy
from datetime import date

class TwoDayRule(ClashRuleStrategy):
    def check_clash(self, date: date, assessments: list) -> bool:
        for assessment in assessments:
            if abs((assessment.startDate - date).days) <= 2:
                return True
        return False