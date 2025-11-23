import uuid
from typing import Optional

from pydantic import BaseModel

class ProductMixin(BaseModel):
    id: uuid.UUID

class ProductForBuy(ProductMixin):
    quantity: int = 1

class ProductInfo(BaseModel):
    product_id: str
    quantity: int

    model_config = {"from_attributes": True}

class ProductPurchaseResponse(BaseModel):
    success: bool
    amount_spent: int
    product_received: Optional[ProductInfo] = None
    message: str

    model_config = {"from_attributes": True}
