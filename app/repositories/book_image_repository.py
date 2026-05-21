from sqlalchemy import select

from app.models.book_image import BookImage


class BookImageRepository:

    async def create(
        self,
        session,
        image: BookImage,
    ):

        session.add(image)

        await session.flush()

        await session.refresh(image)

        return image

    async def get_book_images(
        self,
        session,
        book_id: int,
    ):

        stmt = select(BookImage).where(
            BookImage.book_id == book_id
        )

        result = await session.execute(stmt)

        return result.scalars().all()

    async def delete(
        self,
        session,
        image: BookImage,
    ):

        await session.delete(image)


book_image_repository = BookImageRepository()