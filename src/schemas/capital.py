from uuid import UUID
from pydantic import BaseModel, Field, field_validator, ConfigDict


def letter_only(v: str) -> str | None:
    if v is None:
        return v
    if not v.replace(' ', '').replace('-', '').isalpha():
        raise ValueError('Используйте только буквы.')
    return v


def not_empty(v: str) -> str | None:
    if v is None:
        return v
    if not v.replace(' ', ''):
        raise ValueError('Строка не может быть пустой.')
    return v


class CapitalSchemaCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    mayor: str | None = Field(default=None, min_length=1, max_length=100)
    population: int = Field(ge=0)

    @field_validator('name', 'mayor')
    @classmethod
    def check_letter_only(cls, v: str) -> str | None:
        return letter_only(v)

    @field_validator('name', 'mayor')
    @classmethod
    def check_not_empty(cls, v: str) -> str | None:
        return not_empty(v)


class CapitalSchemaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    mayor: str | None
    population: int


class CapitalSchemaUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=50)
    mayor: str | None = Field(default=None, min_length=1, max_length=100)
    population: int | None = Field(default=None, ge=0)

    @field_validator('name', 'mayor')
    @classmethod
    def check_letter_only(cls, v: str) -> str | None:
        return letter_only(v)

    @field_validator('name', 'mayor')
    @classmethod
    def check_not_empty(cls, v: str) -> str | None:
        return not_empty(v)