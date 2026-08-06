from datetime import date
from typing import Annotated
from uuid import UUID
from pydantic import BaseModel, field_validator, Field, ConfigDict
from src.schemas.author import AuthorSchemaCreate, AuthorSchemaResponse, AuthorSchemaUpdate


def not_empty(v: list) -> list:
    if not v:
        raise ValueError(f'Список не должен быть пустым.')
    return v


def strings_not_empty(v):
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

def letter_only(v: list[str]) -> list[str] | None:
    if v is None:
        return v
    for genre in v:
        if not genre.replace(' ', '').isalpha():
            raise ValueError(f'Используйте только буквы.')
    return v


class BookSchemaCreate(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    description: str = Field(min_length=1, max_length=1000)
    genre: list[Annotated[str, Field(max_length=150)]] = Field(min_length=1)
    date_written: date = Field(le=date.today())
    authors: list[AuthorSchemaCreate]

    @field_validator('authors')
    @classmethod
    def check_not_empty(cls, v: list)-> list:
        return not_empty(v)

    @field_validator('genre', 'description', 'title')
    @classmethod
    def check_strings_not_empty(cls, v):
        return strings_not_empty(v)

    @field_validator('genre')
    @classmethod
    def check_letter_only(cls, v: list[str]) -> list[str] | None:
        return letter_only(v)


class BookSchemaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str
    genre: list[Annotated[str, Field(max_length=150)]]
    date_written: date
    authors: list[AuthorSchemaResponse]


class BookSchemaUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = Field(default=None, min_length=1, max_length=1000)
    genre: list[Annotated[str, Field(max_length=150)]] | None = Field(default=None, min_length=1)
    date_written: date | None = Field(default=None, le=date.today())
    authors: list[AuthorSchemaUpdate] | None = Field(default=None)

    @field_validator('genre', 'description', 'title')
    @classmethod
    def check_strings_not_empty(cls, v):
        return strings_not_empty(v)

    @field_validator('genre')
    @classmethod
    def check_letter_only(cls, v: list[str]) -> list[str] | None:
        return letter_only(v)
