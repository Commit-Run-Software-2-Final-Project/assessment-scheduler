from .clashRuleStrategy import ClashRuleStrategy
from datetime import date, timedelta

class OneWeekRuleStrategy(ClashRuleStrategy):
    def check_clash(self, target_date: date, assessments: list) -> bool:
        target_week_start = target_date - timedelta(days=target_date.weekday())
        target_week_end = target_week_start + timedelta(days=6)
        
        for assessment in assessments:
            assessment_date = assessment.startDate
            # Check if assessment falls within the same week
            if target_week_start <= assessment_date <= target_week_end:
                return True
        return False