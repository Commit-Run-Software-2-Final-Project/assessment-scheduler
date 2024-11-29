from abc import ABC, abstractmethod
from models.clashRuleStrategy import ClashRuleStrategy
from datetime import date

class TwoDayRule(ClashRuleStrategy):
    def check_clash(self, date: date, assignments: list) -> bool:
        for assignment in assignments:
            if abs((assignment - date).days) <= 2:
                return True
        return False