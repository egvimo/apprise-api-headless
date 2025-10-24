from http.server import HTTPServer
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from apprise_api_headless.main import app


@pytest.fixture(autouse=True)
def apprise_config(httpserver: HTTPServer):
    httpserver.expect_request("/").respond_with_json({"result": "ok"})
    with TestClient(app) as client:
        config_dir = Path(client.app.state.settings.apprise_config_dir)
        config_dir.mkdir(parents=True, exist_ok=True)
        with open(config_dir / "test-apprise.yml", "w") as file:
            file.write(
                f"urls:\n- 'json://{httpserver.host}:{httpserver.port}/':\n  - tag: tag"
            )


def test_notify_success():
    with TestClient(app) as client:
        response = client.post("/notify/test-apprise", json={"body": "body"})
        assert response.status_code == 200
        assert response.json()["success"] is True


def test_notify_missing_config():
    with TestClient(app) as client:
        response = client.post("/notify/nonexistent", json={"body": "body"})
        assert response.status_code == 404


def test_notify_with_title():
    with TestClient(app) as client:
        response = client.post(
            "/notify/test-apprise", json={"title": "title", "body": "body"}
        )
        assert response.status_code == 200
        assert response.json()["success"] is True


def test_notify_with_tag():
    with TestClient(app) as client:
        response = client.post(
            "/notify/test-apprise", json={"body": "body", "tag": "tag"}
        )
        assert response.status_code == 200
        assert response.json()["success"] is True


def test_notify_with_missing_tag():
    with TestClient(app) as client:
        response = client.post(
            "/notify/test-apprise", json={"body": "body", "tag": "missing"}
        )
        assert response.status_code == 424


def test_notify_with_title_and_tag():
    with TestClient(app) as client:
        response = client.post(
            "/notify/test-apprise",
            json={"title": "title", "body": "body", "tag": "tag"},
        )
        assert response.status_code == 200
        assert response.json()["success"] is True


def test_notify_extra_fields():
    with TestClient(app) as client:
        response = client.post(
            "/notify/test-apprise", json={"body": "body", "extra": "field"}
        )
        assert response.status_code == 200
