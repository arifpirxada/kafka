from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/")
def read_root():
    return {"Hello": "World!"}

