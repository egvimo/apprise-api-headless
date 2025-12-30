from fastapi.testclient import TestClient

from apprise_api_headless.main import app


def test_status(client: TestClient):
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json()["status"] == "OK"
