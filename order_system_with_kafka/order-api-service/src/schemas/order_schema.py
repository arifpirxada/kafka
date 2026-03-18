import enum
from pydantic import BaseModel, Field

class PaymentType(enum.Enum):
    COD = "COD"
    ONLINE = "ONLINE"

class OrderCreatedInput(BaseModel):
    products: str
    amount: int = Field(ge=0)
    payment_type: PaymentType