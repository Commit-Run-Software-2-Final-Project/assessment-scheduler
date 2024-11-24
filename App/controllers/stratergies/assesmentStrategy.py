from abc import ABC, abstractmethod
from App.models import CourseAssessment

class AssessmentStrategy(ABC):
    """
    Interface for assessment validation strategies.
    Defines the contract that concrete strategies must follow.
    """
    
    @abstractmethod
    def validate_assessment(self, course_assessment: CourseAssessment) -> bool:
        """
        Validates a course assessment based on rules specified.
        
        Args:
            course_assessment (CourseAssessment): The assessment to validate
            
        Returns:
            bool: True if assessment is valid, False otherwise
        """
        pass
    
    @abstractmethod
    def check_conflicts(self, course_assessment: CourseAssessment) -> bool:
        """
        Checks for scheduling conflicts with other assessments.
        
        Args:
            course_assessment (CourseAssessment): The assessment to check for conflicts
            
        Returns:
            bool: True if there are conflicts, False otherwise
        """
        pass