from fastapi import APIRouter, Depends, HTTPException, Query
from models import Order, OrderCreate, OrderUpdate, StatusLog, OrderStatus
from database import get_session
from datetime import datetime
from sqlmodel import Session, select
from typing import List

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=Order)
def create_order(order: OrderCreate, session: Session = Depends(get_session)):
    """
    Create a new order
    """
    db_order = Order(**order.model_dump())
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order

@router.get("/", response_model=list[Order])
def list_orders(
    status: OrderStatus = Query(default=None, description="Filter by order status"),
    created_date: str = Query(default=None, description="Filter by created date YYYY-MM-DD"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    session: Session = Depends(get_session)
):
    query = select(Order)
    if status:
        query = query.where(Order.status == status)
    if created_date:
        start_date = datetime.combine(created_date, datetime.min.time())
        end_date = datetime.combine(created_date, datetime.max.time())
        query = query.where(Order.created_at >= start_date, Order.created_at <= end_date)
    
    query = query.offset(skip).limit(limit)
    return session.exec(query).all()