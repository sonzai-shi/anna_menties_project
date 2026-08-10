from uuid import UUID
from pydantic import BaseModel, Field, field_validator, ConfigDict
from src.schemas.capital import CapitalSchemaResponse, CapitalSchemaCreate, CapitalSchemaUpdate


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


class CountrySchemaCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    capital: CapitalSchemaCreate
    president: str = Field(min_length=1, max_length=100)
    population: int = Field(ge= 0)
    currency: str | None = Field(default=None, min_length=1, max_length=100)

    @field_validator('name', 'president', 'currency')
    @classmethod
    def check_letter_only(cls, v: str) -> str | None:
        return letter_only(v)

    @field_validator('name', 'president', 'currency')
    @classmethod
    def check_not_empty(cls, v: str) -> str | None:
        return not_empty(v)


class CountrySchemaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    capital: CapitalSchemaResponse
    president: str
    population: int
    currency: str | None


class CountrySchemaUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=50)
    capital: CapitalSchemaUpdate | None = Field(default=None)
    president: str | None = Field(default=None, min_length=1, max_length=100)
    population: int | None = Field(default=None, ge=0)
    currency: str | None = Field(default=None, min_length=1, max_length=100)

    @field_validator('name', 'president', 'currency')
    @classmethod
    def check_letter_only(cls, v: str) -> str | None:
        return letter_only(v)

    @field_validator('name', 'president', 'currency')
    @classmethod
    def check_not_empty(cls, v: str) -> str | None:
        return not_empty(v)


class CountrySchemaPagination(BaseModel):
    items: list[CountrySchemaResponse]
    offset: int
    limit: int