from fastapi.testclient import TestClient
from pytest_httpserver import HTTPServer

from apprise_api_headless.main import app


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


def test_notify_with_empty_body(httpserver: HTTPServer):
    with TestClient(app) as client:
        response = client.post("/notify/test", json={"body": ""})
        assert response.status_code == 422
        assert (
            response.json()["detail"][0]["msg"]
            == "String should have at least 1 character"
        )

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
