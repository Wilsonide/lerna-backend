import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.core.cloudinary
from app.api import (
    auth,
    authors,
    books,
    categories,
    email_verify,
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://lerna-frontend-fvvw.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(email_verify.router)
app.include_router(authors.router)
app.include_router(books.router)
app.include_router(categories.router)


def main():
    uvicorn.run(app, host="localhost", port=8001)


if __name__ == "__main__":
    main()
