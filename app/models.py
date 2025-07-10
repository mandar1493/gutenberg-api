from sqlalchemy import (Column, Integer, String, SmallInteger,ForeignKey, Table)
from sqlalchemy.orm import relationship
from .database import Base

# Tables for Many-to-Many Relationships
books_book_authors = Table('books_book_authors', Base.metadata,
    Column('book_id', Integer, ForeignKey('books_book.id'), primary_key=True),
    Column('author_id', Integer, ForeignKey('books_author.id'), primary_key=True)
)

books_book_subjects = Table('books_book_subjects', Base.metadata,
    Column('book_id', Integer, ForeignKey('books_book.id'), primary_key=True),
    Column('subject_id', Integer, ForeignKey('books_subject.id'), primary_key=True)
)

books_book_bookshelves = Table('books_book_bookshelves', Base.metadata,
    Column('book_id', Integer, ForeignKey('books_book.id'), primary_key=True),
    Column('bookshelf_id', Integer, ForeignKey('books_bookshelf.id'), primary_key=True)
)

books_book_languages = Table('books_book_languages', Base.metadata,
    Column('book_id', Integer, ForeignKey('books_book.id'), primary_key=True),
    Column('language_id', Integer, ForeignKey('books_language.id'), primary_key=True)
)

# Tables as per gutendex.dump database

class Book(Base):
    __tablename__ = "books_book"
    id = Column(Integer, primary_key=True)
    download_count = Column(Integer)
    gutenberg_id = Column(Integer, unique=True, index=True)
    media_type = Column(String(16))
    title = Column(String(1024), index=True)

    authors = relationship("Author", secondary=books_book_authors, back_populates="books")
    subjects = relationship("Subject", secondary=books_book_subjects, back_populates="books")
    bookshelves = relationship("Bookshelf", secondary=books_book_bookshelves, back_populates="books")
    languages = relationship("Language", secondary=books_book_languages, back_populates="books")
    formats = relationship("Format", back_populates="book")

class Author(Base):
    __tablename__ = "books_author"
    id = Column(Integer, primary_key=True)
    birth_year = Column(SmallInteger)
    death_year = Column(SmallInteger)
    name = Column(String(128), index=True)
    
    books = relationship("Book", secondary=books_book_authors, back_populates="authors")

class Subject(Base):
    __tablename__ = "books_subject"
    id = Column(Integer, primary_key=True)
    name = Column(String(256))

    books = relationship("Book", secondary=books_book_subjects, back_populates="subjects")

class Bookshelf(Base):
    __tablename__ = "books_bookshelf"
    id = Column(Integer, primary_key=True)
    name = Column(String(64))

    books = relationship("Book", secondary=books_book_bookshelves, back_populates="bookshelves")

class Language(Base):
    __tablename__ = "books_language"
    id = Column(Integer, primary_key=True)
    code = Column(String(4), unique=True)

    books = relationship("Book", secondary=books_book_languages, back_populates="languages")

class Format(Base):
    __tablename__ = "books_format"
    id = Column(Integer, primary_key=True)
    mime_type = Column(String(32))
    url = Column(String(256))
    book_id = Column(Integer, ForeignKey('books_book.id'))

    book = relationship("Book", back_populates="formats")