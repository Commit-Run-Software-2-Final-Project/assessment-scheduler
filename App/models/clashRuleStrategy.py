from App import db
from abc import ABC, abstractmethod
from datetime import date

class ClashRuleStrategy(ABC):
    @abstractmethod

    def check_clash(self, date: date, assignments: list) -> bool:
        pass
   

       

