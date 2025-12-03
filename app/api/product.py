import uuid

from fastapi import APIRouter, Depends, Header

from app.core.dependencies import get_product_service
from app.core.security import get_current_user
from app.schema.product import ProductForBuy, ProductPurchaseResponse
from app.schema.user import UserOut, UseConsumableItemResponse
from app.service.product import ProductService


router = APIRouter(prefix="/products", tags=["Продукты"])


@router.post(
    "/{product_id}/purchase",
    response_model=ProductPurchaseResponse
)
async def purchase_product(
    product_id: uuid.UUID,
    payload: ProductForBuy,
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
    current_user: UserOut = Depends(get_current_user),
    service: ProductService = Depends(get_product_service),
):
    return await service.process_purchase(
        user_id=current_user.id,
        product_id=product_id,
        payload=payload,
        idempotency_key=idempotency_key
    )


@router.post(
    "/{product_id}/use",
    response_model=UseConsumableItemResponse
)
async def use_consumable_item(
    product_id: uuid.UUID,
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
    current_user: UserOut = Depends(get_current_user),
    service: ProductService = Depends(get_product_service),
):
    return await service.use_consumable_item(
        user_id=current_user.id,
        product_id=product_id,
        idempotency_key=idempotency_key
    )
