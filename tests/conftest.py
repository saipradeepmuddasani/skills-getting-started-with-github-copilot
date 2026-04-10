import pytest
from copy import deepcopy
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def clean_activities():
    """Provide a fresh copy of activities for each test"""
    return deepcopy(activities)


@pytest.fixture
def client(clean_activities, monkeypatch):
    """Create a test client with isolated activities state"""
    # Replace the app's activities with clean copy
    monkeypatch.setattr("src.app.activities", clean_activities)
    return TestClient(app)
