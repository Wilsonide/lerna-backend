from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.category import Category


class CategoryRepository:
    async def create(
        self,
        session,
        category: Category,
    ):
        session.add(category)

        await session.commit()

        await session.refresh(category)

        return category

    async def get_all(
        self,
        session,
    ):
        stmt = select(Category).order_by(Category.name)

        result = await session.execute(stmt)

        return result.scalars().all()

    async def get_by_id(
        self,
        session,
        category_id: int,
    ):
        stmt = (
            select(Category)
            .where(Category.id == category_id)
            .options(selectinload(Category.books))
        )

        result = await session.execute(stmt)

        return result.scalar_one_or_none()


category_repository = CategoryRepository()
