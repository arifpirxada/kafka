from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db.db import check_connection

from .routes import order_route

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(order_route.router)

@app.on_event("startup")
async def startup():
    await check_connection()

@app.get("/")
def read_root():
    return {"Hello": "World!"}

@app.get("/healthz")
def health():
    return {"status": "ok"}
