from uuid import UUID
from pydantic import BaseModel, Field, field_validator, ConfigDict


def letter_only(v: str) -> str | None:
    if v is None:
        return v
    if not v.replace(' ', '').isalpha():
        raise ValueError('Используйте только буквы.')
    return v

def not_empty(v: str) -> str | None:
    if v is None:
        return v
    if not v.replace(' ', ''):
        raise ValueError('Строка не может быть пустой.')
    return v


class AuthorSchemaCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    age: int = Field(ge=0)
    location: str | None = Field(default=None, min_length=2, max_length=150)
    citizenship: str | None = Field(default=None, min_length=2, max_length=150)

    @field_validator('name', 'location', 'citizenship')
    @classmethod
    def check_letter_only(cls, v: str) -> str | None:
        return letter_only(v)

    @field_validator('name', 'location', 'citizenship')
    @classmethod
    def check_not_empty(cls, v: str) -> str | None:
        return not_empty(v)


class AuthorSchemaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    age: int
    location: str | None
    citizenship: str | None


class AuthorSchemaUpdate(BaseModel):
    id: UUID
    name: str | None = Field(default=None, min_length=2, max_length=50)
    age: int | None = Field(default=None, ge=0)
    location: str | None = Field(default=None, min_length=2, max_length=150)
    citizenship: str | None = Field(default=None, min_length=2, max_length=150)

    @field_validator('name', 'location', 'citizenship')
    @classmethod
    def check_letter_only(cls, v: str) -> str | None:
        return letter_only(v)

    @field_validator('name', 'location', 'citizenship')
    @classmethod
    def check_not_empty(cls, v: str) -> str | None:
        return not_empty(v)
