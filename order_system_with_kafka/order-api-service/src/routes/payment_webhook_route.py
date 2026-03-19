from fastapi import APIRouter
from ..schemas.payment_webhook_schema import PaymentInput

router = APIRouter(
    tags=["payment"]
)

@router.post("/webhook/payment")
async def payment_webhook(input: PaymentInput):
    try:
        pass
    except Exception as e:
        return {
            "message": "Error: failed to process payment",
            "status": "failed"
        }
