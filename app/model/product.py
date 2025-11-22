import datetime
import uuid
import enum

from sqlalchemy import String, Boolean, Integer, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.db import Base


class ProductType(enum.Enum):
    CONSUMABLE = "consumable"
    PERMANENT = "permanent"


class Product(Base):
    __tablename__ = "products"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )
    description: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )
    price: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    type: Mapped[ProductType] = mapped_column(
        Enum(ProductType, name="product_type_enum"),
        nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        index=True
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(),
        index = True
    )

    transactions = relationship(
        "Transaction",
        back_populates="product",
        lazy="selectin"
    )
    inventory = relationship(
        "Inventory",
        back_populates="product",
        lazy="selectin"
    )
