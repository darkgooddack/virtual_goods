from fastapi import APIRouter, Depends
from app.schema.user import (
    UserRegisterIn,
    UserRegisterOut,
    UserLoginIn,
    UserLoginOut
)
from app.service.user import UserService
from app.core.dependencies import get_user_service


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
