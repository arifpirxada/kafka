from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.db import get_db
from ..models.order_model import Order
from sqlalchemy import select
from ..schemas.order_schema import OrderCreatedInput
import uuid
import asyncio
from ..kafka.producer import kafka_producer
from ..kafka.order_events import OrderEvents

router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)

@router.get("/")
async def read_orders(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Order))
    orders = result.scalars().all()
    return orders


@router.post("/")
async def create_order(order_input: OrderCreatedInput, db: AsyncSession = Depends(get_db)):
    try:
        order_id = str(uuid.uuid4())
        db.add(Order(
            id=order_id,
            products=order_input.products,
            amount=order_input.amount,
            payment_type=order_input.payment_type.value,
        ))

        await db.commit()

        # Send Event to Kafka

        event = {
            "type": OrderEvents.ORDER_CREATED,
            "order_id": order_id 
        }

        asyncio.create_task(kafka_producer.send_message("orders", event))

        return {
            "message": "Order Created",
            "status": "success"
        }
    except Exception as e:
        await db.rollback()
        return {
            "message": "Order creation unsuccessful",
            "status": "failed"
        }