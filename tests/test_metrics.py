from fastapi.testclient import TestClient


def test_metrics(client: TestClient):
    response = client.get("/metrics")
    assert response.status_code == 200

    content_type = response.headers.get("content-type", "").lower()
    assert "text/plain" in content_type

    text = response.text or ""
    assert "# HELP" in text or "# TYPE" in text or "process_cpu_seconds" in text
