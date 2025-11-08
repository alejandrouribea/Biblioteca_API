# app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Optional

def get_book(db: Session, book_id: int) -> Optional[models.Book]:
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def get_books(db: Session, skip: int = 0, limit: int = 100, author: str = None, year: int = None) -> List[models.Book]:
    q = db.query(models.Book)
    if author:
        q = q.filter(models.Book.author.ilike(f"%{author}%"))
    if year:
        q = q.filter(models.Book.year == year)
    return q.offset(skip).limit(limit).all()

def search_books(db: Session, qstr: str) -> List[models.Book]:
    q = db.query(models.Book).filter(
        (models.Book.title.ilike(f"%{qstr}%")) | (models.Book.author.ilike(f"%{qstr}%"))
    )
    return q.all()

# app/crud.py
from fastapi import HTTPException, status

def create_book(db: Session, book: schemas.BookCreate) -> models.Book:
    # Verificar si ya existe un libro con el mismo ISBN (si se envió)
    if book.isbn:
        existing = db.query(models.Book).filter(models.Book.isbn == book.isbn).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un libro con el ISBN {book.isbn}",
            )

    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error al crear el libro: {str(e)}")
    db.refresh(db_book)
    return db_book


def update_book(db: Session, book_id: int, book_in: schemas.BookUpdate) -> Optional[models.Book]:
    db_book = get_book(db, book_id)
    if not db_book:
        return None
    for field, value in book_in.model_dump(exclude_unset=True).items():
        setattr(db_book, field, value)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int) -> bool:
    db_book = get_book(db, book_id)
    if not db_book:
        return False
    db.delete(db_book)
    db.commit()
    return True
