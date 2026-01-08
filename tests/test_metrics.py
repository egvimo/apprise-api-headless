import pytest
from fastapi.testclient import TestClient

from tests.payloads import BASE_ALERTMANAGER_PAYLOAD


def get_metric_value(text: str, name: str) -> float:
    """Extract metric value from Prometheus text format."""
    for line in text.splitlines():
        if line.startswith(name):
            # Extract the number at the end of the line
            parts = line.split()
            if len(parts) >= 2:
                try:
                    return float(parts[-1])
                except ValueError:
                    pass
    return 0.0


def test_metrics(client: TestClient):
    response = client.get("/metrics")
    assert response.status_code == 200

    content_type = response.headers.get("content-type", "").lower()
    assert content_type.startswith("text/plain")

    text = response.text
    assert text, "Metrics response should not be empty"

    metric_lines = [
        line for line in text.splitlines() if line and not line.startswith("#")
    ]
    assert metric_lines, "Should contain at least one metric"


@pytest.mark.parametrize(
    "path, payload",
    [
        ("/notify/nonexistent", {"body": "body"}),
        ("/webhook/alertmanager?config_key=nonexistent", BASE_ALERTMANAGER_PAYLOAD),
    ],
)
def test_notify_error_metric_increments(client: TestClient, path: str, payload: dict):
    metric_name = "apprise_notify_errors_total"

    before = get_metric_value(client.get("/metrics").text, metric_name)

    resp = client.post(path, json=payload)
    assert resp.status_code == 404

    after = get_metric_value(client.get("/metrics").text, metric_name)
    assert after == before + 1, (
        f"Expected {metric_name} to increment by 1 (was {before}, now {after})"
    )
