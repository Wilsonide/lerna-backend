from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class BookImagePayload(BaseModel):
    url: str
    public_id: str


class BookCreate(BaseModel):
    title: str
    description: str
    isbn: str

    price: Decimal

    quantity: int

    pages: int | None = None

    language: str | None = None

    publisher: str | None = None

    published_date: date | None = None

    author_id: int

    category_id: int

    cover_image: BookImagePayload

    images: list[BookImagePayload] = []


class BookUpdate(BaseModel):
    title: str | None = None

    description: str | None = None

    isbn: str | None = None

    price: Decimal | None = None

    quantity: int | None = None

    pages: int | None = None

    language: str | None = None

    publisher: str | None = None

    published_date: date | None = None

    author_id: int | None = None

    category_id: int | None = None

    cover_image: BookImagePayload | None = None

    images: list[BookImagePayload] | None = None


class AuthorMini(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
class CategoryMini(BaseModel):
    name: str

    class Config:
        from_attributes = True
class ImageMini(BaseModel):

    image_url: str

class BookOut(BaseModel):
    id: int
    title: str
    price: float
    cover_image: str | None = None
    description: str | None = None
    isbn: str | None = None
    pages: int | None = None
    quantity: int | None = None
    publisher: str | None = None
    published_date: date | None = None
    language: str | None = None
    images: list[ImageMini] = []
    author: AuthorMini | None = None
    category: CategoryMini | None = None

    class Config:
        from_attributes = True





class BookOutOnly(BaseModel):
    id: int
    title: str
    price: float
    cover_image: str | None = None
    description: str | None = None

    class Config:
        from_attributes = True
