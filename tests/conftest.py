from pathlib import Path
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from pytest_httpserver import HTTPServer

from apprise_api_headless.main import app


def default_config(host: str, port: int) -> str:
    return (
        f"urls:\n"
        f"- 'json://{host}:{port}/tag':\n"
        f"  - tag: tag\n"
        f"- 'json://{host}:{port}/no-tag'\n"
    )


def failing_config(host: str, port: int) -> str:
    return default_config(host, port) + (
        f"- 'json://{host}:{port}/fail':\n"
        f"  - tag: fail\n"
    )  # fmt: skip


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
    Tests can override by writing different files into the config dir.
    """
    httpserver.expect_request("/tag").respond_with_json({"result": "ok"})
    httpserver.expect_request("/no-tag").respond_with_json({"result": "ok"})

    config_dir = Path(client.app.state.settings.apprise_config_dir)
    config_dir.mkdir(parents=True, exist_ok=True)
    with open(config_dir / "test.yml", "w") as file:
        file.write(default_config(httpserver.host, httpserver.port))
    with open(config_dir / "test-fail.yml", "w") as file:
        file.write(failing_config(httpserver.host, httpserver.port))
