from pydantic import BaseModel


class ServicesStatus(BaseModel):
    db: bool
    redis: bool


class HealthResponse(BaseModel):
    status: ServicesStatus
    http_status: int
