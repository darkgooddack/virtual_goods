import uuid

from pydantic import BaseModel


class ProductInfoOut(BaseModel):
    name: str
    product_type: str


class InventoryItemOut(BaseModel):
    product_id: uuid.UUID
    product: ProductInfoOut
    quantity: int
