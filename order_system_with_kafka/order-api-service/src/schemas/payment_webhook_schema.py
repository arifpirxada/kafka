import enum
from pydantic import BaseModel
from typing import Optional

class PaymentStatus(enum.Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

class PaymentInput(BaseModel):
    order_id: str
    status: Optional[PaymentStatus] = None