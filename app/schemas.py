# app/schemas.py
from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional

class BookBase(BaseModel):
    title: str = Field(..., description="Título del libro (obligatorio, no vacío)")
    author: str = Field(..., description="Autor del libro (obligatorio, no vacío)")
    year: Optional[int] = Field(None, ge=0, le=9999, description="Año de publicación (no puede ser negativo)")
    isbn: Optional[str] = Field(None, description="Código ISBN (solo números)")

    # 🔍 Validar que el título no esté vacío o con solo espacios
    @field_validator("title")
    @classmethod
    def validate_title(cls, v):
        if not v or not v.strip():
            raise ValueError("El título no puede estar vacío")
        return v

    # 🔍 Validar que el autor no esté vacío o con solo espacios
    @field_validator("author")
    @classmethod
    def validate_author(cls, v):
        if not v or not v.strip():
            raise ValueError("El autor no puede estar vacío")
        return v

    # 🔍 Validar que el ISBN solo contenga números
    @field_validator("isbn")
    @classmethod
    def validate_isbn(cls, v):
        if v is not None and not v.isdigit():
            raise ValueError("El ISBN solo puede contener números")
        return v


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = Field(None, ge=0, le=9999)
    isbn: Optional[str] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, v):
        if v is not None and not v.strip():
            raise ValueError("El título no puede estar vacío")
        return v

    @field_validator("author")
    @classmethod
    def validate_author(cls, v):
        if v is not None and not v.strip():
            raise ValueError("El autor no puede estar vacío")
        return v

    @field_validator("isbn")
    @classmethod
    def validate_isbn(cls, v):
        if v is not None and not v.isdigit():
            raise ValueError("El ISBN solo puede contener números")
        return v


class Book(BookBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
