from uuid import UUID
from pydantic import BaseModel, Field, field_validator, ConfigDict
import src.schemas.base as base

class AuthorSchemaCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    age: int = Field(ge=0)
    location: str | None = Field(default=None, min_length=2, max_length=150)
    citizenship: str | None = Field(default=None, min_length=2, max_length=150)

    @field_validator('name', 'location', 'citizenship')
    @classmethod
    def check_letter_only(cls, value: str) -> str | None:
        return base.letter_only_str(value)

    @field_validator('name', 'location', 'citizenship')
    @classmethod
    def check_not_empty(cls, value: str) -> str | None:
        return base.not_empty_str(value)


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
    def check_letter_only(cls, value: str) -> str | None:
        return base.letter_only_str(value)

    @field_validator('name', 'location', 'citizenship')
    @classmethod
    def check_not_empty(cls, value: str) -> str | None:
        return base.not_empty_str(value)
