from datetime import date
from typing import Annotated
from uuid import UUID
from pydantic import BaseModel, field_validator, Field
from src.schemas.author import AuthorSchemaCreate, AuthorSchemaUpdate


class BookSchemaCreate(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    description: str = Field(min_length=1, max_length=1000)
    genre: list[Annotated[str, Field(max_length=150)]] | None = Field(min_length=1)
    date_written: date = Field(le=date.today())
    authors: list[AuthorSchemaCreate]

    @field_validator('authors')
    @classmethod
    def not_empty(cls, v: list) -> list:
        if not v:
            raise ValueError(f'Список не должен быть пустым.')
        return v

    @field_validator('genre', 'description', 'title')
    @classmethod
    def not_empty(cls, v):
        if v is None:
            return v
        if isinstance(v, list):
            if not v:
                raise ValueError(f'Список не должен быть пустым.')
            for i in v:
                if not i.replace(' ', ''):
                    raise ValueError(f'Строка в списке не должна быть пустой.')
        if isinstance(v, str):
            if not v.replace(' ', ''):
                raise ValueError(f'Строка не должна быть пустой.')
        return v


    @field_validator('genre')
    @classmethod
    def letter_only(cls, v: list[str]) -> list[str] | None:
        if v is None:
            return v
        for genre in v:
            if not genre.replace(' ', '').isalpha():
                raise ValueError(f'Используйте только буквы.')
        return v


class BookSchemaUpdate(BookSchemaCreate):
    id: UUID

