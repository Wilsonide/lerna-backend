from decimal import Decimal

from app.repositories.book_repository import (
    book_repository,
)
from fastapi import HTTPException, status

from app.models.order import Order
from app.models.order_item import OrderItem
from app.repositories.order_repository import (
    order_repository,
)


class OrderService:
    async def create_order(
        self,
        session,
        user,
        data,
    ):
        total_amount = Decimal("0.00")

        order_items = []

        for item in data.items:
            book = await book_repository.get_by_id(
                session,
                item.book_id,
            )

            if not book:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Book not found",
                )

            if book.stock < item.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(f"Insufficient stock for {book.title}"),
                )

            line_total = book.price * item.quantity

            total_amount += line_total

            order_item = OrderItem(
                book_id=book.id,
                quantity=item.quantity,
                price=book.price,
            )

            order_items.append(order_item)

            book.stock -= item.quantity

        order = Order(
            total_amount=total_amount,
            shipping_address=data.shipping_address,
            phone_number=data.phone_number,
            user_id=user.id,
            items=order_items,
        )

        return await order_repository.create(
            session,
            order,
        )

    async def get_orders(
        self,
        session,
    ):
        return await order_repository.get_all(
            session,
        )

    async def get_order(
        self,
        session,
        order_id: int,
    ):
        order = await order_repository.get_by_id(
            session,
            order_id,
        )

        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found",
            )

        return order


order_service = OrderService()
