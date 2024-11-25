# from abc import ABC, abstractmethod
# from datetime import datetime

# class ClashRule(ABC):
#     @abstractmethod
#     def is_clashing(self, assignment1, assignment2):
#         pass

# class TimeClashRule(ClashRule):
#     def is_clashing(self, assignment1, assignment2):
#         return assignment1.due_date == assignment2.due_date
        
# class Assignment:
#     def __init__(self, name, due_date):
#         self.name = name
#         self.due_date = due_date

# class AssignmentScheduler:
#     def __init__(self, clash_rule: ClashRule):
#         self.clash_rule = clash_rule
#         self.assignments = []

#     def add_assignment(self, assignment: Assignment):
#         for existing_assignment in self.assignments:
#             if self.clash_rule.is_clashing(existing_assignment, assignment):
#                 raise ValueError(f"Assignment {assignment.name} clashes with {existing_assignment.name}")
#         self.assignments.append(assignment)

#     def get_assignments(self):
#         return self.assignments

# if __name__ == "__main__":
#     scheduler = AssignmentScheduler(TimeClashRule())
#     assignment1 = Assignment("Math Homework", datetime(2023, 10, 15))
#     assignment2 = Assignment("Science Project", datetime(2023, 10, 15))
    
#     scheduler.add_assignment(assignment1)
#     try:
#         scheduler.add_assignment(assignment2)
#     except ValueError as e:
#         print(e)