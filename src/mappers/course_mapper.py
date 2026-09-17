from src.models.students import StudentModel
from src.models.courses import CourseModel
from src.schemas.course import (
    CourseSchemaCreate,
    CourseSchemaResponse,
    CourseSchemaUpdate,
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

def update_course(course: CourseModel, data: CourseSchemaUpdate ) -> None:
    update_data = data.model_dump(exclude_unset=True)
    students_data = update_data.pop('students', None)

    for field, value in update_data.items():
        setattr(course, field, value)

    if students_data is not None:
        students_id = {student.id: student for student in course.students}

        for student_data in students_data:
            student = students_id.get(student_data['id'])
            for field, value in student_data.items():
                if field != 'id':
                    setattr(student, field, value)