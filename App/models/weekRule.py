from .clashRuleStrategy import ClashRuleStrategy
from datetime import date

class OneWeekRuleStrategy(ClashRuleStrategy):
    def check_clash(self, date: date, assessments: list) -> bool:
        for assessment in assessments:
            if abs((assessment.startDate - date).days) < 7:
                return True
        return False