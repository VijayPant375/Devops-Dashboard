"""
Test suite for DevOps Dashboard Flask Application
"""
import pytest
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_returns_200(client):
    """Test that the main page loads successfully."""
    response = client.get("/")
    assert response.status_code == 200


def test_index_contains_app_name(client):
    """Test that the index page contains the app name."""
    response = client.get("/")
    assert b"DevOps Dashboard" in response.data


def test_health_endpoint(client):
    """Test the /health endpoint returns healthy status."""
    response = client.get("/health")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "healthy"
    assert "version" in data
    assert "timestamp" in data


def test_api_info_endpoint(client):
    """Test the /api/info endpoint returns system info."""
    response = client.get("/api/info")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "hostname" in data
    assert "python_version" in data
    assert "version" in data


def test_404_not_found(client):
    """Test that unknown routes return 404."""
    response = client.get("/nonexistent-route")
    assert response.status_code == 404
