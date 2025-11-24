import uuid
from typing import Optional

from pydantic import BaseModel


class ProductMixin(BaseModel):
    id: uuid.UUID


class ProductForBuy(BaseModel):
    quantity: int = 1


class ProductInfo(BaseModel):
    product_id: str
    quantity: int


class ProductPurchaseResponse(BaseModel):
    success: bool = False
    amount_spent: int = 0
    product_received: Optional[ProductInfo] = None
    message: str
