import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from app.main import app as flask_app

@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client

def test_home_returns_200(client):
    response = client.get("/")
    assert response.status_code == 200

def test_home_returns_json(client):
    response = client.get("/")
    data = response.get_json()
    assert "message" in data
    assert "status" in data
    assert data["status"] == "healthy"

def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"

def test_ready_endpoint(client):
    response = client.get("/ready")
    assert response.status_code == 200