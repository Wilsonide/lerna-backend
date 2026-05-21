from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.author import Author


class AuthorRepository:
    async def create(
        self,
        session,
        author: Author,
    ):
        session.add(author)

        await session.commit()

        await session.refresh(author)

        return author

    async def get_all(
        self,
        session,
    ):
        stmt = select(Author).options(selectinload(Author.books))

        result = await session.execute(stmt)

        return result.scalars().all()

    async def get_by_id(
        self,
        session,
        author_id: int,
    ):
        stmt = (
            select(Author)
            .where(Author.id == author_id)
            .options(selectinload(Author.books))
        )

        result = await session.execute(stmt)

        return result.scalar_one_or_none()


author_repository = AuthorRepository()
