from typing import Optional

from apprise_api_headless.models import AlertmanagerRequest


def format_alert_for_notification(payload: AlertmanagerRequest) -> tuple[Optional[str], str]:
    """
    Convert Alertmanager payload to title and body for notification.

    Returns:
        Tuple of (title, body)
    """
    alerts = payload.alerts
    status = payload.status

    if not alerts:
        return None, f"AlertManager: {status}"

    # Use the first alert as the main alert
    alert = alerts[0]
    alert_name = alert.labels.get("alertname", "Alert")
    severity = alert.labels.get("severity", "unknown")

    # Build title
    title = f"[{severity.upper()}] {alert_name}"

    # Build body from annotations
    summary = alert.annotations.get("summary", "")
    description = alert.annotations.get("description", "")

    body_parts = [f"Status: {status}"]

    if summary:
        body_parts.append(f"Summary: {summary}")

    if description:
        body_parts.append(f"Description: {description}")

    # Add additional alert info
    if len(alerts) > 1:
        body_parts.append(f"\nTotal alerts: {len(alerts)}")

    # Add labels
    if alert.labels:
        labels_str = ", ".join([f"{k}={v}" for k, v in alert.labels.items() if k not in ["alertname", "severity"]])
        if labels_str:
            body_parts.append(f"Labels: {labels_str}")

    body = "\n".join(body_parts)

    return title, body
