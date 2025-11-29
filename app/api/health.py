from fastapi import APIRouter, Depends
from app.core.dependencies import get_health_service
from app.service.health import HealthService


router = APIRouter(prefix="/health", tags=["health"])


@router.get("/liveness")
async def liveness():
    return {"status": "ok"}


@router.get("/readiness")
async def readiness(
     service: HealthService = Depends(get_health_service)
):
    return await service.check_health()
