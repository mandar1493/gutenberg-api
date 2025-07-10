from sqlalchemy.orm import Session
from sqlalchemy import or_
from . import models, schemas
from typing import List, Optional

def _get_genre(book: models.Book) -> Optional[str]:
    """
    get a genre from a book's bookshelves and subjects.
    """
    # mapping of keywords to genres. This can be expanded.
    GENRE_KEYWORDS = {
        "science fiction": "Science Fiction",
        "fantasy": "Fantasy",
        "mystery": "Mystery",
        "detective": "Mystery",
        "horror": "Horror",
        "adventure": "Adventure",
        "romance": "Romance",
        "poetry": "Poetry",
        "history": "History",
        "biography": "Biography",
        "children's literature": "Children's Literature",
        "fiction": "Fiction",
    }

    # loop through bookshelves and try to create genre for book
    for bookshelf in book.bookshelves:
        shelf_name_lower = bookshelf.name.lower()
        for keyword, genre in GENRE_KEYWORDS.items():
            if keyword in shelf_name_lower:
                return genre

    # loop through subjects and try to create genre for book
    all_subjects = " ".join([s.name.lower() for s in book.subjects])
    for keyword, genre in GENRE_KEYWORDS.items():
        if keyword in all_subjects:
            return genre

    return None

def get_books(
    db: Session, 
    page: int, 
    page_size: int, 
    book_ids: List[int] = None, 
    languages: List[str] = None, 
    mime_types: List[str] = None, 
    topics: List[str] = None, 
    author: str = None, 
    title: str = None
):
    query = db.query(models.Book)   

    if book_ids:
        query = query.filter(models.Book.gutenberg_id.in_(book_ids))
    
    if languages:
        query = query.join(models.Book.languages).filter(models.Language.code.in_(languages))
    
    if mime_types:
        query = query.join(models.Book.formats).filter(models.Format.mime_type.in_(mime_types))

    if author:
        query = query.join(models.Book.authors).filter(models.Author.name.ilike(f"%{author}%"))

    if title:
        query = query.filter(models.Book.title.ilike(f"%{title}%"))
    
    if topics:
        topic_filters = []
        for topic_item in topics:
            topic_filters.append(models.Subject.name.ilike(f"%{topic_item}%"))
            topic_filters.append(models.Bookshelf.name.ilike(f"%{topic_item}%"))
        
        query = query.join(models.Book.subjects, isouter=True).join(models.Book.bookshelves, isouter=True).filter(or_(*topic_filters))
   
    # Get the total count of books with applied filters 
    total_count = query.distinct().count()

    # sort by download_count and pagination
    books_query = query.order_by(models.Book.download_count.desc())\
                       .offset((page - 1) * page_size)\
                       .limit(page_size)\
                       .distinct()

    results = books_query.all()
 
    book_objects = []
    
    for book in results:        
        book_objects.append(schemas.Book(
            title=book.title,
            authors=[schemas.AuthorInfo.model_validate(a) for a in book.authors],
            genre=_get_genre(book), 
            language=book.languages[0].code if book.languages else None,
            subjects=[s.name for s in book.subjects],
            bookshelves=[b.name for b in book.bookshelves],
            download_links=[f.url for f in book.formats] 
        ))
        
    return {"total_count": total_count, "results": book_objects}