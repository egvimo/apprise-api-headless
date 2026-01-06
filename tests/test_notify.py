from fastapi.testclient import TestClient
from pytest_httpserver import HTTPServer


def test_notify_success(client: TestClient, httpserver: HTTPServer):
    response = client.post("/notify/test", json={"body": "body"})
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert len(httpserver.log) == 1


def test_notify_missing_config(client: TestClient, httpserver: HTTPServer):
    response = client.post("/notify/nonexistent", json={"body": "body"})
    assert response.status_code == 404
    assert len(httpserver.log) == 0


def test_notify_with_title(client: TestClient, httpserver: HTTPServer):
    response = client.post("/notify/test", json={"title": "title", "body": "body"})
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert len(httpserver.log) == 1


def test_notify_with_tag(client: TestClient, httpserver: HTTPServer):
    response = client.post("/notify/test", json={"body": "body", "tag": "tag"})
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert len(httpserver.log) == 1


def test_notify_with_all_tag(client: TestClient, httpserver: HTTPServer):
    response = client.post("/notify/test", json={"body": "body", "tag": "all"})
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert len(httpserver.log) == 2


def test_notify_with_missing_tag(client: TestClient, httpserver: HTTPServer):
    response = client.post("/notify/test", json={"body": "body", "tag": "missing"})
    assert response.status_code == 424
    assert len(httpserver.log) == 0


def test_notify_with_empty_body(client: TestClient, httpserver: HTTPServer):
    response = client.post("/notify/test", json={"body": ""})
    assert response.status_code == 422
    assert (
        response.json()["detail"][0]["msg"] == "String should have at least 1 character"
    )
    assert len(httpserver.log) == 0


def test_notify_with_title_and_tag(client: TestClient, httpserver: HTTPServer):
    response = client.post(
        "/notify/test",
        json={"title": "title", "body": "body", "tag": "tag"},
    )
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert len(httpserver.log) == 1


def test_notify_with_extra_fields(client: TestClient, httpserver: HTTPServer):
    response = client.post("/notify/test", json={"body": "body", "extra": "field"})
    assert response.status_code == 200
    assert len(httpserver.log) == 1


def test_notify_with_failing_url(client: TestClient, httpserver: HTTPServer):
    response = client.post("/notify/test-fail", json={"body": "body"})
    assert response.status_code == 200
    assert len(httpserver.log) == 1


def test_notify_with_all_tag_and_failing_url(
    client: TestClient, httpserver: HTTPServer
):
    response = client.post("/notify/test-fail", json={"body": "body", "tag": "all"})
    assert response.status_code == 424
    assert len(httpserver.log) == 3


def test_notify_with_failing_url_and_tag(client: TestClient, httpserver: HTTPServer):
    response = client.post("/notify/test-fail", json={"body": "body", "tag": "fail"})
    assert response.status_code == 424
    assert len(httpserver.log) == 1
