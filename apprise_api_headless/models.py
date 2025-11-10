from typing import Optional

from pydantic import BaseModel, Field


class StatusResponse(BaseModel):
    status: str = "OK"


class NotifyRequest(BaseModel):
    title: Optional[str] = None
    body: str = Field(..., min_length=1)
    tag: Optional[str] = "all"


class NotifyResponse(BaseModel):
    success: Optional[bool]
