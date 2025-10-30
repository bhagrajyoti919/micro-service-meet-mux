import httpx
from typing import Optional
import logging
import os
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()

class UserServiceClient:
    
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or os.getenv("USER_SERVICE_URL", "http://localhost:8000")
        try:
            self.timeout = float(os.getenv("SERVICE_TIMEOUT", "5"))
        except ValueError:
            self.timeout = 5.0
    
    async def validate_user(self, user_id: str) -> dict:
        url = f"{self.base_url}/users/{user_id}/validate"
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url)
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 404:
                    logger.warning(f"User {user_id} not found in User Service")
                    return {"user_id": user_id, "is_valid": False}
                else:
                    logger.error(f"User Service returned status {response.status_code}")
                    return {"user_id": user_id, "is_valid": False}
                    
        except httpx.TimeoutException:
            logger.error(f"Timeout while validating user {user_id}")
            raise Exception("User service timeout - please try again")
        except httpx.ConnectError:
            logger.error(f"Cannot connect to User Service at {self.base_url}")
            raise Exception("User service unavailable")
        except Exception as e:
            logger.error(f"Error validating user: {str(e)}")
            raise Exception(f"Error communicating with user service: {str(e)}")
