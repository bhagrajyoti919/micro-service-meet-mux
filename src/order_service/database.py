import os
from pymongo import MongoClient
from dotenv import load_dotenv
from typing import Dict, Optional, List
from datetime import datetime, UTC, timezone
import uuid
from decimal import Decimal

load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')
DB_NAME = os.getenv('DB_NAME', 'meet_mux')

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
orders_col = db['orders']

def create_order(user_id: str, items: list, shipping_address: str, user_details: dict = None) -> dict:
    order_id = str(uuid.uuid4())
    total_amount = sum(Decimal(item["quantity"]) * Decimal(str(item["price"])) for item in items)
    
    order = {
        "order_id": order_id,
        "user_id": user_id,
        "user_details": user_details,
        "items": items,
        "total_amount": float(total_amount),
        "status": "pending",
        "shipping_address": shipping_address,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    }
    orders_col.insert_one(order)
    return order

def get_order(order_id: str) -> Optional[dict]:
    order = orders_col.find_one({"order_id": order_id})
    if order:
        order.pop('_id', None)
    return order

def get_orders_by_user(user_id: str) -> List[dict]:
    orders = list(orders_col.find({"user_id": user_id}))
    for o in orders:
        o.pop('_id', None)
    return orders

def get_all_orders() -> list:
    orders = list(orders_col.find())
    for o in orders:
        o.pop('_id', None)
    return orders
