from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.db import get_db
from ..models.order_model import Order
from sqlalchemy import select
from ..schemas.order_schema import OrderCreatedInput
import uuid

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
        db.add(Order(
            id=str(uuid.uuid4()),
            products=order_input.products,
            amount=order_input.amount,
            payment_type=order_input.payment_type.value,
        ))

        await db.commit()

        return {
            "message": "Order Created",
            "status": "success"
        }
    except Exception as e:
        await db.rollback()
        print(e)
        return {
            "message": "Order creation unsuccessful",
            "status": "failed"
        }