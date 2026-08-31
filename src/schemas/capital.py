from uuid import UUID
from pydantic import BaseModel, Field, field_validator, ConfigDict
import src.schemas.base as base


class CapitalSchemaCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    mayor: str | None = Field(default=None, min_length=1, max_length=100)
    population: int = Field(ge=0)

    @field_validator('name', 'mayor')
    @classmethod
    def check_letter_only(cls, value: str) -> str | None:
        return base.letter_only_str(value)

    @field_validator('name', 'mayor')
    @classmethod
    def check_not_empty(cls, value: str) -> str | None:
        return base.not_empty_str(value)


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
    def check_letter_only(cls, value: str) -> str | None:
        return base.letter_only_str(value)

    @field_validator('name', 'mayor')
    @classmethod
    def check_not_empty(cls, value: str) -> str | None:
        return base.not_empty_str(value)