from pydantic import BaseModel
from typing import List, Optional

class AuthorInfo(BaseModel):
    name: str
    birth_year: Optional[int] = None
    death_year: Optional[int] = None

    class Config:
        from_attributes = True

class Book(BaseModel):
    title: Optional[str]
    authors: List[AuthorInfo]
    genre: Optional[str] = None
    language: Optional[str] = None
    subjects: List[str]
    bookshelves: List[str]
    download_links: List[str]

    class Config:
        from_attributes = True

class BookResponse(BaseModel):
    count: int
    results: List[Book]