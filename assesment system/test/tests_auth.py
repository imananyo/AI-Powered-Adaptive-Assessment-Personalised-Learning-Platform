import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import Base, engine
from app.core.security import hash_password

client = TestClient(app)


# Create test database tables
@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_signup_success(test_db):
    response = client.post(
        "/auth/signup",
        json={
            "email": "teststudent@example.com",
            "password": "TestPass123!"
        }
    )
    assert response.status_code == 201
    assert response.json()["message"] == "User created successfully"


def test_signup_duplicate_email(test_db):
    # First signup
    client.post(
        "/auth/signup",
        json={"email": "duplicate@example.com", "password": "Pass123"}
    )
    # Second signup with same email
    response = client.post(
        "/auth/signup",
        json={"email": "duplicate@example.com", "password": "Pass123"}
    )
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_login_success(test_db):
    # Create user first
    client.post(
        "/auth/signup",
        json={"email": "loginuser@example.com", "password": "LoginPass123"}
    )

    response = client.post(
        "/auth/login",
        json={"email": "loginuser@example.com", "password": "LoginPass123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_invalid_credentials(test_db):
    response = client.post(
        "/auth/login",
        json={"email": "wrong@example.com", "password": "WrongPass"}
    )
    assert response.status_code == 401
    assert "Invalid credentials" in response.json()["detail"]