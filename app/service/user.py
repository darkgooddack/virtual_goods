import uuid

from app.schema.user import UserRegisterIn, UserLoginIn, UserLoginOut, UserRegisterOut, BalanceTopUpResponse
from app.core.security import hash_password, verify_password, create_token_pair
from app.utils.error import UserAlreadyExistsError, InvalidCredentialsError
from app.utils.redis import redis_cache


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

    async def get_all_user_ids(self) -> list[uuid.UUID]:
        return await self.repo.get_all_user_ids()

    async def top_up(self, idempotency_key, user_id, amount) -> BalanceTopUpResponse:

        # TODO: Event Sourcing
        #       Добавить запись транзакции в таблицу history_transactions
        #       Добавить колонку "operation_type" или "action", чтобы хранить
        #       тип операции: сняли (debit) или положили (credit) деньги.
        #       Это позволит видеть историю всех изменений баланса пользователя.

        cached = await redis_cache.get(idempotency_key)
        if cached:
            return BalanceTopUpResponse()

        await self.repo.increase_user_balance(user_id, amount)

        await redis_cache.set(idempotency_key, {"amount": amount}, expire=300)
        return BalanceTopUpResponse(
            amount_added=amount,
            message="Баланс успешно пополнен"
        )
