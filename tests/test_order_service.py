import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from src.order_service.main import app
from src.order_service.database import orders_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_database():
    """Clear database before each test"""
    orders_db.clear()
    yield
    orders_db.clear()

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["service"] == "Order Service"

@patch("src.order_service.main.user_service_client.validate_user")
@pytest.mark.asyncio
async def test_create_order_success(mock_validate):
    """Test successful order creation with valid user"""
    mock_validate.return_value = {
        "user_id": "user123",
        "is_valid": True,
        "user_details": {
            "username": "johndoe",
            "email": "john@example.com",
            "full_name": "John Doe"
        }
    }
    
    order_data = {
        "user_id": "user123",
        "items": [
            {
                "product_id": "prod1",
                "product_name": "Laptop",
                "quantity": 1,
                "price": 999.99
            }
        ],
        "shipping_address": "123 Main St, City, Country"
    }
    
    response = client.post("/orders", json=order_data)
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == "user123"
    assert data["total_amount"] == 999.99
    assert "order_id" in data

@patch("src.order_service.main.user_service_client.validate_user")
@pytest.mark.asyncio
async def test_create_order_invalid_user(mock_validate):
    """Test order creation with invalid user"""
    mock_validate.return_value = {
        "user_id": "invalid_user",
        "is_valid": False
    }
    
    order_data = {
        "user_id": "invalid_user",
        "items": [
            {
                "product_id": "prod1",
                "product_name": "Laptop",
                "quantity": 1,
                "price": 999.99
            }
        ],
        "shipping_address": "123 Main St"
    }
    
    response = client.post("/orders", json=order_data)
    assert response.status_code == 400

@patch("src.order_service.main.user_service_client.validate_user")
@pytest.mark.asyncio
async def test_create_order_service_unavailable(mock_validate):
    """Test order creation when user service is unavailable"""
    mock_validate.side_effect = Exception("User service unavailable")
    
    order_data = {
        "user_id": "user123",
        "items": [
            {
                "product_id": "prod1",
                "product_name": "Laptop",
                "quantity": 1,
                "price": 999.99
            }
        ],
        "shipping_address": "123 Main St"
    }
    
    response = client.post("/orders", json=order_data)
    assert response.status_code == 503

@patch("src.order_service.main.user_service_client.validate_user")
@pytest.mark.asyncio
async def test_get_order_success(mock_validate):
    """Test getting order by ID"""
    mock_validate.return_value = {
        "user_id": "user123",
        "is_valid": True,
        "user_details": {"username": "johndoe"}
    }
    
    order_data = {
        "user_id": "user123",
        "items": [{"product_id": "prod1", "product_name": "Mouse", "quantity": 2, "price": 25.00}],
        "shipping_address": "456 Oak Ave"
    }
    
    create_response = client.post("/orders", json=order_data)
    order_id = create_response.json()["order_id"]
    
    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 200
    assert response.json()["order_id"] == order_id

def test_get_order_not_found():
    """Test getting non-existent order"""
    response = client.get("/orders/nonexistent-id")
    assert response.status_code == 404

@patch("src.order_service.main.user_service_client.validate_user")
@pytest.mark.asyncio
async def test_get_user_orders(mock_validate):
    """Test getting all orders for a user"""
    mock_validate.return_value = {
        "user_id": "user123",
        "is_valid": True,
        "user_details": {"username": "johndoe"}
    }
    
    orders = [
        {
            "user_id": "user123",
            "items": [{"product_id": "prod1", "product_name": "Item1", "quantity": 1, "price": 10.00}],
            "shipping_address": "Address 1"
        },
        {
            "user_id": "user123",
            "items": [{"product_id": "prod2", "product_name": "Item2", "quantity": 2, "price": 20.00}],
            "shipping_address": "Address 2"
        }
    ]
    
    for order in orders:
        client.post("/orders", json=order)
    
    response = client.get("/users/user123/orders")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
