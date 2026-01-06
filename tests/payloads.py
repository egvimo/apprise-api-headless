# ruff: noqa E501

BASE_ALERTMANAGER_PAYLOAD = {
    "receiver": "apprise",
    "status": "firing",
    "alerts": [
        {
            "status": "firing",
            "labels": {
                "alertname": "Watchdog",
                "prometheus": "monitoring/kube-prometheus-stack-prometheus",
                "severity": "none",
            },
            "annotations": {
                "description": 'This is an alert meant to ensure that the entire alerting pipeline is functional.\nThis alert is always firing, therefore it should always be firing in Alertmanager\nand always fire against a receiver. There are integrations with various notification\nmechanisms that send a notification when this alert is not firing. For example the\n"DeadMansSnitch" integration in PagerDuty.\n',
                "runbook_url": "https://runbooks.prometheus-operator.dev/runbooks/general/watchdog",
                "summary": "An alert that should always be firing to certify that Alertmanager is working properly.",
            },
            "startsAt": "2025-11-01T09:43:24.47Z",
            "endsAt": "0001-01-01T00:00:00Z",
            "generatorURL": "http://kube-prometheus-stack-prometheus.monitoring:9090/graph?g0.expr=vector%281%29&g0.tab=1",
            "fingerprint": "7da76e02b5888fb5",
        },
        {
            "status": "firing",
            "labels": {
                "alertname": "Watchcat",
                "prometheus": "monitoring/kube-prometheus-stack-prometheus",
                "severity": "none",
            },
            "annotations": {
                "description": 'This is an alert meant to ensure that the entire alerting pipeline is functional.\nThis alert is always firing, therefore it should always be firing in Alertmanager\nand always fire against a receiver. There are integrations with various notification\nmechanisms that send a notification when this alert is not firing. For example the\n"DeadMansSnitch" integration in PagerDuty.\n',
                "runbook_url": "https://runbooks.prometheus-operator.dev/runbooks/general/watchdog",
                "summary": "An alert that should always be firing to certify that Alertmanager is working properly.",
            },
            "startsAt": "2025-11-01T09:43:24.47Z",
            "endsAt": "0001-01-01T00:00:00Z",
            "generatorURL": "http://kube-prometheus-stack-prometheus.monitoring:9090/graph?g0.expr=vector%281%29&g0.tab=1",
            "fingerprint": "7da76e02b5888fb5",
        },
    ],
    "groupLabels": {"alertname": "Watchdog"},
    "commonLabels": {
        "alertname": "Watchdog",
        "prometheus": "monitoring/kube-prometheus-stack-prometheus",
        "severity": "none",
    },
    "commonAnnotations": {
        "description": 'This is an alert meant to ensure that the entire alerting pipeline is functional.\nThis alert is always firing, therefore it should always be firing in Alertmanager\nand always fire against a receiver. There are integrations with various notification\nmechanisms that send a notification when this alert is not firing. For example the\n"DeadMansSnitch" integration in PagerDuty.\n',
        "runbook_url": "https://runbooks.prometheus-operator.dev/runbooks/general/watchdog",
        "summary": "An alert that should always be firing to certify that Alertmanager is working properly.",
    },
    "externalURL": "http://kube-prometheus-stack-alertmanager.monitoring:9093",
    "version": "4",
    "groupKey": '{}:{alertname="Watchdog"}',
    "truncatedAlerts": 0,
}
