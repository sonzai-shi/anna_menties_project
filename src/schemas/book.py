from datetime import date
from typing import Annotated
from uuid import UUID
from pydantic import BaseModel, field_validator, Field, ConfigDict
from src.schemas.author import AuthorSchemaCreate, AuthorSchemaResponse, AuthorSchemaUpdate
import src.schemas.base as base


class BookSchemaCreate(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    description: str = Field(min_length=1, max_length=1000)
    genre: list[Annotated[str, Field(max_length=150)]] = Field(min_length=1)
    date_written: date = Field(le=date.today())
    authors: list[AuthorSchemaCreate]

    @field_validator('authors', 'genre')
    @classmethod
    def check_not_empty_list(cls, value: list)-> list | None:
        return base.not_empty_list(value)

    @field_validator( 'description', 'title')
    @classmethod
    def check__not_empty_str(cls, value: str)-> str | None:
        return base.not_empty_str(value)

    @field_validator('genre')
    @classmethod
    def check_letter_only(cls, value: list[str]) -> list[str] | None:
        return base.letter_only_list(value)


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

    @field_validator('authors', 'genre')
    @classmethod
    def check_not_empty_list(cls, value: list) -> list | None:
        return base.not_empty_list(value)

    @field_validator('description', 'title')
    @classmethod
    def check_not_empty_str(cls, value: str) -> str | None:
        return base.not_empty_str(value)

    @field_validator('genre')
    @classmethod
    def check_letter_only(cls, value: list[str]) -> list[str] | None:
        return base.letter_only_list(value)


class BookSchemaPagination(BaseModel):
    items: list[BookSchemaResponse]
    offset: int
    limit: int
