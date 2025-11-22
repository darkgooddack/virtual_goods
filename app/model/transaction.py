import datetime
import uuid
import enum

from sqlalchemy import (
    Integer, ForeignKey, Enum, String
)
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.db import Base


class TransactionStatus(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class Transaction(Base):
    __tablename__ = "transactions"

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
    amount: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    status: Mapped[TransactionStatus] = mapped_column(
        Enum(TransactionStatus, name="transaction_status_enum"),
        nullable=False,
        index=True
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(),
        index=True
    )

    user = relationship(
        "User",
        back_populates="transactions",
        lazy="joined"
    )
    product = relationship(
        "Product",
        back_populates="transactions",
        lazy="joined"
    )


class PaymentRequest(Base):
    __tablename__ = "payment_requests"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )
    idempotency_key: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        nullable=False
    )
    amount: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now()
    )
