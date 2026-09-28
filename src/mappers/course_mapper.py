from src.models.students import StudentModel
from src.models.courses import CourseModel
from src.schemas.course import (
    CourseSchemaCreate,
    CourseSchemaResponse,
    CourseSchemaPagination
)
from datetime import datetime
from uuid import UUID


def to_model(course_data: CourseSchemaCreate) -> CourseModel:
    course = CourseModel(
        title=course_data.title,
        description=course_data.description,
        mentor=course_data.mentor,
        teaching_hours=course_data.teaching_hours,
    )
    course.students = [
        StudentModel(
            name=student.name,
            age=student.age,
            dormitory=student.dormitory,
            citizenship=student.citizenship,
        )
        for student in course_data.students
    ]
    return course


def to_pagination(
        courses: list[CourseModel],
        limit: int,
        next_cursor_created_at: datetime | None,
        next_cursor_id: UUID | None,
) -> CourseSchemaPagination:
    return CourseSchemaPagination(
        items=[CourseSchemaResponse.model_validate(course) for course in courses],
        limit=limit,
        next_cursor_created_at=next_cursor_created_at,
        next_cursor_id=next_cursor_id,
    )
