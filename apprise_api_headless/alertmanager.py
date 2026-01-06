from typing import Optional

from apprise_api_headless.models import AlertmanagerRequest

STATUS_ICONS = {
    "firing": "🔥",
    "resolved": "✅",
}


def convert_alert(
    payload: AlertmanagerRequest,
) -> tuple[Optional[str], str]:
    """
    Convert Alertmanager webhook payload to title and body for notification.

    Returns:
        Tuple of (title, body)
    """
    alerts = payload.alerts
    overall_status = payload.status

    if not alerts:
        return None, f"Alertmanager: {overall_status}"

    messages: list[str] = []

    for alert in alerts:
        labels = alert.labels or {}
        annotations = alert.annotations or {}

        alertname = labels.get("alertname", "Unknown Alert")
        severity = labels.get("severity", "unknown")
        summary = annotations.get("summary", "")
        description = annotations.get("description", "")

        message_parts = [
            f"**Alert:** {alertname}",
            f"**Status:** {alert.status.upper()}",
            f"**Severity:** {severity}",
        ]

        if summary:
            message_parts.extend(["", f"**Summary:** {summary}"])

        if description:
            message_parts.extend(["", f"**Description:** {description}"])

        messages.append("\n".join(message_parts))

    final_message = "\n---\n".join(messages)

    icon = STATUS_ICONS.get(overall_status.lower(), "ℹ️")
    title = f"{icon} [{overall_status.upper()}: {len(alerts)}] Alerts"

    return title, final_message
