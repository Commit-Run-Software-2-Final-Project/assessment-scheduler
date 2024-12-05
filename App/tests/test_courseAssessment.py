import pytest
from App.models import CourseAssessment, Assessment, Course, TwoDayRule, OneWeekRuleStrategy
from App.controllers.courseAssessment import (
    add_CourseAsm,
    list_Assessments,
    get_Assessment_id,
    get_Assessment_type,
    get_CourseAsm_id,
    get_CourseAsm_code,
    delete_CourseAsm,
    get_clashes,
    check_clash,
    setClashStrategy
)
from App.models.assessment import Category
from App.database import db
from datetime import date, time

class MockAssessment:
    def __init__(self, start_date, id, endDate):
        self.startDate = start_date
        self.id = id
        self.endDate = endDate


@pytest.fixture(scope='function')
def sample_data(session):
    """Fixture to add sample data for tests."""
    # Create sample courses and assessments
    course = Course(courseCode="COMP3607", courseTitle="Object Oreintated Programming II",
                    description="Software Engineering Pro Max", level=3, semester = 1, aNum = 0)
    assessment = Assessment( category=Category.ASSIGNMENT)
    db.session.add(course)
    db.session.add(assessment)
    db.session.commit()

    # Add CourseAssessment
    course_assessment = CourseAssessment(
        courseCode="COMP3607",
        a_ID=1,
        startDate=date(2024, 12, 1),
        endDate=date(2024, 12, 2),
        startTime=time(9, 0),
        endTime=time(11, 0),
        clashDetected=False
    )
    db.session.add(course_assessment)
    db.session.commit()

    yield {
        "course": course,
        "assessment": assessment,
        "course_assessment": course_assessment
    }

    # Teardown
    db.session.remove()
    db.drop_all()


@pytest.mark.unit
def test_add_course_assessment(test_app, session):
    """Test adding a new CourseAssessment."""
    with test_app.app_context():
        new_course_assessment = add_CourseAsm(
            "COMP3607", 1, date(2024, 12, 3), date(2024, 12, 4),
            time(10, 0), time(12, 0), False
        )
        assert new_course_assessment.courseCode == "COMP3607"
        assert new_course_assessment.a_ID == 1
        assert new_course_assessment.startDate == date(2024, 12, 3)


@pytest.mark.unit
def test_list_assessments(test_app, session, sample_data):
    """Test listing all assessments."""
    with test_app.app_context():
        assessments = list_Assessments()
        assert len(assessments) == 1
        assert assessments[0].category == Category.ASSIGNMENT


@pytest.mark.unit
def test_get_assessment_id(test_app, session, sample_data):
    """Test retrieving assessment ID by category."""
    with test_app.app_context():
        assessment_id = get_Assessment_id(Category.ASSIGNMENT)
        assert assessment_id == 1


@pytest.mark.unit
def test_get_assessment_type(test_app, session, sample_data):
    """Test retrieving assessment category by ID."""
    with test_app.app_context():
        assessment_type = get_Assessment_type(1)
        assert assessment_type == "ASSIGNMENT"


@pytest.mark.unit
def test_get_course_assessment_by_id(test_app, session, sample_data):
    """Test retrieving a CourseAssessment by ID."""
    with test_app.app_context():
        course_assessment = get_CourseAsm_id(sample_data["course_assessment"].id)
        assert course_assessment is not None
        assert course_assessment.courseCode == "COMP3607"


@pytest.mark.unit
def test_get_course_assessment_by_code(test_app, session, sample_data):
    """Test retrieving CourseAssessments by course code."""
    with test_app.app_context():
        assessments = get_CourseAsm_code("COMP3607")
        assert len(assessments) == 1
        assert assessments[0].courseCode == "COMP3607"


@pytest.mark.unit
def test_delete_course_assessment(test_app, session, sample_data):
    """Test deleting a CourseAssessment."""
    with test_app.app_context():
        course_assessment = sample_data["course_assessment"]

        # Ensure the object exists in the database before deletion
        assert CourseAssessment.query.get(course_assessment.id) is not None

        # Call delete function
        result = delete_CourseAsm(course_assessment)
        assert result is True

        # Verify deletion
        deleted = CourseAssessment.query.get(course_assessment.id)
        assert deleted is None


@pytest.mark.unit
def test_get_clashes(test_app, session, sample_data):
    """Test retrieving CourseAssessments with clashes."""
    with test_app.app_context():
        # Set clashDetected to True
        sample_data["course_assessment"].clashDetected = True
        db.session.merge(sample_data["course_assessment"])
        db.session.commit()

        clashes = get_clashes()
        assert len(clashes) == 1
        assert clashes[0].clashDetected is True


@pytest.mark.unit
def test_setClashRule(test_app, session, sample_data):
    """Test setting clash strategy"""
    with test_app.app_context():
        sample_data["course_assessment"].setClashRule(TwoDayRule())
        assert sample_data["course_assessment"].clashRule == "TwoDayRule"


@pytest.mark.unit
def test_getClashRule(test_app, session, sample_data):
    """Test Getting Clash Rule"""
    with test_app.app_context():
        sample_data["course_assessment"].clashRule = "TwoDayRule"
        assert isinstance(sample_data["course_assessment"].getClashRule(), TwoDayRule)


@pytest.mark.unit
def test_setClashStrategy(test_app, session, sample_data):
    """Test setting clash strategy with controller"""
    with test_app.app_context():
        course_assessment = setClashStrategy(1, "WeekRule")
        assert course_assessment.clashRule == "OneWeekRuleStrategy"


@pytest.mark.unit
def test_check_clash(test_app, session, sample_data):
    """Test checking for clash in course assessments"""
    with test_app.app_context():
        sample_data["course_assessment"].clashRule = "TwoDayRule"
        course_assessment = sample_data["course_assessment"]
        course_assessment.clashRule = "TwoDayRule"
        db.session.merge(course_assessment)
        assessments = [
            MockAssessment(date(2024, 12, 1), 1, date(2024, 12, 1)),
            MockAssessment(date(2024, 12, 5), 2, date(2024, 12, 5)),
            MockAssessment(date(2024, 12, 8), 3, date(2024, 12, 8)),
        ]
        assert check_clash(assessments, 1) == False
        
        assessments = [
            MockAssessment(date(2024, 12, 4), 1 , date(2024, 12, 4)),
            MockAssessment(date(2024, 12, 5), 2, date(2024, 12, 5)),
            MockAssessment(date(2024, 12, 8), 3, date(2024, 12, 8)),
        ]
        assert check_clash(assessments, 1) == False



'''
Integration tests
'''
@pytest.fixture(scope='function')
def setup_data(test_app):
    """Fixture to set up data for integration tests."""
    with test_app.app_context():
        # Create courses and assessments
        course = Course(courseCode="COMP3607", courseTitle="Object Oreintated Programming II",
                        description="Software Engineering Pro Max", level=3, semester = 1, aNum = 0)
        assessment1 = Assessment(category=Category.EXAM)
        assessment2 = Assessment(category=Category.QUIZ)

        db.session.add(course)
        db.session.add(assessment1)
        db.session.add(assessment2)
        db.session.commit()

        yield {
            "course": course,
            "assessment1": assessment1,
            "assessment2": assessment2
        }

        # Teardown
        db.session.remove()
        db.drop_all()


@pytest.mark.integration
def test_full_course_assessment_lifecycle(test_app, setup_data):
    """Test the full lifecycle of a CourseAssessment."""
    with test_app.app_context():
        # Add a CourseAssessment
        new_assessment = add_CourseAsm(
            "COMP3610", 1, date(2024, 12, 5), date(2024, 12, 6),
            time(14, 0), time(16, 0), False
        )

        # Verify addition
        saved_assessment = CourseAssessment.query.get(new_assessment.id)
        assert saved_assessment is not None
        assert saved_assessment.courseCode == "COMP3610"

        # Simulate a clash and verify retrieval
        saved_assessment.clashDetected = True
        db.session.commit()

        clashes = get_clashes()
        assert len(clashes) == 1
        assert clashes[0].id == saved_assessment.id

        # Delete the assessment and verify deletion
        db.session.delete(saved_assessment)
        db.session.commit()

        deleted_assessment = CourseAssessment.query.get(new_assessment.id)
        assert deleted_assessment is None
