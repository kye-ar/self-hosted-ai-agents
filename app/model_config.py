from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class BaseResponse(BaseModel):
    """Base response model for API responses"""
    success: bool = True
    message: Optional[str] = None
    timestamp: datetime = datetime.now()

class ErrorResponse(BaseResponse):
    """Error response model"""
    success: bool = False
    error_code: Optional[str] = None
    details: Optional[dict] = None

class PaginatedResponse(BaseResponse):
    """Paginated response model"""
    page: int
    per_page: int
    total: int
    total_pages: int
    data: List[dict]