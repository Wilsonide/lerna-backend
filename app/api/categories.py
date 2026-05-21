from fastapi import APIRouter, HTTPException

from app.core.deps import DBSession, RequireAdmin
from app.schemas.category import (
    CategoryCreate,
    CategoryOut,
    CategoryResponse,
    CategoryUpdate,
)
from app.services.category_service import (
    category_service,
)

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


@router.post("/")
async def create_category(
    data: CategoryCreate,
    session: DBSession,
    _: RequireAdmin,
):
    return await category_service.create_category(
        session,
        data,
    )


@router.get(
    "/",
    response_model=list[CategoryResponse],
)
async def get_categories(
    session: DBSession,
):
    return await category_service.get_categories(
        session,
    )


@router.get(
    "/{category_id}",
    response_model=CategoryOut,
)
async def get_category(
    category_id: int,
    session: DBSession,
):
    category = await category_service.get_category(
        session,
        category_id,
    )

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found",
        )

    return category


@router.patch(
    "/{category_id}",
    response_model=CategoryOut,
)
async def update_category(
    category_id: int,
    data: CategoryUpdate,
    session: DBSession,
    _: RequireAdmin,
):
    updated_category = await category_service.update_category(
        session,
        category_id,
        data,
    )

    if not updated_category:
        raise HTTPException(
            status_code=404,
            detail="Category not found",
        )

    return updated_category


@router.delete("/{category_id}")
async def delete_category(
    category_id: int,
    session: DBSession,
    _: RequireAdmin,
):
    await category_service.delete_category(session, category_id)

    return {
        "message": "Category deleted",
    }
