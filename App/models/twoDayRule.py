from abc import ABC, abstractmethod
from .clashRuleStrategy import ClashRuleStrategy
from datetime import date

class TwoDayRule(ClashRuleStrategy):
    def check_clash(self, target_date: date, assessments: list) -> bool:
        for assessment in assessments:
            # Check if endDate exists; if not, use startDate
            end_date = getattr(assessment, "endDate", assessment.startDate)
            
            days_to_start = abs((assessment.startDate - target_date).days)
            days_to_end = abs((end_date - target_date).days)
            
            if min(days_to_start, days_to_end) <= 2:
                return True
        return False
