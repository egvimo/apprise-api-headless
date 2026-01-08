from fastapi import FastAPI
from prometheus_client import Counter
from prometheus_fastapi_instrumentator import Instrumentator, metrics

from apprise_api_headless.logging import logger

error_counter = Counter(
    "apprise_notify_errors_total",
    "Total number of error responses for apprise notify paths",
)


def apprise_error_metric():
    def instrumentation(info: metrics.Info):
        path: str = info.request.url.path
        status_code: int = info.response.status_code
        client_host: str = (
            info.request.client.host if info.request.client else "unknown"
        )

        # Count only errors (4xx and 5xx) for /notify and /webhook paths
        if 400 <= status_code < 600 and (
            path.startswith("/notify") or path.startswith("/webhook")
        ):
            msg: str = f"{path} failed with {status_code} from {client_host}"
            logger.warning(msg)
            error_counter.inc()

    return instrumentation


def setup_metrics(app: FastAPI):
    Instrumentator().add(metrics.default()).add(apprise_error_metric()).instrument(
        app
    ).expose(app)
