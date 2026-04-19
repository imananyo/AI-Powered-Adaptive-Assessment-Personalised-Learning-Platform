import pytest
from unittest.mock import patch
from app.workers.celery_work import async_generate_questions
from app.services.question_generator import question_generator


@pytest.fixture
def mock_question_generator():
    with patch.object(question_generator, 'generate_for_students') as mock:
        mock.return_value = [
            {
                "student_id": "student_1",
                "seed": 42,
                "question": {"main_question": "Mock question 1"}
            }
        ]
        yield mock


def test_async_generate_questions_task(mock_question_generator):
    """Test that the Celery task calls the question generator correctly"""
    result = async_generate_questions.delay("Python", "medium", 3)
    
    # Get the actual task result
    task_result = result.get(timeout=10)
    
    assert isinstance(task_result, list)
    assert len(task_result) == 3
    assert task_result[0]["student_id"] == "student_1"
    mock_question_generator.assert_called_once_with(
        topic="Python",
        difficulty="medium",
        num_students=3
    )


def test_celery_task_signature():
    """Test task can be called without executing"""
    task = async_generate_questions.signature(
        args=("Data Science", "hard", 5),
        countdown=5
    )
    assert task is not None
    assert task.args == ("Data Science", "hard", 5)


@pytest.mark.asyncio
async def test_celery_task_async_execution(mock_question_generator):
    """Test async task execution using Celery"""
    result = async_generate_questions.delay("Math", "easy", 2)
    task_result = result.get(timeout=15)
    
    assert len(task_result) == 2
    assert "student_" in task_result[0]["student_id"]