from uuid import UUID

from pydantic import BaseModel, Field, field_validator, ConfigDict
from src.schemas.student import StudentSchemaCreate, StudentSchemaResponse, StudentSchemaUpdate


def not_empty(v: list) -> list:
    if not v:
        raise ValueError(f'Список не должен быть пустым.')
    return v


def strings_not_empty(v: str) -> str | None:
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


class CourseSchemaCreate(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    students: list[StudentSchemaCreate]
    description: str = Field(min_length=1, max_length=1000)
    mentor: str = Field(min_length=1, max_length=150)
    teaching_hours: int | None = Field(default=None, ge=0)

    @field_validator('students')
    @classmethod
    def check_not_empty(cls, v: list) -> list:
        return not_empty(v)

    @field_validator('title', 'description', 'mentor')
    @classmethod
    def check_strings_not_empty(cls, v: str) -> str | None:
        return strings_not_empty(v)

    @field_validator('title', 'mentor')
    @classmethod
    def check_letter_only(cls, v: str) -> str | None:
        return letter_only(v)


class CourseSchemaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    students: list[StudentSchemaResponse]
    description: str
    mentor: str
    teaching_hours: int | None


class CourseSchemaUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=150)
    students: list[StudentSchemaUpdate] | None = Field(default=None)
    description: str | None = Field(default=None, min_length=1, max_length=1000)
    mentor: str | None = Field(default=None, min_length=1, max_length=150)
    teaching_hours: int | None = Field(default=None, ge=0)

    @field_validator('title', 'description', 'mentor')
    @classmethod
    def check_strings_not_empty(cls, v: str) -> str | None:
        return strings_not_empty(v)

    @field_validator('title', 'mentor')
    @classmethod
    def check_letter_only(cls, v: str) -> str | None:
        return letter_only(v)
