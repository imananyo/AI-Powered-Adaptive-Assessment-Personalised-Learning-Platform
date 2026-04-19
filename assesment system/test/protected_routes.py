from fastapi.testclient import TestClient
from app.main import app
from app.core.security import create_access_token

client = TestClient(app)


def get_auth_headers():
    token = create_access_token({"sub": "teacher@example.com"})
    return {"Authorization": f"Bearer {token}"}


def test_generate_assessment_protected():
    headers = get_auth_headers()
    payload = {
        "topic": "Python Basics",
        "difficulty": "easy",
        "num_students": 2,
        "use_async": False
    }
    response = client.post("/assessment/generate", json=payload, headers=headers)
    assert response.status_code == 200
    assert "questions" in response.json()


def test_teacher_content_protected():
    headers = get_auth_headers()
    payload = {"topic": "Deep Learning"}
    response = client.post("/teacher/content", json=payload, headers=headers)
    assert response.status_code == 200
    assert "resources" in response.json()
    assert "generated_for" in response.json()


def test_protected_route_without_token():
    payload = {"topic": "Math", "difficulty": "medium", "num_students": 3}
    response = client.post("/assessment/generate", json=payload)
    assert response.status_code == 401