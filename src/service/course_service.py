from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.students import StudentModel
from src.models.courses import CourseModel
from src.schemas.course import CourseSchemaCreate, CourseSchemaResponse, CourseSchemaUpdate
import src.repositories.course_repository as course_repo


async def post_course(course_data: CourseSchemaCreate, session: AsyncSession):
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
    result = await course_repo.create(session, course)
    return CourseSchemaResponse.model_validate(result)


async def get_course(course_id: UUID, session: AsyncSession):
    result = await course_repo.find_course(session, course_id)
    if  result is None:
        return None
    return CourseSchemaResponse.model_validate(result)


async def put_course(course_id: UUID, data: CourseSchemaUpdate, session: AsyncSession):
    course = await course_repo.find_course(session, course_id)
    if course is None:
        return None

    if data.title is not None:
        course.title = data.title
    if data.description is not None:
        course.description = data.description
    if data.mentor is not None:
        course.mentor = data.mentor
    if data.teaching_hours is not None:
        course.teaching_hours = data.teaching_hours

    if data.students is not None:
        students_by_id = {s.id: s for s in course.students}

        for student_data in data.students:
            student = students_by_id.get(student_data.id)
            if student is None:
                continue
            if student_data.name is not None:
                student.name = student_data.name
            if student_data.age is not None:
                student.age = student_data.age
            if student_data.dormitory is not None:
                student.dormitory = student_data.dormitory
            if student_data.citizenship is not None:
                student.citizenship = student_data.citizenship

    return CourseSchemaResponse.model_validate(course)


async def delete_course(course_id: UUID, session: AsyncSession):
    result = await course_repo.find_course(session, course_id)
    if result is None:
        return None
    result.is_deleted = True
    for student in result.students:
        student.is_deleted = True
    return True