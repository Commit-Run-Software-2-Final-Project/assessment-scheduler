from abc import ABC, abstractmethod
from datetime import date

class ClashRuleStrategy(ABC):
    @abstractmethod
    def check_clash(self, date: date, assessments: list) -> bool:
        pass
   

       

