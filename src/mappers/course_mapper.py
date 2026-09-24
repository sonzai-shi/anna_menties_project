from src.models.students import StudentModel
from src.models.courses import CourseModel
from src.schemas.course import (
    CourseSchemaCreate,
    CourseSchemaResponse,
    CourseSchemaPagination
)


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


def to_pagination(courses: list[CourseModel], offset, limit) -> CourseSchemaPagination:
    return CourseSchemaPagination(
        items=[CourseSchemaResponse.model_validate(course) for course in courses],
        offset=offset,
        limit=limit,
    )
