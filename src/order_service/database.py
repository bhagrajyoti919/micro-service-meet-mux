from typing import Dict, Optional, List
from datetime import datetime, UTC
import uuid
from decimal import Decimal

orders_db: Dict[str, dict] = {}

def create_order(user_id: str, items: list, shipping_address: str, user_details: dict = None) -> dict:
    order_id = str(uuid.uuid4())
    total_amount = sum(Decimal(item["quantity"]) * Decimal(str(item["price"])) for item in items)
    
    order = {
        "order_id": order_id,
        "user_id": user_id,
        "user_details": user_details,
        "items": items,
        "total_amount": total_amount,
        "status": "pending",
        "shipping_address": shipping_address,
        "created_at": datetime.now(UTC),
        "updated_at": datetime.now(UTC)
    }
    orders_db[order_id] = order
    return order

def get_order(order_id: str) -> Optional[dict]:
    return orders_db.get(order_id)

def get_orders_by_user(user_id: str) -> List[dict]:
    return [order for order in orders_db.values() if order["user_id"] == user_id]

def get_all_orders() -> list:
    return list(orders_db.values())
