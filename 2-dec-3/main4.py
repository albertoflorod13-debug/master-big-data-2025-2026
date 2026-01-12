from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

app = FastAPI(title="Library API", version="1.1")

class BookBase(BaseModel):
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    pages: int = Field(..., gt=0)


class BookCreate(BookBase):
    """Model used when creating a book."""
    pass


class Book(BookBase):
    """Model returned by the API."""
    id: int

BOOKS: list[Book] = []
_next_id = 1

def get_next_id() -> int:
    global _next_id
    val = _next_id
    _next_id += 1
    return val

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/books", response_model=list[Book])
def list_books(
    limit: int | None = Query(default=None, ge=1),
    author: str | None = None,
    search: str | None = None,
):
    """
    Get all books with optional filters:
    - limit: max number of books
    - author: filter by author
    - search: filter by keyword in title
    """
    results = BOOKS

    if author:
        results = [b for b in results if b.author.lower() == author.lower()]

    if search:
        s = search.lower()
        results = [b for b in results if s in b.title.lower()]

    if limit:
        results = results[:limit]

    return results


@app.post("/books", response_model=Book, status_code=201)
def create_book(new_book: BookCreate):
    """
    Create a new book.
    """
    book = Book(id=get_next_id(), **new_book.model_dump())
    BOOKS.append(book)
    return book


@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    """
    Get a single book by ID.
    """
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@app.put("/books/{book_id}", response_model=Book)
def replace_book(book_id: int, updated: BookCreate):
    """
    Replace an entire book (PUT).
    """
    for i, b in enumerate(BOOKS):
        if b.id == book_id:
            new_book = Book(id=book_id, **updated.model_dump())
            BOOKS[i] = new_book
            return new_book

    raise HTTPException(status_code=404, detail="Book not found")


@app.patch("/books/{book_id}", response_model=Book)
def update_book(book_id: int, pages: int | None = None):
    """
    Update only some fields (PATCH).
    Example: just update page count.
    """
    for b in BOOKS:
        if b.id == book_id:
            if pages is not None:
                if pages <= 0:
                    raise HTTPException(status_code=400, detail="Pages must be > 0")
                b.pages = pages
            return b

    raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int):
    """
    Delete a book by ID.
    """
    for i, b in enumerate(BOOKS):
        if b.id == book_id:
            BOOKS.pop(i)
            return

    raise HTTPException(status_code=404, detail="Book not found")