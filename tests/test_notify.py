import pytest
from fastapi.testclient import TestClient
from pytest_httpserver import HTTPServer

from tests.conftest import request_paths


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


@pytest.mark.parametrize(
    "expression,expected_paths,status",
    [
        ("a", {"/a", "/a-c"}, 200),
        ("b", {"/b", "/b-c"}, 200),
        ("c", {"/a-c", "/b-c"}, 200),
        ("a c", {"/a-c"}, 200),  # AND
        ("b c", {"/b-c"}, 200),  # AND
        ("a, b", {"/a", "/b", "/a-c", "/b-c"}, 200),  # OR
        ("a c, b", {"/a-c", "/b", "/b-c"}, 200),  # (A AND C) OR B
        ("a b", set(), 424),  # impossible AND
    ],
)
def test_tag_expression(
    client: TestClient,
    httpserver: HTTPServer,
    expression: str,
    expected_paths: set[str],
    status: int,
):
    response = client.post(
        "/notify/test-tags",
        json={"body": "body", "tag": expression},
    )

    assert response.status_code == status
    assert request_paths(httpserver) == expected_paths
