from typing import Annotated

from apprise import Apprise
from fastapi import APIRouter, Body, HTTPException, Request, status

from apprise_api_headless.apprise import get_apprise_instance
from apprise_api_headless.config import Settings
from apprise_api_headless.models import NotifyRequest, NotifyResponse, StatusResponse

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
        raise HTTPException(
            status_code=404,
            detail=f"Apprise config {config_key} not found in {settings.apprise_config_dir}",
        )

    result = await apprise_instance.async_notify(
        title=notify_request.title, body=notify_request.body, tag=notify_request.tag
    )

    if not result:
        raise HTTPException(
            status_code=424, detail="One or more notification could not be sent"
        )

    return NotifyResponse(success=result)
