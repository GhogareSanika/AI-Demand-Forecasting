from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_home_endpoint() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "message" in response.json()


def test_health_endpoint() -> None:
    with TestClient(app) as test_client:
        response = test_client.get("/health")

        assert response.status_code == 200
        assert "status" in response.json()
        assert "model_loaded" in response.json()


def test_model_info_endpoint() -> None:
    with TestClient(app) as test_client:
        response = test_client.get("/model-info")

        assert response.status_code == 200

        data = response.json()

        assert data["number_of_features"] > 0
        assert len(data["features"]) > 0