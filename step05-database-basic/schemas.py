"""
Pydantic 스키마 정의
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# 사용자 스키마
class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    age: int = Field(..., ge=1, le=120)

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(None, ge=1, le=120)
    is_active: Optional[bool] = None

class UserInDB(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# 제품 스키마
class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    price: float = Field(..., gt=0)
    category: str = Field(..., min_length=1, max_length=100)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    price: Optional[float] = Field(None, gt=0)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    is_available: Optional[bool] = None

class ProductInDB(ProductBase):
    id: int
    is_available: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # 가격을 센트에서 원으로 변환
    @property
    def price(self):
        return self._price / 100
    
    @price.setter
    def price(self, value):
        self._price = int(value * 100)
    
    class Config:
        from_attributes = True
