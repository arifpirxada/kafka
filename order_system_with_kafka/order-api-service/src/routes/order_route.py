from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.db import get_db
from ..models.order_model import Order
from sqlalchemy import select

router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)

@router.get("/")
async def read_orders(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Order))
    orders = result.scalars().all()
    return orders