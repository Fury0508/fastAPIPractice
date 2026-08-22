from enum import Enum
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class OrderStatus(str, Enum):
    PREPARING = "preparing"
    PICKUP_UP = "pickup_up"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"


class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_name: str
    deliver_address: str
    items: str
    status: OrderStatus = Field(default=OrderStatus.PREPARING)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class OrderCreate(SQLModel):
    customer_name: str
    deliver_address: str
    items: str


class OrderUpdate(SQLModel):
    status: Optional[OrderStatus] = None
    delivery_address: Optional[str] = None


class StatusLog(SQLModel):
    order_id: int
    old_status: str
    new_status: str
    changed_at: datetime