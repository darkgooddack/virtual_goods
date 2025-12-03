import uuid

from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: EmailStr) -> User | None:
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def create_user(self, username: str, email: EmailStr, password_hash: str) -> User:
        user = User(username=username, email=email, hash_password=password_hash)
        self.session.add(user)
        await self.session.flush()
        return user

    async def decrease_user_balance(self, user_id: uuid.UUID, amount: int):
        user = await self.session.get(User, user_id)
        user.balance -= amount
        self.session.add(user)

    async def increase_user_balance(self, user_id: uuid.UUID, amount: int):
        user = await self.session.get(User, user_id)
        user.balance += amount
        self.session.add(user)

    async def get_balance(self, user_id: uuid.UUID) -> int:
        user = await self.session.get(User, user_id)
        return user.balance

    async def get_all_user_ids(self) -> list[uuid.UUID]:
        query = select(User.id)
        result = await self.session.execute(query)
        return [row[0] for row in result.fetchall()]
