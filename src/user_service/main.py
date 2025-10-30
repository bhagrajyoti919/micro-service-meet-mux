from fastapi import FastAPI, HTTPException, status
from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from .models import UserCreate, UserResponse, UserValidation
from .database import create_user, get_user, get_all_users, user_exists
from typing import List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="User Service",
    description="Microservice for user management",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()

@router.get("/")
def root():
    return {"service": "User Service", "status": "running"}

@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_new_user(user: UserCreate):
    try:
        logger.info(f"Creating user {user.username}")
        new_user = create_user(
            username=user.username,
            email=user.email,
            full_name=user.full_name
        )
        logger.info(f"User {new_user['user_id']} created successfully")
        return new_user
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: str):
    user = get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return user

@router.get("/users", response_model=List[UserResponse])
def list_users():
    return get_all_users()

@router.get("/users/{user_id}/validate", response_model=UserValidation)
def validate_user(user_id: str):
    logger.info(f"Validating user {user_id}")
    user = get_user(user_id)
    if not user:
        logger.warning(f"User {user_id} not found")
        return UserValidation(user_id=user_id, is_valid=False)
    
    return UserValidation(
        user_id=user_id,
        is_valid=user.get("is_active", False),
        user_details={
            "username": user["username"],
            "email": user["email"],
            "full_name": user["full_name"]
        }
    )

@router.get("/health")
def health_check():
    return {"status": "healthy", "service": "user-service"}

app.include_router(router)
