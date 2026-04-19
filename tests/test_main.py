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
    assert data is not None
    assert "message" in data
    assert data["status"] == "healthy"


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"


def test_ready_endpoint(client):
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ready"