import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def test_student_data():
    return {
        "first_name" : "Test",
        "last_name" : "User",
        "email" : "testuser@example.com",
        "age" : 20
    }