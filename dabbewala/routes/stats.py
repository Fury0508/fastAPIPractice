from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select, func
from models import Order, OrderStatus
from database import get_session


router = APIRouter(prefix="/stats", tags=["stats"])

@router.get("/daily")
def daily_summary(
    summary_date: datetime | None = Query(default=None, description="Filter by date YYYY-MM-DD"),
    session: Session = Depends(get_session)
):
    if summary_date is None:
        summary_date = datetime.now().date()
    else:
        summary_date = summary_date.date()
    start = datetime.combine(summary_date, datetime.min.time())
    end = datetime.combine(summary_date, datetime.max.time())
    summary = {}
    total = 0

    for status in OrderStatus:
        count = session.exec(
            select(func.count(Order.id)).where(
                Order.status == status,
                Order.created_at >= start,
                Order.created_at <= end
            )

        ).one()
        summary[status.value] = count
        total += count

    return {
        "date": summary_date.isoformat(),
        "total_orders": total,
        "summary": summary
    }


        