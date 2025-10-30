from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.user_service.main import router as user_router
from src.order_service.main import router as order_router

app = FastAPI(
    title="Microservice Gateway",
    description="Unified FastAPI app exposing User and Order services on a single port",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="/user-service")
app.include_router(order_router, prefix="/order-service")

@app.get("/")
def root():
    return {"service": "gateway", "status": "running", "docs": "/docs"}