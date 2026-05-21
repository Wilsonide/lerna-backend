from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.order import Order


class OrderRepository:
    async def create(
        self,
        session,
        order: Order,
    ):
        session.add(order)

        await session.commit()

        await session.refresh(order)

        return order

    async def get_all(
        self,
        session,
    ):
        stmt = select(Order).options(
            selectinload(Order.items),
            selectinload(Order.payment),
        )

        result = await session.execute(stmt)

        return result.scalars().all()

    async def get_by_id(
        self,
        session,
        order_id: int,
    ):
        stmt = (
            select(Order)
            .options(
                selectinload(Order.items),
                selectinload(Order.payment),
            )
            .where(Order.id == order_id)
        )

        result = await session.execute(stmt)

        return result.scalar_one_or_none()


order_repository = OrderRepository()
