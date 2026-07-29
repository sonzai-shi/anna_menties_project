from uuid import UUID

from pydantic import BaseModel, Field, field_validator
from src.schemas.student import StudentSchemaCreate, StudentSchemaUpdate


class CourseSchemaCreate(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    students: list[StudentSchemaCreate]
    description: str = Field(min_length=1, max_length=1000)
    mentor: str = Field(min_length=1, max_length=150)
    teaching_hours: int | None = Field(ge=0)

    @field_validator('students')
    @classmethod
    def not_empty(cls, v: list) -> list:
        if not v:
            raise ValueError(f'Список не должен быть пустым.')
        return v

    @field_validator('title', 'description', 'mentor')
    @classmethod
    def not_empty(cls, v: str) -> str | None:
        if v is None:
            return v
        if not v.replace(' ', ''):
            raise ValueError('Строка не может быть пустой.')
        return v

    @field_validator('title', 'mentor')
    @classmethod
    def letter_only(cls, v: str) -> str | None:
        if v is None:
            return v
        if not v.replace(' ', '').isalpha():
            raise ValueError('Используйте только буквы.')
        return v


class CourseSchemaUpdate(CourseSchemaCreate):
    id: UUID