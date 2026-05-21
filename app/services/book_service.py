from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.book import Book
from app.models.book_image import BookImage
from app.repositories.book_image_repository import book_image_repository
from app.repositories.book_repository import book_repository
from app.schemas.book import BookUpdate


class BookService:
    async def create_full_book(
        self,
        session: AsyncSession,
        data: BookUpdate,
    ):
        # check duplicate ISBN
        existing = await book_repository.get_by_isbn(
            session,
            data.isbn,
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Book already exists",
            )

        # -----------------------------
        # NORMALIZE INPUT (IMPORTANT FIX)
        # -----------------------------

        cover_url = None

        # handle both string OR object
        if isinstance(data.cover_image, str):
            cover_url = data.cover_image
        elif data.cover_image:
            cover_url = getattr(data.cover_image, "url", None)

        if not cover_url:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cover image is required",
            )

        gallery_urls = []

        if data.images:
            for img in data.images:
                if isinstance(img, str):
                    gallery_urls.append(img)
                else:
                    gallery_urls.append(getattr(img, "url", None))

        # remove None values
        gallery_urls = [x for x in gallery_urls if x]

        # -----------------------------
        # CREATE BOOK
        # -----------------------------
        book = Book(
            title=data.title,
            description=data.description,
            isbn=data.isbn,
            price=data.price,
            quantity=data.quantity,
            pages=data.pages,
            language=data.language,
            publisher=data.publisher,
            published_date=data.published_date,
            author_id=data.author_id,
            category_id=data.category_id,
            cover_image=cover_url,  # now ALWAYS string
            cover_public_id=None,
        )

        created_book = await book_repository.create(session, book)

        # -----------------------------
        # SAVE GALLERY (URL ONLY)
        # -----------------------------
        for url in gallery_urls:
            book_image = BookImage(
                image_url=url,
                book_id=created_book.id,
            )
            await book_image_repository.create(session, book_image)

        await session.commit()
        await session.refresh(created_book)

        return created_book

    async def update_book(
        self,
        session: AsyncSession,
        book_id: int,
        data: BookUpdate,
    ):
        book = await book_repository.get_by_id(session, book_id)

        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found",
            )

        # update fields (slug removed)
        fields = [
            "title",
            "description",
            "isbn",
            "price",
            "quantity",
            "pages",
            "language",
            "publisher",
            "published_date",
            "author_id",
            "category_id",
        ]

        for field in fields:
            value = getattr(data, field, None)
            if value is not None:
                setattr(book, field, value)

        # cover image
        if data.cover_image:
            book.cover_image = data.cover_image

        # gallery
        if data.images is not None:
            for img in book.images:
                await book_image_repository.delete(session, img)

            for url in data.images:
                book_image = BookImage(
                    image_url=url,
                    book_id=book.id,
                )
                await book_image_repository.create(session, book_image)

        await session.commit()
        await session.refresh(book)

        return book

    def get_books_by_id(self, session, book_id: int):
        return book_repository.get_by_id(session, book_id)

    def get_books(self, session):
        return book_repository.get_all(session)

    def get_book_by_author(self, session, author_id: int):
        return book_repository.get_by_author(session, author_id)

    async def delete_book(self, session, book_id: int):
        book = await book_repository.get_by_id(session, book_id)

        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found",
            )

        await book_repository.delete(session, book)
        await session.commit()


book_service = BookService()
