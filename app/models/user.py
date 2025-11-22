import datetime
import uuid

from sqlalchemy import String, Integer, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True
    )
    email: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True
    )
    hash_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    balance: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now()
    )

    transactions = relationship(
        "PaymentTransaction",
        back_populates="user",
        lazy="selectin"
    )
    payment_requests = relationship(
        "PaymentRequest",
        back_populates="user",
        lazy="selectin"
    )
    inventory = relationship(
        "Inventory",
        back_populates="user",
        lazy="selectin"
    )
