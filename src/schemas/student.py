from uuid import UUID

from pydantic import BaseModel, Field, field_validator, ConfigDict


def not_empty(v: str) -> str | None:
    if v is None:
        return v
    if not v.replace(' ', ''):
        raise ValueError('Строка не может быть пустой.')
    return v

def letter_only(v: str) -> str | None:
    if v is None:
        return v
    if not v.replace(' ', '').isalpha():
        raise ValueError('Используйте только буквы.')
    return v

class StudentSchemaCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    age: int = Field(ge= 0)
    dormitory: str | None = Field(default=None, min_length=2, max_length=150)
    citizenship: str = Field(min_length=2, max_length=150)

    @field_validator('name', 'dormitory', 'citizenship')
    @classmethod
    def check_not_empty(cls, v: str) -> str | None:
        return not_empty(v)

    @field_validator('name',  'citizenship')
    @classmethod
    def check_letter_only(cls, v: str) -> str | None:
        return letter_only(v)


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
    def check_not_empty(cls, v: str) -> str | None:
        return not_empty(v)

    @field_validator('name',  'citizenship')
    @classmethod
    def check_letter_only(cls, v: str) -> str | None:
        return letter_only(v)