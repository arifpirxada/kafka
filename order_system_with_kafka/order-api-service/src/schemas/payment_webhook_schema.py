import enum
from pydantic import BaseModel

class PaymentStatus(enum.Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

class PaymentInput(BaseModel):
    orderId: str
    status: PaymentStatus