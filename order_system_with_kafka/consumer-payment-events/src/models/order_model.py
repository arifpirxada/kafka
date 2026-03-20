import enum
from sqlalchemy import Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime, timezone
from sqlalchemy import DateTime

class Base(DeclarativeBase):
    pass


class PaymentType(enum.Enum):
    COD = "COD"
    ONLINE = "ONLINE"

class PaymentStatus(enum.Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

class DeliveryStatus(enum.Enum):
    PENDING = "PENDING"
    PACKED = "PACKED"
    SHIPPED = "SHIPPED"
    OUT = "OUT"
    DELIVERED = "DELIVERED"
    FAILED = "FAILED"


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[str] = mapped_column(primary_key=True)

    products: Mapped[str] = mapped_column(nullable=False)

    amount: Mapped[int] = mapped_column(nullable=False)

    payment_type: Mapped[PaymentType] = mapped_column(Enum(PaymentType), nullable=False)

    payment_status: Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    delivery_status: Mapped[DeliveryStatus] = mapped_column(Enum(DeliveryStatus), default=DeliveryStatus.PENDING)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    last_event_id: Mapped[str] = mapped_column(nullable=True)