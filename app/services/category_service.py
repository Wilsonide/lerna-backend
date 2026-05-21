from fastapi import HTTPException, status

from app.models.category import Category
from app.repositories.category_repository import (
    category_repository,
)
from app.schemas.category import CategoryUpdate


class CategoryService:
    async def create_category(
        self,
        session,
        data,
    ):
        category = Category(
            name=data.name,
        )

        return await category_repository.create(
            session,
            category,
        )

    async def get_categories(
        self,
        session,
    ):
        return await category_repository.get_all(
            session,
        )

    async def get_category(
        self,
        session,
        category_id: int,
    ):
        return await category_repository.get_by_id(
            session,
            category_id,
        )

    async def update_category(self, session, category_id: int, data: CategoryUpdate):
        category = await category_repository.get_by_id(session, category_id)

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )

        try:
            if data.name is not None:
                category.name = data.name

            await session.commit()
            await session.refresh(category)

            return category

        except Exception as e:
            await session.rollback()
            raise e

    # ✅ DELETE CATEGORY METHOD (NEW)
    async def delete_category(self, session, category_id: int):
        category = await category_repository.get_by_id(session, category_id)

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )

        try:
            await category_repository.delete(session, category)
            await session.commit()
            return {"message": "Category deleted successfully"}

        except Exception as e:
            await session.rollback()
            raise e


category_service = CategoryService()
