from typing import Dict, Optional
from datetime import datetime, UTC
import uuid

users_db: Dict[str, dict] = {}

def create_user(username: str, email: str, full_name: str) -> dict:
    user_id = str(uuid.uuid4())
    user = {
        "user_id": user_id,
        "username": username,
        "email": email,
        "full_name": full_name,
        "created_at": datetime.now(UTC),
        "is_active": True
    }
    users_db[user_id] = user
    return user

def get_user(user_id: str) -> Optional[dict]:
    return users_db.get(user_id)

def get_all_users() -> list:
    return list(users_db.values())

def user_exists(user_id: str) -> bool:
    return user_id in users_db
