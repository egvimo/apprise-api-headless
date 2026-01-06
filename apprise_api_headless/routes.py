from typing import Annotated, Optional

from apprise import Apprise
from fastapi import APIRouter, Body, HTTPException, Query, Request, status

from apprise_api_headless.alertmanager import convert_alert
from apprise_api_headless.apprise import get_apprise_instance
from apprise_api_headless.config import Settings
from apprise_api_headless.logging import logger
from apprise_api_headless.models import (
    AlertmanagerRequest,
    NotifyRequest,
    NotifyResponse,
    StatusResponse,
)

router = APIRouter()


@router.get(
    "/status",
    tags=["status"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=StatusResponse,
)
async def get_status():
    return StatusResponse()


@router.post(
    "/notify/{config_key}",
    tags=["notify"],
    summary="Send a Notification",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=NotifyResponse,
)
async def post_notify(
    config_key: str, request: Request, notify_request: Annotated[NotifyRequest, Body()]
):
    settings: Settings = request.app.state.settings
    apprise_instance: Apprise = get_apprise_instance(
        settings.apprise_config_dir, config_key
    )

    if not apprise_instance:
        msg = f"Apprise config {config_key} not found in {settings.apprise_config_dir}"
        raise HTTPException(status_code=404, detail=msg)

    result = await apprise_instance.async_notify(
        title=notify_request.title, body=notify_request.body, tag=notify_request.tag
    )

    if not result:
        msg = "One or more notification could not be sent"
        raise HTTPException(status_code=424, detail=msg)

    return NotifyResponse(success=result)


@router.post(
    "/webhook/alertmanager",
    tags=["alertmanager"],
    summary="Alertmanager Webhook",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=NotifyResponse,
)
async def post_alertmanager(
    config_key: Annotated[str, Query(...)],
    tag: Annotated[Optional[str], Query()] = None,
    request: Request = None,
    alertmanager_request: Annotated[AlertmanagerRequest, Body()] = None,
):
    """
    Accept Alertmanager webhook notifications and forward them to Apprise.

    This endpoint is designed to be used as a webhook receiver in Alertmanager.
    It converts Alertmanager alert payloads into notifications and sends them
    using the configured Apprise instance.

    Query Parameters:
        config_key: The Apprise configuration key to use
        tag: Optional tag to use for notifications
    """
    settings: Settings = request.app.state.settings
    apprise_instance: Apprise = get_apprise_instance(
        settings.apprise_config_dir, config_key
    )

    if not apprise_instance:
        msg = f"Apprise config {config_key} not found in {settings.apprise_config_dir}"
        logger.error(msg)
        raise HTTPException(status_code=404, detail=msg)

    title, body = convert_alert(alertmanager_request)

    result = await apprise_instance.async_notify(title=title, body=body, tag=tag)

    if not result:
        msg = "One or more notification could not be sent"
        raise HTTPException(status_code=424, detail=msg)

    return NotifyResponse(success=result)
