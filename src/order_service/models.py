from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime
from enum import Enum
from decimal import Decimal

class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class OrderItem(BaseModel):
    model_config = ConfigDict(json_encoders={Decimal: float})
    product_id: str
    product_name: str
    quantity: int = Field(..., gt=0)
    price: Decimal = Field(..., gt=0)

class OrderCreate(BaseModel):
    user_id: str
    items: List[OrderItem]
    shipping_address: str

class OrderResponse(BaseModel):
    model_config = ConfigDict(json_encoders={Decimal: float})
    order_id: str
    user_id: str
    user_details: Optional[dict] = None
    items: List[OrderItem]
    total_amount: Decimal
    status: OrderStatus
    shipping_address: str
    created_at: datetime
    updated_at: datetime
