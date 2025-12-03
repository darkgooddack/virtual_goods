from app.repository.health import HealthRepository
from app.schema.health import HealthResponse, ServicesStatus


class HealthService:
    def __init__(self, health_repo: HealthRepository, redis_cache):
        self.health_repo = health_repo
        self.redis_cache = redis_cache

    async def check_health(self) -> HealthResponse:
        db_ok = await self.health_repo.check_db()
        redis_ok = await self.redis_cache.check_redis()
        status_code = 200 if db_ok and redis_ok else 503
        return HealthResponse(
            status=ServicesStatus(db=db_ok, redis=redis_ok),
            http_status=status_code
        )
