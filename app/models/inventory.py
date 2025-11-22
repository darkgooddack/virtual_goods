import datetime
import uuid

from sqlalchemy import (
    Integer, ForeignKey, UniqueConstraint
)
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.db import Base


class Inventory(Base):
    __tablename__ = "inventory"

    __table_args__ = (
        UniqueConstraint("user_id", "product_id", name="uq_inventory_user_product"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
        index=True
    )
    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1
    )
    purchased_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now()
    )

    user = relationship(
        "User",
        back_populates="inventory",
        lazy="selectin"
    )
    product = relationship(
        "Product",
        back_populates="inventory",
        lazy="selectin"
    )
