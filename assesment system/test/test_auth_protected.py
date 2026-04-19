import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.security import create_access_token

client = TestClient(app)


# Example Protected Route (for testing purposes)
# We'll add this temporarily in tests or you can add it in main.py
def add_protected_route_for_testing():
    from fastapi import Depends, HTTPException
    from app.core.security import verify_token

    @app.get("/protected/me")
    def get_current_user(token: str = Depends(verify_token)):
        if not token:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        return {"user": token.get("sub"), "message": "You are authenticated!"}


# Call this once to register the protected route for tests
add_protected_route_for_testing()


@pytest.fixture
def auth_headers():
    """Create valid JWT token for authenticated requests"""
    token = create_access_token({"sub": "testuser@example.com"})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def invalid_auth_headers():
    return {"Authorization": "Bearer invalid.token.here"}


def test_protected_route_success(auth_headers):
    """Test accessing protected route with valid token"""
    response = client.get("/protected/me", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["user"] == "testuser@example.com"
    assert "authenticated" in response.json()["message"].lower()


def test_protected_route_no_token():
    """Test protected route without token"""
    response = client.get("/protected/me")
    assert response.status_code == 401


def test_protected_route_invalid_token(invalid_auth_headers):
    """Test protected route with invalid token"""
    response = client.get("/protected/me", headers=invalid_auth_headers)
    assert response.status_code == 401


def test_login_and_access_protected_route():
    """Full flow: Signup → Login → Access protected route"""
    # Signup
    client.post(
        "/auth/signup",
        json={"email": "protecteduser@example.com", "password": "SecurePass123"}
    )

    # Login
    login_response = client.post(
        "/auth/login",
        json={"email": "protecteduser@example.com", "password": "SecurePass123"}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Access protected route
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/protected/me", headers=headers)
    
    assert response.status_code == 200
    assert response.json()["user"] == "protecteduser@example.com"