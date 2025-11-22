from fastapi import HTTPException
from app.models.user import User
from app.repository.user import UserRepository
from app.core.security import hash_password, verify_password, create_access_token

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register(self, username: str, email: str, password: str) -> User:
        existing = await self.user_repo.get_by_email(email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")

        user = User(username=username, email=email, hash_password=hash_password(password))
        return await self.user_repo.create(user)

    async def login(self, email: str, password: str) -> str:
        user = await self.user_repo.get_by_email(email)
        if not user or not verify_password(password, str(user.hash_password)):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return create_access_token({"sub": str(user.id)})
