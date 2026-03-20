from fastapi import APIRouter
from ..schemas.payment_webhook_schema import PaymentInput
import random
import asyncio
from ..kafka.producer import kafka_producer
from ..kafka.order_events import OrderEvents

router = APIRouter(
    tags=["payment"]
)

@router.post("/webhook/payment")
async def payment_webhook(input: PaymentInput):
    try:

        # Success 70% of the time
        event_type = OrderEvents.PAYMENT_SUCCESS if random.random() < 0.7 else OrderEvents.PAYMENT_FAILED

        if input.status is not None:
            if input.status.value == "SUCCESS":
                event_type = OrderEvents.PAYMENT_SUCCESS
            elif input.status.value == "FAILED":
                event_type = OrderEvents.PAYMENT_FAILED

        event = {
            "type": event_type.value,
            "order_id": input.orderId
        }

        asyncio.create_task(kafka_producer.send_message("orders", event))

        return {
            "message": "payment process successfull",
            "status": "success"
        }
    except Exception as e:
        return {
            "message": "Error: failed to process payment",
            "status": "failed"
        }
