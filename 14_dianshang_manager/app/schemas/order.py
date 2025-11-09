from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from schemas.product import Product

# orderItem 是订单的详细目录
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price: float

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemInDB(OrderItemBase):
    id: int
    order_id: int
    created_at: datetime
    product_name: Optional[str] = None
    
    class Config:
        from_attributes = True

class OrderItem(BaseModel):
    product_name: str
    quantity: int
    price: float

class OrderItemWithProduct(OrderItem):
    product: Optional[Product] = None

class OrderBase(BaseModel):
    total_amount: float
    status: str = "pending"

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

class OrderUpdate(BaseModel):
    status: Optional[str] = None

class OrderInDB(OrderBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class Order(OrderInDB):
    items: List[OrderItem] = []

class AdminOrderList(OrderInDB):
    user_name: str


class AdminOrderUpdate(BaseModel):
    status: Optional[str] = None
