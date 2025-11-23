import uuid
from app.schema.product import ProductForBuy, ProductPurchaseResponse, ProductInfo
from app.utils.error import TransactionFailedError
from app.utils.idempotency import generate_idempotency_key
from app.utils.unit_of_work import UnitOfWork


class ProductService:
    def __init__(self, product_repo, inventory_repo, transaction_repo, payment_request_repo, user_repo):
        self.product_repo = product_repo
        self.inventory_repo = inventory_repo
        self.transaction_repo = transaction_repo
        self.payment_request_repo = payment_request_repo
        self.user_repo = user_repo

    async def process_purchase(
        self,
        user_id: uuid.UUID,
        product_id: uuid.UUID,
        payload: ProductForBuy
    ) -> ProductPurchaseResponse:

        idempotency_key = generate_idempotency_key(str(user_id), str(product_id))

        existing_request = await self.payment_request_repo.get_by_key(idempotency_key)
        if existing_request:
            return ProductPurchaseResponse(
                success=True,
                amount_spent=existing_request.amount,
                product_received=ProductInfo(
                    product_id=str(product_id),
                    quantity=payload.quantity
                ),
                message="Покупка уже обработана"
            )

        product = await self.product_repo.get_product(product_id)
        if not product or not product.is_active:
            return ProductPurchaseResponse(
                success=False,
                amount_spent=0,
                product_received=None,
                message="Товар не найден или не активен"
            )

        user_balance = await self.user_repo.get_balance(user_id)
        total_cost = product.price * payload.quantity
        if user_balance < total_cost:
            return ProductPurchaseResponse(
                success=False,
                amount_spent=0,
                product_received=None,
                message="Недостаточно средств"
            )

        inventory_item = await self.inventory_repo.get_inventory_item(user_id, product_id)
        if product.product_type == "permanent" and inventory_item is not None:
            return ProductPurchaseResponse(
                success=False,
                amount_spent=0,
                product_received=None,
                message="Товар уже куплен"
            )

        async with UnitOfWork(self.product_repo.session):
            # создаём транзакцию pending
            tx = await self.transaction_repo.create_transaction(
                user_id=user_id,
                product_id=product_id,
                amount=total_cost,
                status="pending"
            )

            try:
                # списываем деньги
                await self.product_repo.decrease_user_balance(user_id, total_cost)

                # обновляем инвентарь
                if inventory_item:
                    await self.inventory_repo.update_inventory_quantity(inventory_item, payload.quantity)
                else:
                    await self.inventory_repo.add_inventory_item(user_id, product_id, payload.quantity)

                # успешное завершение
                tx.status = "completed"
                self.product_repo.session.add(tx)

                # создаём PaymentRequest
                await self.payment_request_repo.create_request(user_id, total_cost, idempotency_key)

            except Exception as e:
                tx.status = "failed"
                self.product_repo.session.add(tx)
                raise TransactionFailedError() from e

        return ProductPurchaseResponse(
            success=True,
            amount_spent=total_cost,
            product_received=ProductInfo(
                product_id=str(product_id),
                quantity=payload.quantity
            ),
            message="Покупка успешно завершена"
        )
