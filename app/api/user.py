from fastapi import APIRouter, Depends, Header

from app.core.security import get_current_user
from app.schema.inventory import InventoryItemOut
from app.schema.user import (
    UserRegisterIn,
    UserRegisterOut,
    UserLoginIn,
    UserLoginOut, UserOut, BalanceTopUpRequest, BalanceTopUpResponse
)
from app.service.inventory import InventoryService
from app.service.user import UserService
from app.core.dependencies import get_user_service, get_inventory_service


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


@router.post("/add-funds", response_model=BalanceTopUpResponse)
async def top_up_balance(
    payload: BalanceTopUpRequest,
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
    current_user: UserOut = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    return await service.top_up(idempotency_key, current_user.id, payload.top_up_amount)
