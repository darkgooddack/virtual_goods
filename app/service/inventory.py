import uuid

from app.schema.inventory import InventoryItemOut


class InventoryService:
    def __init__(
        self,
        inventory_repo,
        product_repo,
        cache,
    ):
        self.inventory_repo = inventory_repo
        self.product_repo = product_repo
        self.cache = cache

    async def get_user_inventory(self, user_id: uuid.UUID):
        cache_key = f"user:{user_id}:inventory"

        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        items = await self.inventory_repo.get_by_user_id(user_id)
        result = [
            InventoryItemOut.model_validate(item, from_attributes=True)
            for item in items
        ]

        data = [item.model_dump(mode="json") for item in result]

        await self.cache.set(cache_key, data, expire=300)
        return result
