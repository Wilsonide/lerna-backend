from fastapi import APIRouter, HTTPException

from app.core.deps import DBSession, RequireAdmin
from app.schemas.author import (
    AuthorCreate,
    AuthorOut,
    AuthorUpdate,
)
from app.services.author_service import (
    author_service,
)

router = APIRouter(
    prefix="/authors",
    tags=["Authors"],
)


@router.post("/")
async def create_author(
    data: AuthorCreate,
    session: DBSession,
    _: RequireAdmin,
):
    return await author_service.create_author(
        session,
        data,
    )


@router.get(
    "/",
    response_model=list[AuthorOut],
)
async def get_authors(
    session: DBSession,
):
    return await author_service.get_authors(
        session,
    )


@router.get(
    "/{author_id}",
    response_model=AuthorOut,
)
async def get_author(
    author_id: int,
    session: DBSession,
):
    author = await author_service.get_author(
        session,
        author_id,
    )

    if not author:
        raise HTTPException(
            status_code=404,
            detail="Author not found",
        )

    return author


@router.patch(
    "/{author_id}",
    response_model=AuthorOut,
)
async def update_author(
    author_id: int,
    data: AuthorUpdate,
    session: DBSession,
    _: RequireAdmin,
):
    updated_author = await author_service.update_author(
        session,
        author_id,
        data,
    )

    if not updated_author:
        raise HTTPException(
            status_code=404,
            detail="Author not found",
        )

    return updated_author


@router.delete("/{author_id}")
async def delete_author(
    author_id: int,
    session: DBSession,
    _: RequireAdmin,
):
    deleted = await author_service.delete_author(
        session,
        author_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Author not found",
        )

    return {
        "message": "Author deleted",
    }
