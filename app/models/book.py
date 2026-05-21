from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )
    quantity: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    isbn: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    pages: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    language: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    publisher: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    published_date: Mapped[datetime | None] = mapped_column(
        Date,
        nullable=True,
    )

    cover_image: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    cover_public_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    is_available: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    author_id: Mapped[int] = mapped_column(
        ForeignKey("authors.id"),
        nullable=False,
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    author = relationship(
        "Author",
        back_populates="books",
    )

    category = relationship(
        "Category",
        back_populates="books",
    )

    images = relationship(
        "BookImage",
        back_populates="book",
        cascade="all, delete",
    )

    reviews = relationship(
        "Review",
        back_populates="book",
        cascade="all, delete",
    )
