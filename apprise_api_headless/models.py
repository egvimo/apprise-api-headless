from typing import Optional

from pydantic import BaseModel


class StatusResponse(BaseModel):
    status: str = "OK"


class NotifyRequest(BaseModel):
    title: Optional[str] = None
    body: str
    tag: Optional[str] = "all"


class NotifyResponse(BaseModel):
    success: Optional[bool]
