from sqlalchemy import func, select

from app.models.order import Order
from app.models.order_item import OrderItem


class AnalyticsRepository:
    async def get_total_revenue(self, session):
        stmt = select(func.sum(Order.total_amount)).where(
            Order.payment_status == "paid"
        )
        result = await session.execute(stmt)
        return result.scalar() or 0

    async def get_total_sales(self, session):
        stmt = select(func.count(Order.id)).where(Order.payment_status == "paid")
        result = await session.execute(stmt)
        return result.scalar() or 0

    async def get_best_selling_books(self, session):
        stmt = (
            select(OrderItem.book_id, func.sum(OrderItem.quantity).label("total_sold"))
            .join(Order)
            .where(Order.payment_status == "paid")
            .group_by(OrderItem.book_id)
            .order_by(func.sum(OrderItem.quantity).desc())
        )

        result = await session.execute(stmt)
        return result.all()


analytics_repository = AnalyticsRepository()
