from fastapi import FastAPI
from prometheus_client import Counter
from prometheus_fastapi_instrumentator import Instrumentator, metrics

error_counter = Counter(
    "apprise_notify_errors_total",
    "Total number of error responses for apprise notify paths",
)


def apprise_error_metric():
    def instrumentation(info: metrics.Info):
        path: str = info.request.url.path
        status_code: int = info.response.status_code

        # Count only errors (4xx and 5xx) for /notify paths
        if 400 <= status_code < 600 and path.startswith("/notify"):
            error_counter.inc()

    return instrumentation


def setup_metrics(app: FastAPI):
    Instrumentator().add(metrics.default()).add(apprise_error_metric()).instrument(
        app
    ).expose(app)
