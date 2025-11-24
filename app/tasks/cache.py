from app.database.db import new_session
from app.repository.user import UserRepository
from app.service.user import UserService
from app.utils.redis import redis_cache
from app.utils.celery_app import celery_app
import asyncio


@celery_app.task
def clear_inventory_cache():
    async def _clear():
        async with new_session() as session:
            user_repo = UserRepository(session)
            user_service = UserService(user_repo)

            user_ids = await user_service.get_all_user_ids()
            for user_id in user_ids:
                key = f"user:{user_id}:inventory"
                await redis_cache.delete(key)

    asyncio.run(_clear())
