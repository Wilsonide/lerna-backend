from fastapi import APIRouter, HTTPException

from app.core.deps import DBSession, RequireAdmin
from app.schemas.book import (
    BookCreate,
    BookOut,
    BookOutOnly,
    BookUpdate,
)
from app.services.book_service import (
    book_service,
)

router = APIRouter(
    prefix="/books",
    tags=["Books"],
)


@router.post(
    "/",
    response_model=BookOutOnly,
)
async def create_book(
    data: BookCreate,
    session: DBSession,
    _: RequireAdmin,
):
    return await book_service.create_full_book(
        session,
        data,
    )


@router.get(
    "/",
    response_model=list[BookOut],
)
async def get_books(
    session: DBSession,
):
    return await book_service.get_books(
        session,
    )


@router.get(
    "/{book_id}",
    response_model=BookOut,
)
async def get_book(
    book_id: int,
    session: DBSession,
):
    book = await book_service.get_books_by_id(
        session,
        book_id,
    )

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found",
        )

    return book


@router.patch(
    "/{book_id}",
    response_model=BookOut,
)
async def update_book(
    book_id: int,
    data: BookUpdate,
    session: DBSession,
    _: RequireAdmin,
):
    updated_book = await book_service.update_book(
        session,
        book_id,
        data,
    )

    if not updated_book:
        raise HTTPException(
            status_code=404,
            detail="Book not found",
        )

    return updated_book


@router.delete(
    "/{book_id}",
)
async def delete_book(
    book_id: int,
    session: DBSession,
    _: RequireAdmin,
):
    await book_service.delete_book(
        session,
        book_id,
    )
