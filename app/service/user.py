from app.models import User
from app.schema.user import UserRegisterIn, UserLoginIn, UserLoginOut, UserRegisterOut
from app.core.security import hash_password, verify_password, create_token_pair
from app.utils.error import UserAlreadyExistsError, InvalidCredentialsError


class UserService:
    def __init__(self, repo):
        self.repo = repo

    async def register(self, data: UserRegisterIn) -> UserRegisterOut:
        existing = await self.repo.get_by_email(data.email)
        if existing:
            raise UserAlreadyExistsError()

        user = await self.repo.create_user(
            username=data.username,
            email=data.email,
            password_hash=hash_password(data.password)
        )

        return UserRegisterOut(id=user.id, email=user.email)

    async def login(self, data: UserLoginIn) -> UserLoginOut:
        user = await self.repo.get_by_email(data.email)
        if not user or not verify_password(data.password, str(user.hash_password)):
            raise InvalidCredentialsError()

        return create_token_pair(str(user.id))
