import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Inventory


class InventoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_inventory_item(self, user_id: uuid.UUID, product_id: uuid.UUID) -> Inventory | None:
        result = await self.session.execute(
            select(Inventory)
            .where(Inventory.user_id == user_id)
            .where(Inventory.product_id == product_id)
        )
        return result.scalar_one_or_none()

    async def add_inventory_item(self, user_id: uuid.UUID, product_id: uuid.UUID, quantity: int) -> Inventory:
        item = Inventory(user_id=user_id, product_id=product_id, quantity=quantity)
        self.session.add(item)
        await self.session.flush()
        return item

    async def update_inventory_quantity(self, item: Inventory, quantity: int):
        item.quantity += quantity
        self.session.add(item)
        await self.session.flush()

    async def get_by_user_id(self, user_id: uuid.UUID):
        query = (
            select(Inventory)
            .where(Inventory.user_id == user_id)
            .options(
                selectinload(Inventory.product)
            )
        )
        result = await self.session.execute(query)
        return result.scalars().all()
