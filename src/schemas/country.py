from uuid import UUID
from pydantic import BaseModel, Field, field_validator, ConfigDict
from src.schemas.capital import CapitalSchemaResponse, CapitalSchemaCreate, CapitalSchemaUpdate
import src.schemas.base as base


class CountrySchemaCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    capital: CapitalSchemaCreate
    president: str = Field(min_length=1, max_length=100)
    population: int = Field(ge= 0)
    currency: str | None = Field(default=None, min_length=1, max_length=100)

    @field_validator('name', 'president', 'currency')
    @classmethod
    def check_letter_only(cls, value: str) -> str | None:
        return base.letter_only_str(value)

    @field_validator('name', 'president', 'currency')
    @classmethod
    def check_not_empty(cls, value: str) -> str | None:
        return base.not_empty_str(value)


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
    def check_letter_only(cls, value: str) -> str | None:
        return base.letter_only_str(value)

    @field_validator('name', 'president', 'currency')
    @classmethod
    def check_not_empty(cls, value: str) -> str | None:
        return base.not_empty_str(value)


class CountrySchemaPagination(BaseModel):
    items: list[CountrySchemaResponse]
    offset: int
    limit: int