from fastapi import HTTPException, status

from app.models.author import Author
from app.repositories.author_repository import author_repository
from app.repositories.book_repository import book_repository
from app.schemas.author import AuthorUpdate  # IMPORTANT


class AuthorService:
    async def create_author(self, session, data):
        author = Author(
            name=data.name,
            bio=data.bio,
            image_url=data.image_url,
        )

        return await author_repository.create(session, author)

    async def get_authors(self, session):
        return await author_repository.get_all(session)

    async def get_author(self, session, author_id: int):
        return await author_repository.get_by_id(session, author_id)

    # 🔥 NEW METHOD (frontend requirement)
    async def get_author_with_books(self, session, author_id: int):
        author = await author_repository.get_by_id(session, author_id)

        if not author:
            return None

        result = await book_repository.get_by_author(session, author_id)
        books = [
            {
                "id": b.id,
                "title": b.title,
                "cover_url": b.cover_url,
                "price": b.price,
            }
            for b in result
        ]
        return {
            "author": {
                "id": author.id,
                "name": author.name,
                "bio": author.bio,
                "image_url": author.image_url,
            },
            "books": books,
        }

    async def update_author(self, session, author_id: int, data: AuthorUpdate):
        author = await author_repository.get_by_id(session, author_id)

        if not author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Author not found",
            )

        try:
            if data.name is not None:
                author.name = data.name

            if data.bio is not None:
                author.bio = data.bio

            if data.image_url is not None:
                author.image_url = data.image_url

            await session.commit()
            await session.refresh(author)

            return author

        except Exception as e:
            await session.rollback()
            raise e


author_service = AuthorService()
