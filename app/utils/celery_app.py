from celery import Celery
from app.core.config import settings


celery_app = Celery(
    "worker",
    broker=settings.redis.broker_url,
    backend=settings.redis.backend_url,
    include=["app.tasks.cache"]
)

celery_app.conf.beat_schedule = {
    "clear_inventory_cache_daily": {
        "task": "app.tasks.cache.clear_inventory_cache",
        "schedule": 24*60*60,
    }
}
celery_app.conf.timezone = "UTC"
