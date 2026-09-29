from uuid import UUID
import src.schemas.base as base
from pydantic import BaseModel, Field, field_validator, ConfigDict


class StudentSchemaCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    age: int = Field(ge= 0)
    dormitory: str | None = Field(default=None, min_length=2, max_length=150)
    citizenship: str = Field(min_length=2, max_length=150)

    @field_validator('name', 'dormitory', 'citizenship')
    @classmethod
    def check_not_empty(cls, value: str) -> str | None:
        return base.not_empty_str(value)

    @field_validator('name',  'citizenship')
    @classmethod
    def check_letter_only(cls, value: str) -> str | None:
        return base.letter_only_str(value)


class StudentSchemaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    age: int
    dormitory: str | None
    citizenship: str


class StudentSchemaUpdate(BaseModel):
    id : UUID
    name: str | None = Field(default=None, min_length=2, max_length=50)
    age: int | None = Field(default=None, ge= 0)
    dormitory: str | None = Field(default=None, min_length=2, max_length=150)
    citizenship: str | None = Field(default=None, min_length=2, max_length=150)

    @field_validator('name', 'dormitory', 'citizenship')
    @classmethod
    def check_not_empty(cls, value: str) -> str | None:
        return base.not_empty_str(value)

    @field_validator('name',  'citizenship')
    @classmethod
    def check_letter_only(cls, value: str) -> str | None:
        return base.letter_only_str(value)