from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from pytest_httpserver import HTTPServer

from apprise_api_headless.main import app


def config(host: str, port: int) -> str:
    return (
        f"urls:\n"
        f"- 'json://{host}:{port}/tag':\n"
        f"  - tag: tag\n"
        f"- 'json://{host}:{port}/no-tag'\n"
    )


def failing_config(host: str, port: int) -> str:
    return config(host, port) + (
        f"- 'json://{host}:{port}/fail':\n"
        f"  - tag: fail\n"
    )  # fmt: skip


@pytest.fixture(autouse=True)
def apprise_config(httpserver: HTTPServer):
    httpserver.expect_request("/tag").respond_with_json({"result": "ok"})
    httpserver.expect_request("/no-tag").respond_with_json({"result": "ok"})

    with TestClient(app) as client:
        config_dir = Path(client.app.state.settings.apprise_config_dir)
        config_dir.mkdir(parents=True, exist_ok=True)
        with open(config_dir / "test.yml", "w") as file:
            file.write(config(httpserver.host, httpserver.port))
        with open(config_dir / "test-fail.yml", "w") as file:
            file.write(failing_config(httpserver.host, httpserver.port))


def test_notify_success(httpserver: HTTPServer):
    with TestClient(app) as client:
        response = client.post("/notify/test", json={"body": "body"})
        assert response.status_code == 200
        assert response.json()["success"] is True

    assert len(httpserver.log) == 2


def test_notify_missing_config(httpserver: HTTPServer):
    with TestClient(app) as client:
        response = client.post("/notify/nonexistent", json={"body": "body"})
        assert response.status_code == 404

    assert len(httpserver.log) == 0


def test_notify_with_title(httpserver: HTTPServer):
    with TestClient(app) as client:
        response = client.post("/notify/test", json={"title": "title", "body": "body"})
        assert response.status_code == 200
        assert response.json()["success"] is True

    assert len(httpserver.log) == 2


def test_notify_with_tag(httpserver: HTTPServer):
    with TestClient(app) as client:
        response = client.post("/notify/test", json={"body": "body", "tag": "tag"})
        assert response.status_code == 200
        assert response.json()["success"] is True

    assert len(httpserver.log) == 1


def test_notify_with_missing_tag(httpserver: HTTPServer):
    with TestClient(app) as client:
        response = client.post("/notify/test", json={"body": "body", "tag": "missing"})
        assert response.status_code == 424

    assert len(httpserver.log) == 0


def test_notify_with_title_and_tag(httpserver: HTTPServer):
    with TestClient(app) as client:
        response = client.post(
            "/notify/test",
            json={"title": "title", "body": "body", "tag": "tag"},
        )
        assert response.status_code == 200
        assert response.json()["success"] is True

    assert len(httpserver.log) == 1


def test_notify_with_extra_fields(httpserver: HTTPServer):
    with TestClient(app) as client:
        response = client.post("/notify/test", json={"body": "body", "extra": "field"})
        assert response.status_code == 200

    assert len(httpserver.log) == 2


def test_notify_with_failing_url(httpserver: HTTPServer):
    with TestClient(app) as client:
        response = client.post("/notify/test-fail", json={"body": "body"})
        assert response.status_code == 424

    assert len(httpserver.log) == 3


def test_notify_with_failing_url_and_tag(httpserver: HTTPServer):
    with TestClient(app) as client:
        response = client.post(
            "/notify/test-fail", json={"body": "body", "tag": "fail"}
        )
        assert response.status_code == 424

    assert len(httpserver.log) == 1
