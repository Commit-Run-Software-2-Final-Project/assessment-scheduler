from models.clashRuleStrategy import ClashRuleStrategy
from datetime import date

class OneWeekRuleStrategy(ClashRuleStrategy):
    def is_valid_schedule(self, assessment_date: date, other_assessments: list) -> bool:
        for scheduled_date in other_assessments:
            if abs((assessment_date - scheduled_date).days) < 7:
                return False
        return True