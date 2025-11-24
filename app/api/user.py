from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.schema.inventory import InventoryItemOut
from app.schema.user import (
    UserRegisterIn,
    UserRegisterOut,
    UserLoginIn,
    UserLoginOut, UserOut
)
from app.service.inventory import InventoryService
from app.service.user import UserService
from app.core.dependencies import get_user_service, get_inventory_service
from app.utils.redis import redis_cache
from app.tasks.cache import clear_inventory_cache


router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.post("/register", response_model=UserRegisterOut)
async def register(
    payload: UserRegisterIn,
    service: UserService = Depends(get_user_service)
) -> UserRegisterOut:
    return await service.register(payload)


@router.post("/login", response_model=UserLoginOut)
async def login(
    payload: UserLoginIn,
    service: UserService = Depends(get_user_service)
) -> UserLoginOut:
   return await service.login(payload)


@router.get("/inventory", response_model=list[InventoryItemOut])
async def receiving_inventory(
    current_user: UserOut = Depends(get_current_user),
    service: InventoryService = Depends(get_inventory_service),
):
    return await service.get_user_inventory(current_user.id)


@router.post("/test-clear-cache")
async def test_clear_cache():
    print("fe")
    keys_before = await redis_cache.redis.keys("user:*:inventory")
    clear_inventory_cache.delay()  # ставим задачу в очередь
    return {"keys_before": keys_before, "message": "Task queued"}