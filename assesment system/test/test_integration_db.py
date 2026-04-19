import pytest
from app.models.user import User
from app.models.models import Assessment, Submission
from app.core.security import hash_password


def test_user_creation_in_db(db_session):
    user = User(
        email="integration_test@example.com",
        password=hash_password("TestPass123")
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    fetched_user = db_session.query(User).filter(User.email == "integration_test@example.com").first()
    assert fetched_user is not None
    assert fetched_user.email == "integration_test@example.com"


def test_assessment_save_in_db(db_session):
    assessment = Assessment(
        topic="Machine Learning",
        difficulty="medium",
        questions=[
            {"student_id": "student_1", "question": {"main_question": "What is overfitting?"}},
            {"student_id": "student_2", "question": {"main_question": "Explain bias-variance tradeoff"}}
        ]
    )
    db_session.add(assessment)
    db_session.commit()
    db_session.refresh(assessment)

    saved = db_session.query(Assessment).filter(Assessment.topic == "Machine Learning").first()
    assert saved is not None
    assert len(saved.questions) == 2


def test_submission_save_in_db(db_session):
    submission = Submission(
        student_id="student_101",
        answer="The answer is 42",
        evaluation={
            "score": 90,
            "depth_score": 85,
            "mistakes": [],
            "feedback": "Excellent work!"
        }
    )
    db_session.add(submission)
    db_session.commit()

    saved = db_session.query(Submission).filter(Submission.student_id == "student_101").first()
    assert saved is not None
    assert saved.evaluation["score"] == 90