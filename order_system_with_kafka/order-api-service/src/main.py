from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db.db import check_connection
from contextlib import asynccontextmanager
from .kafka.producer import kafka_producer

from .routes import order_route
from .routes import payment_webhook_route

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    await check_connection() # check Database connection
    yield
    # Shutdown: Wait for remaining messages to be sent
    kafka_producer.flush()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(order_route.router)
app.include_router(payment_webhook_route.router)

@app.get("/")
def read_root():
    return {"Hello": "Kafka!"}

@app.get("/healthz")
def health():
    return {"status": "ok"}
