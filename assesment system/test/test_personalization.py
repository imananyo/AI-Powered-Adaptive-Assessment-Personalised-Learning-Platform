import pytest
from fastapi.testclient import TestClient

# Sample data for testing
sample_question = {
    "main_question": "What is the time complexity of QuickSort?",
    "logic_check": "O(n log n) average case",
    "conceptual_why": "Explain partitioning and recursion"
}

sample_answer = "QuickSort has average time complexity of O(n log n) because it divides the array recursively."

sample_evaluation = {
    "score": 85,
    "depth_score": 70,
    "mistakes": ["minor conceptual gap in worst case"],
    "feedback": "Good understanding of average case, but mention worst case O(n^2)."
}


def test_personalization_recommendation(test_client):
    payload = {
        "question": sample_question,
        "student_answer": sample_answer,
        "evaluation": sample_evaluation
    }

    response = test_client.post("/personalization/recommend", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    
    assert "weak_analysis" in data
    assert "recommended_resources" in data
    assert "weak_concepts" in data["weak_analysis"]
    assert "videos" in data["recommended_resources"]
    assert "articles" in data["recommended_resources"]


def test_personalization_invalid_payload(test_client):
    payload = {
        "question": {"main_question": "Sample"},
        # Missing student_answer and evaluation
    }
    response = test_client.post("/personalization/recommend", json=payload)
    assert response.status_code == 422  # Pydantic validation error