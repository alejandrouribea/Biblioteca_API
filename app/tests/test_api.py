# app/tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal
from app import models

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Crea las tablas antes de ejecutar las pruebas y limpia después."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield
    db.query(models.Book).delete()
    db.commit()
    db.close()


def test_create_book():
    """Prueba la creación de un libro."""
    data = {
        "title": "Crónica de una muerte anunciada",
        "author": "Gabriel García Márquez",
        "year": 1981,
        "isbn": "9780307388940"
    }
    response = client.post("/books/", json=data)
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == data["title"]
    assert body["author"] == data["author"]
    assert "id" in body


def test_get_books():
    """Verifica que el libro creado se liste correctamente."""
    response = client.get("/books/")
    assert response.status_code == 200
    books = response.json()
    assert isinstance(books, list)
    assert any(b["title"] == "Crónica de una muerte anunciada" for b in books)


def test_update_book():
    """Prueba la actualización (PUT) de un libro existente."""
    # obtener id del primer libro
    books = client.get("/books/").json()
    book_id = books[0]["id"]

    update_data = {"year": 1982}
    response = client.put(f"/books/{book_id}", json=update_data)
    assert response.status_code == 200
    updated = response.json()
    assert updated["year"] == 1982


def test_delete_book():
    """Prueba la eliminación (DELETE) de un libro."""
    # obtener id del primer libro
    books = client.get("/books/").json()
    book_id = books[0]["id"]

    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 204

    # verificar que ya no exista
    response_check = client.get(f"/books/{book_id}")
    assert response_check.status_code == 404


def test_search_books():
    """Crea otro libro y verifica búsqueda por autor."""
    data = {
        "title": "El amor en los tiempos del cólera",
        "author": "Gabriel García Márquez",
        "year": 1985,
        "isbn": "9780307389732"
    }
    client.post("/books/", json=data)

    response = client.get("/books/search/?q=García")
    assert response.status_code == 200
    results = response.json()
    assert len(results) > 0
    assert any("García" in b["author"] for b in results)
