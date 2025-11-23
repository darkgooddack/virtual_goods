import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import PaymentTransaction


class TransactionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_transaction(self, user_id: uuid.UUID, product_id: uuid.UUID, amount: int, status: str = "completed") -> PaymentTransaction:
        txn = PaymentTransaction(user_id=user_id, product_id=product_id, amount=amount, status=status)
        self.session.add(txn)
        await self.session.flush()
        return txn