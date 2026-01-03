import pytest
from fastapi.testclient import TestClient
from app.main import app

# Use the real database and dependency injection from the app
client = TestClient(app)

def test_read_main():
    """Test that the API is accessible"""
    response = client.get("/docs")
    assert response.status_code == 200

def test_create_user():
    """Test creating a user"""
    response = client.post(
        "/users/",
        json={"username": "testuser", "email": "test@example.com", "full_name": "Test User"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_get_users():
    """Test getting all users"""
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_create_project():
    """Test creating a project"""
    # First create a user
    user_response = client.post(
        "/users/",
        json={"username": "projectowner", "email": "owner@example.com"}
    )
    user_id = user_response.json()["id"]
    
    # Then create a project
    response = client.post(
        "/projects/",
        json={
            "name": "Test Project",
            "description": "A test project",
            "owner_id": user_id
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Project"
    assert data["owner_id"] == user_id

def test_get_projects():
    """Test getting all projects"""
    response = client.get("/projects/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)