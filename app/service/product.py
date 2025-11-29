import uuid
from app.schema.product import ProductForBuy, ProductPurchaseResponse, ProductInfo
from app.schema.user import UseConsumableItemResponse
from app.utils.error import TransactionFailedError
from app.utils.redis import redis_cache
from app.utils.unit_of_work import UnitOfWork


class ProductService:
    def __init__(
        self,
        product_repo,
        inventory_repo,
        transaction_repo,
        payment_request_repo,
        user_repo
    ):
        self.product_repo = product_repo
        self.inventory_repo = inventory_repo
        self.transaction_repo = transaction_repo
        self.payment_request_repo = payment_request_repo
        self.user_repo = user_repo

    async def _get_active_product(self, product_id):
        product = await self.product_repo.get_product(product_id)
        if not product or not product.is_active:
            return None
        return product

    @staticmethod
    async def _check_idempotency_redis(key, product_id):
        cached = await redis_cache.get(key)
        if not cached:
            return None
        return ProductPurchaseResponse(
            success=True,
            amount_spent=cached["amount"],
            product_received=ProductInfo(
                product_id=str(product_id),
                quantity=cached["quantity"]
            ),
            message="Операция уже обработана (cache)"
        )

    async def _check_idempotency_db(self, key):
        existing = await self.payment_request_repo.get_by_key(key)
        if not existing:
            return None
        return ProductPurchaseResponse(
            success=True,
            amount_spent=existing.amount,
            product_received=None,
            message="Операция уже обработана (db)"
        )

    async def _check_user_balance(self, user_id, total_cost):
        balance = await self.user_repo.get_balance(user_id)
        return balance >= total_cost

    async def _check_permanent_product_limit(self, user_id, product_id, product):
        inventory_item = await self.inventory_repo.get_inventory_item(user_id, product_id)

        if product.product_type == "permanent" and inventory_item:
            return False, inventory_item

        return True, inventory_item

    async def _perform_purchase_tx(
        self, user_id, product_id, total_cost, quantity, inventory_item, idempotency_key
    ):
        async with UnitOfWork(self.product_repo.session):
            try:
                tx = await self.transaction_repo.create_transaction(
                    user_id=user_id,
                    product_id=product_id,
                    amount=total_cost,
                    status="pending"
                )

                await self.user_repo.decrease_user_balance(user_id, total_cost)

                if inventory_item:
                    await self.inventory_repo.update_inventory_quantity(
                        inventory_item, quantity
                    )
                else:
                    await self.inventory_repo.add_inventory_item(
                        user_id, product_id, quantity
                    )

                tx.status = "completed"

                if idempotency_key:
                    await self.payment_request_repo.create_request(
                        user_id, total_cost, idempotency_key
                    )
                    await redis_cache.set(
                        idempotency_key,
                        {"amount": total_cost, "quantity": quantity},
                        expire=300
                    )

            except Exception:
                tx.status = "failed"
                raise TransactionFailedError()

    async def process_purchase(
        self,
        user_id: uuid.UUID,
        product_id: uuid.UUID,
        payload: ProductForBuy,
        idempotency_key: str
    ) -> ProductPurchaseResponse:

        product = await self._get_active_product(product_id)
        if not product:
            return ProductPurchaseResponse(message="Товар не найден или не активен")

        if idempotency_key:
            redis_result = await self._check_idempotency_redis(idempotency_key, product_id)
            if redis_result:
                return redis_result

        db_result = await self._check_idempotency_db(idempotency_key)
        if db_result:
            return db_result

        total_cost = product.price * payload.quantity

        if not await self._check_user_balance(user_id, total_cost):
            return ProductPurchaseResponse(message="Недостаточно средств")

        can_buy, inventory_item = await self._check_permanent_product_limit(
            user_id, product_id, product
        )
        if not can_buy:
            return ProductPurchaseResponse(message="Товар уже куплен")

        await self._perform_purchase_tx(
            user_id,
            product_id,
            total_cost,
            payload.quantity,
            inventory_item,
            idempotency_key
        )

        return ProductPurchaseResponse(
            success=True,
            amount_spent=total_cost,
            product_received=ProductInfo(
                product_id=str(product_id),
                quantity=payload.quantity
            ),
            message="Покупка успешно завершена"
        )

    async def use_consumable_item(self, user_id, product_id, idempotency_key) -> UseConsumableItemResponse:

        cached = await redis_cache.get(idempotency_key)
        if cached:
            return UseConsumableItemResponse(
                message="Операция уже обработана",
                remaining_quantity=cached.get("remaining_quantity")
            )

        inventory_item = await self.inventory_repo.get_inventory_item(user_id, product_id)
        if not inventory_item or inventory_item.quantity <= 0:
            return UseConsumableItemResponse(
                success=False,
                message="У пользователя нет такого товара",
                remaining_quantity=0
            )

        await self.inventory_repo.update_inventory_quantity(inventory_item, -1)

        await redis_cache.set(
            idempotency_key,
            {"remaining_quantity": inventory_item.quantity},
            expire=300
        )

        return UseConsumableItemResponse(
            message="Товар использован",
            remaining_quantity=inventory_item.quantity
        )






