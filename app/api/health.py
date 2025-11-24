from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db import get_session
from app.utils.redis import redis_cache

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/liveness")
async def liveness():
    print("we")
    return {"status": "ok"}

@router.get("/readiness")
async def readiness(
        session: AsyncSession = Depends(get_session)
):
    health = {"db": False, "redis": False}

    try:
        async with session.begin():
            await session.execute("SELECT 1")
        health["db"] = True
    except Exception:
        health["db"] = False

    try:
        pong = await redis_cache.redis.ping()
        health["redis"] = pong
    except Exception:
        health["redis"] = False

    status_code = 200 if all(health.values()) else 503
    return health, status_code
