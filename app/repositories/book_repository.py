from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.book import Book


class BookRepository:
    async def create(
        self,
        session,
        book: Book,
    ):
        session.add(book)

        await session.flush()

        await session.refresh(book)

        return book

    async def get_by_id(
        self,
        session,
        book_id: int,
    ):
        stmt = (
            select(Book)
            .options(
                selectinload(Book.images),
                selectinload(Book.author),
                selectinload(Book.category),
            )
            .where(Book.id == book_id)
        )

        result = await session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_by_author(self, session, author_id: int):
        stmt = (
            select(Book)
            .where(Book.author_id == author_id)
            .options(
                selectinload(Book.images),
                selectinload(Book.author),
                selectinload(Book.category),
            )
        )

        result = await session.execute(stmt)
        return result.scalars().all()

    async def get_by_isbn(
        self,
        session,
        isbn: str,
    ):
        stmt = (
            select(Book)
            .where(Book.isbn == isbn)
            .options(
                selectinload(Book.images),
                selectinload(Book.author),
                selectinload(Book.category),
            )
        )

        result = await session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_all(
        self,
        session,
    ):
        stmt = select(Book).options(
            selectinload(Book.images),
            selectinload(Book.author),
            selectinload(Book.category),
        )

        result = await session.execute(stmt)

        return result.scalars().all()

    async def delete(
        self,
        session,
        book: Book,
    ):
        await session.delete(book)


book_repository = BookRepository()
