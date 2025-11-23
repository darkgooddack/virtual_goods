from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db import get_session
from app.repository.inventory import InventoryRepository
from app.repository.payment import PaymentRequestRepository
from app.repository.product import ProductRepository
from app.repository.transaction import TransactionRepository
from app.repository.user import UserRepository
from app.service.product import ProductService
from app.service.user import UserService

def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    repo = UserRepository(session)
    return UserService(repo)

def get_product_service(session: AsyncSession = Depends(get_session)) -> ProductService:
    product_repo = ProductRepository(session)
    inventory_repo = InventoryRepository(session)
    transaction_repo = TransactionRepository(session)
    payment_repo = PaymentRequestRepository(session)
    user_repo = UserRepository(session)
    return ProductService(
        product_repo,
        inventory_repo,
        transaction_repo,
        payment_repo,
        user_repo
    )
