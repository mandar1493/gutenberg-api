from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from . import utils,  schemas
from .database import get_db

app = FastAPI(
    title="Project Gutenberg API",
    description="An API to query and access e-books from the Project Gutenberg dataset.",
    version="1.0.0",
)

@app.get("/books", response_model=schemas.BookResponse)
def read_books(
    book_id: Optional[str] = Query(None, description="List of Project Gutenberg ID numbers."),
    language: Optional[str] = Query(None, description="List of 2-letter language codes (e.g., en,fr)"),
    mime_type: Optional[str] = Query(None, description="List of the MIME types of the book format."),
    topic: Optional[str] = Query(None, description="List of topics"),
    author: Optional[str] = Query(None, description="The name of the author."),
    title: Optional[str] = Query(None, description="The title of the book."),
    page: int = Query(1, ge=1, description="Page number for pagination."),
    page_size: int = Query(25, ge=1, le=100, description="Number of results per page."),
    db: Session = Depends(get_db)
):
    """
    Retrieve books based on applied filter.
    Supports pagination and sorting by download count.
    """
    book_ids_list = [int(i.strip()) for i in book_id.split(',')] if book_id else None
    languages_list = [lang.strip() for lang in language.split(',')] if language else None
    mime_types_list = [mime.strip() for mime in mime_type.split(',')] if mime_type else None
    topics_list = [t.strip() for t in topic.split(',')] if topic else None

    try:
        data = utils.get_books(
            db=db,
            page=page,
            page_size=page_size,
            book_ids=book_ids_list,
            languages=languages_list,
            mime_types=mime_types_list,
            topics=topics_list,
            author=author,
            title=title,
        )
        return schemas.BookResponse(count=data["total_count"], results=data["results"])
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="An internal error.")
