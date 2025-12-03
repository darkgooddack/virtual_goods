import uuid
from sqlalchemy import select
from app.models.transaction import PaymentRequest


class PaymentRequestRepository:
    def __init__(self, session):
        self.session = session

    async def get_by_key(self, key: str):
        result = await self.session.execute(
            select(PaymentRequest).where(PaymentRequest.idempotency_key == key)
        )
        return result.scalar_one_or_none()

    async def create_request(self, user_id: uuid.UUID, amount: int, key: str):
        request = PaymentRequest(user_id=user_id, amount=amount, idempotency_key=key)
        self.session.add(request)
        return request
