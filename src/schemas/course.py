from pydantic import BaseModel
from src.schemas.student import StudentSchemaCreate, StudentSchemaUpdate


class CourseSchemaCreate(BaseModel):
    title: str
    students: list[StudentSchemaCreate]

class CourseSchemaUpdate(BaseModel):
    title: str
    students: list[StudentSchemaUpdate]