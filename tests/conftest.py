import textwrap
from pathlib import Path
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from pytest_httpserver import HTTPServer

from apprise_api_headless.main import app


def default_config(host: str, port: int) -> str:
    return textwrap.dedent(f"""\
        urls:
        - 'json://{host}:{port}/tag':
          - tag: tag
        - 'json://{host}:{port}/no-tag'
    """)


def failing_config(host: str, port: int) -> str:
    return textwrap.dedent(f"""\
        urls:
        - 'json://{host}:{port}/tag':
          - tag: tag
        - 'json://{host}:{port}/no-tag'
        - 'json://{host}:{port}/fail':
          - tag: fail
    """)


def tags_config(host: str, port: int) -> str:
    return textwrap.dedent(f"""\
        urls:
        - 'json://{host}:{port}/a':
          - tag: a
        - 'json://{host}:{port}/b':
          - tag: b
        - 'json://{host}:{port}/a-c':
          - tag: [a, c]
        - 'json://{host}:{port}/b-c':
          - tag: [b, c]
    """)


@pytest.fixture(scope="session")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client


@pytest.fixture(autouse=True)
def apprise_config(client: TestClient, httpserver: HTTPServer) -> None:
    """
    Default autouse fixture that prepares two configs:
      - `test.yml` -> success endpoints
      - `test-fail.yml` -> includes a failing endpoint
      - `test-tags.yml` -> includes tag-based endpoints
    Tests can override by writing different files into the config dir.
    """
    httpserver.expect_request("/tag").respond_with_json({"result": "ok"})
    httpserver.expect_request("/no-tag").respond_with_json({"result": "ok"})
    httpserver.expect_request("/fail").respond_with_data("error", status=500)
    httpserver.expect_request("/a").respond_with_json({"result": "ok"})
    httpserver.expect_request("/b").respond_with_json({"result": "ok"})
    httpserver.expect_request("/a-c").respond_with_json({"result": "ok"})
    httpserver.expect_request("/b-c").respond_with_json({"result": "ok"})

    config_dir = Path(client.app.state.settings.apprise_config_dir)
    config_dir.mkdir(parents=True, exist_ok=True)
    with open(config_dir / "test.yml", "w") as file:
        file.write(default_config(httpserver.host, httpserver.port))
    with open(config_dir / "test-fail.yml", "w") as file:
        file.write(failing_config(httpserver.host, httpserver.port))
    with open(config_dir / "test-tags.yml", "w") as file:
        file.write(tags_config(httpserver.host, httpserver.port))


def request_paths(httpserver: HTTPServer) -> set[str]:
    """Return all request paths received by the mock server."""
    return {req.path for req, _ in httpserver.log}
