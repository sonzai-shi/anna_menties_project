from uuid import UUID
import src.schemas.base as base
from pydantic import BaseModel, Field, field_validator, ConfigDict
from src.schemas.student import StudentSchemaCreate, StudentSchemaResponse, StudentSchemaUpdate


class CourseSchemaCreate(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    students: list[StudentSchemaCreate]
    description: str = Field(min_length=1, max_length=1000)
    mentor: str = Field(min_length=1, max_length=150)
    teaching_hours: int | None = Field(default=None, ge=0)

    @field_validator('students')
    @classmethod
    def check_not_empty(cls, value: list) -> list | None:
        return base.not_empty_list(value)

    @field_validator('title', 'description', 'mentor')
    @classmethod
    def check_strings_not_empty(cls, value: str) -> str | None:
        return base.not_empty_str(value)

    @field_validator('title', 'mentor')
    @classmethod
    def check_letter_only(cls, value: str) -> str | None:
        return base.letter_only_str(value)


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
    def check_strings_not_empty(cls, value: str) -> str | None:
        return base.not_empty_str(value)

    @field_validator('title', 'mentor')
    @classmethod
    def check_letter_only(cls, value: str) -> str | None:
        return base.letter_only_str(value)


class CourseSchemaPagination(BaseModel):
    items: list[CourseSchemaResponse]
    offset: int
    limit: int