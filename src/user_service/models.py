from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: str

class UserResponse(BaseModel):
    user_id: str
    username: str
    email: str
    full_name: str
    created_at: datetime
    is_active: bool

class UserValidation(BaseModel):
    user_id: str
    is_valid: bool
    user_details: Optional[dict] = None
