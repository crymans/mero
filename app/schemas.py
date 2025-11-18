# app/schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    telegram_id: str
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None

class UserRoleUpdate(BaseModel):
    role: str

class User(UserBase):
    id: int
    role: str
    created_at: datetime

    class Config:
        from_attributes = True

class TicketBase(BaseModel):
    qr_code: str
    price: float

class TicketCreate(TicketBase):
    pass

class Ticket(TicketBase):
    id: int
    user_id: int
    is_used: bool
    created_at: datetime

    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: str
    count: int
    is_for_table: bool
    image_url: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    products_ids: str
    quantity: int
    total_price: float
    table_id: int

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    is_fulfilled: Optional[bool] = None

class Order(OrderBase):
    id: int
    user_id: int
    is_fulfilled: bool
    created_at: datetime

    class Config:
        from_attributes = True

# app/schemas.py - добавляем ProductCreate
class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: str
    count: int
    is_for_table: bool = False
    image_url: Optional[str] = None

# app/schemas.py - добавляем недостающие схемы
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    count: Optional[int] = None
    is_for_table: Optional[bool] = None
    image_url: Optional[str] = None