from fastapi import APIRouter, Depends
from app.service.user import UserService
from app.core.dependencies import get_user_service

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register")
async def register(username: str, email: str, password: str,
                   service: UserService = Depends(get_user_service)):
    user = await service.register(username, email, password)
    return {"id": str(user.id), "email": user.email}

@router.post("/login")
async def login(email: str, password: str,
                service: UserService = Depends(get_user_service)):
    token = await service.login(email, password)
    return {"access_token": token, "token_type": "bearer"}
