import pytest
from fastapi.testclient import TestClient
from src.user_service.main import app
from src.user_service.database import users_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_database():
    """Clear database before each test"""
    users_db.clear()
    yield
    users_db.clear()

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["service"] == "User Service"

def test_create_user_success():
    """Test successful user creation"""
    user_data = {
        "username": "johndoe",
        "email": "john@example.com",
        "full_name": "John Doe"
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "johndoe"
    assert data["email"] == "john@example.com"
    assert "user_id" in data
    assert data["is_active"] is True

def test_create_user_invalid_email():
    """Test user creation with invalid email"""
    user_data = {
        "username": "johndoe",
        "email": "invalid-email",
        "full_name": "John Doe"
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 422

def test_get_user_success():
    """Test getting user by ID"""
    user_data = {
        "username": "janedoe",
        "email": "jane@example.com",
        "full_name": "Jane Doe"
    }
    create_response = client.post("/users", json=user_data)
    user_id = create_response.json()["user_id"]
    
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["username"] == "janedoe"

def test_get_user_not_found():
    """Test getting non-existent user"""
    response = client.get("/users/nonexistent-id")
    assert response.status_code == 404

def test_list_users():
    """Test listing all users"""
    users = [
        {"username": "user1", "email": "user1@example.com", "full_name": "User One"},
        {"username": "user2", "email": "user2@example.com", "full_name": "User Two"}
    ]
    for user in users:
        client.post("/users", json=user)
    
    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_validate_user_success():
    """Test user validation endpoint"""
    user_data = {
        "username": "validuser",
        "email": "valid@example.com",
        "full_name": "Valid User"
    }
    create_response = client.post("/users", json=user_data)
    user_id = create_response.json()["user_id"]
    
    response = client.get(f"/users/{user_id}/validate")
    assert response.status_code == 200
    data = response.json()
    assert data["is_valid"] is True
    assert "user_details" in data

def test_validate_user_not_found():
    """Test validation of non-existent user"""
    response = client.get("/users/invalid-id/validate")
    assert response.status_code == 200
    data = response.json()
    assert data["is_valid"] is False

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
