FROM python:3.14-alpine AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /build

ADD . /build
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-dev --locked --no-editable

FROM builder

RUN addgroup -g 1000 apprise \
    && adduser -u 1000 -G apprise -s /bin/bash -D apprise

WORKDIR /apprise/app

COPY config config/
COPY --from=builder /build/.venv .venv/
COPY apprise_api_headless apprise_api_headless/
RUN chown -R apprise:apprise /apprise

USER apprise

ENV APPRISE_CONFIG_DIR="/apprise/config"

EXPOSE 8000

CMD ["/apprise/app/.venv/bin/uvicorn", "apprise_api_headless.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--log-config", "config/log_config.yaml"]
