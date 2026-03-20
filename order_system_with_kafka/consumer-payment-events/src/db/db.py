import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import text

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise Exception("Database URL Not provided")

engine = create_async_engine(DATABASE_URL)

async_session = async_sessionmaker(bind=engine, expire_on_commit=False)

async def get_db():
    async with async_session() as session:
        yield session

async def check_connection():
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
    print("✅ Database connected successfully")