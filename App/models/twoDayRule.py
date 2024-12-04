from abc import ABC, abstractmethod
from .clashRuleStrategy import ClashRuleStrategy
from datetime import date

class TwoDayRule(ClashRuleStrategy):
    def check_clash(self, target_date: date, assessments: list) -> bool:
        for assessment in assessments:
            # Check both start and end dates
            days_to_start = abs((assessment.startDate - target_date).days)
            days_to_end = abs((assessment.endDate - target_date).days)
            
            if min(days_to_start, days_to_end) <= 2:
                return True
        return False