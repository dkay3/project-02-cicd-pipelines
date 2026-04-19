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


def test_home_returns_html(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Great job" in response.data
    assert b"deployed" in response.data


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"


def test_ready_endpoint(client):
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ready"


def test_api_info_endpoint(client):
    response = client.get("/api/info")
    assert response.status_code == 200
    data = response.get_json()
    assert data is not None
    assert "version" in data
    assert "status" in data
    assert data["status"] == "healthy"