from fastapi import FastAPI, HTTPException, status
from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from .models import OrderCreate, OrderResponse
from .database import create_order, get_order, get_orders_by_user, get_all_orders
from .service_client import UserServiceClient
from typing import List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Order Service",
    description="Microservice for order management with inter-service communication",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

user_service_client = UserServiceClient()

router = APIRouter()

@router.get("/")
def root():
    return {"service": "Order Service", "status": "running"}

@router.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_new_order(order: OrderCreate):
    try:
        logger.info(f"Validating user {order.user_id} with User Service")
        validation_result = await user_service_client.validate_user(order.user_id)
        
        if not validation_result.get("is_valid"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid user: User {order.user_id} does not exist or is inactive"
            )
        
        logger.info(f"Creating order for validated user {order.user_id}")
        items_dict = [item.model_dump() for item in order.items]
        new_order = create_order(
            user_id=order.user_id,
            items=items_dict,
            shipping_address=order.shipping_address,
            user_details=validation_result.get("user_details")
        )
        
        logger.info(f"Order {new_order['order_id']} created successfully")
        return new_order
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating order: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Service error: {str(e)}"
        )

@router.get("/orders/{order_id}", response_model=OrderResponse)
def get_order_by_id(order_id: str):
    order = get_order(order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {order_id} not found"
        )
    return order

@router.get("/orders", response_model=List[OrderResponse])
def list_all_orders():
    return get_all_orders()

@router.get("/users/{user_id}/orders", response_model=List[OrderResponse])
def get_user_orders(user_id: str):
    orders = get_orders_by_user(user_id)
    return orders

@router.get("/health")
def health_check():
    return {"status": "healthy", "service": "order-service"}

app.include_router(router)
