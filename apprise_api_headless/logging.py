import logging

logger = logging.getLogger("apprise_api_headless")


class AccessFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        # Assuming record.args contains request details like method and path
        if len(record.args) > 2:
            request_method = record.args[1]
            query_string = record.args[2]
            if request_method == "GET" and query_string in ["/status", "/metrics"]:
                return False  # Filter out logs for these specific paths
        return True
