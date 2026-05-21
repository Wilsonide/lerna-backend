from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class BookImage(Base):
    __tablename__ = "book_images"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    image_url: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id"),
        nullable=False,
    )

    book = relationship(
        "Book",
        back_populates="images",
    )
