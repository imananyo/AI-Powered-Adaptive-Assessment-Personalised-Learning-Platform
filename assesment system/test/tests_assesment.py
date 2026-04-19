import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_generate_assessment_sync():
    payload = {
        "topic": "Python Programming",
        "difficulty": "medium",
        "num_students": 3,
        "base_seed": 42,
        "use_async": False
    }
    response = client.post("/assessment/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["topic"] == "Python Programming"
    assert data["difficulty"] == "medium"
    assert len(data["questions"]) == 3


def test_generate_assessment_async():
    payload = {
        "topic": "Data Structures",
        "difficulty": "easy",
        "num_students": 5,
        "use_async": True
    }
    response = client.post("/assessment/generate", json=payload)
    assert response.status_code == 200
    assert "task_id" in response.json()
    assert "queued" in response.json()["message"].lower()


def test_assessment_invalid_difficulty():
    payload = {
        "topic": "Math",
        "difficulty": "very_hard",  # Invalid
        "num_students": 2
    }
    response = client.post("/assessment/generate", json=payload)
    assert response.status_code == 422  # Validation error


def test_assessment_max_students_limit():
    payload = {
        "topic": "Physics",
        "difficulty": "hard",
        "num_students": 150  # Exceeds limit
    }
    response = client.post("/assessment/generate", json=payload)
    assert response.status_code == 422