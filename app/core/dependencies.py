from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db import get_session
from app.repository.health import HealthRepository
from app.repository.inventory import InventoryRepository
from app.repository.payment import PaymentRequestRepository
from app.repository.product import ProductRepository
from app.repository.transaction import TransactionRepository
from app.repository.user import UserRepository
from app.service.health import HealthService
from app.service.inventory import InventoryService
from app.service.product import ProductService
from app.service.user import UserService
from app.utils.redis import redis_cache, RedisCache




def get_redis_cache():
    return redis_cache

def get_health_service(
    health_repo: HealthRepository = Depends(),
    redis_cache: RedisCache = Depends(get_redis_cache)
) -> HealthService:
    return HealthService(health_repo, redis_cache)

def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    repo = UserRepository(session)
    return UserService(repo)

def get_inventory_service(
    session: AsyncSession = Depends(get_session)
) -> InventoryService:
    inventory_repo = InventoryRepository(session)
    product_repo = ProductRepository(session)
    return InventoryService(inventory_repo, product_repo, redis_cache)

def get_product_service(session: AsyncSession = Depends(get_session)) -> ProductService:
    product_repo = ProductRepository(session)
    inventory_repo = InventoryRepository(session)
    transaction_repo = TransactionRepository(session)
    payment_repo = PaymentRequestRepository(session)
    user_repo = UserRepository(session)
    return ProductService(
        product_repo,
        inventory_repo,
        transaction_repo,
        payment_repo,
        user_repo
    )
