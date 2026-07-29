from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class AuthorSchemaCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    age: int = Field(ge=0)
    location: str | None = Field(min_length=2, max_length=150)
    citizenship: str | None = Field(min_length=2, max_length=150)

    @field_validator('name', 'location', 'citizenship')
    @classmethod
    def letter_only(cls, v: str) -> str | None:
        if v is None:
            return v
        if not v.replace(' ', '').isalpha():
            raise ValueError('Используйте только буквы.')
        return v

    @field_validator('name', 'location', 'citizenship')
    @classmethod
    def not_empty(cls, v: str) -> str | None:
        if v is None:
            return v
        if not v.replace(' ', ''):
            raise ValueError('Строка не может быть пустой.')
        return v


class AuthorSchemaUpdate(AuthorSchemaCreate):
    id: UUID