import uuid

from fastapi import APIRouter, Depends

from app.core.dependencies import get_product_service
from app.core.security import get_current_user
from app.schema.product import ProductForBuy, ProductPurchaseResponse
from app.schema.user import UserOut
from app.service.product import ProductService


router = APIRouter(prefix="/products", tags=["Продукты"])


@router.post(
    "/{product_id}/purchase",
    response_model=ProductPurchaseResponse
)
async def purchase_product(
    product_id: uuid.UUID,
    payload: ProductForBuy,
    current_user: UserOut = Depends(get_current_user),
    service: ProductService = Depends(get_product_service),
):
    res = await service.process_purchase(
        user_id=current_user.id,
        product_id=product_id,
        payload=payload
    )
    return res
