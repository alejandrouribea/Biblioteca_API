# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, Base, get_db

# crea tablas si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Biblioteca API")

@app.post("/books/", response_model=schemas.Book, status_code=status.HTTP_201_CREATED)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    created = crud.create_book(db, book)
    return created

@app.get("/books/", response_model=list[schemas.Book])
def list_books(author: str | None = Query(None), year: int | None = Query(None), skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_books(db, skip=skip, limit=limit, author=author, year=year)

@app.get("/books/search/", response_model=list[schemas.Book])
def search_books(q: str = Query(...), db: Session = Depends(get_db)):
    return crud.search_books(db, q)

@app.get("/books/{book_id}", response_model=schemas.Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book_in: schemas.BookUpdate, db: Session = Depends(get_db)):
    updated = crud.update_book(db, book_id, book_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_book(db, book_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Book not found")
    return None
