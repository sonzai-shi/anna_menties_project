from uuid import UUID
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from src.db import get_session
from src.models.students import StudentModel
from src.models.courses import CourseModel
from src.schemas.course import CourseSchemaCreate, CourseSchemaUpdate


async def post_course(course_data: CourseSchemaCreate):
    async with get_session() as session:
        db_course = CourseModel(title=course_data.title)
        db_course.students = [
            StudentModel(name=student.name)
            for student in course_data.students
        ]

        session.add(db_course)
        await session.flush()

        return {
            'id': db_course.id,
            'title': db_course.title,
            'students': [
                {'id': student.id, 'name': student.name}
                for student in db_course.students
            ],
        }

async def get_course(course_id: UUID):
    async with get_session() as session:
        course = await _find(session, course_id)
        if  course is None:
            return None
        return {
            'id': course.id,
            'title': course.title,
            'students': [
                {'id': student.id, 'name': student.name}
                for student in course.students
            ],
        }

async def put_course(course_id: UUID, course_data: CourseSchemaUpdate):
    async with get_session() as session:
        db_course = await _find(session, course_id)
        if db_course is None:
            return None

        db_course.title = course_data.title
        id_students = {s.id: s for s in db_course.students}

        for student_data in course_data.students:
            student = id_students.get(student_data.id)
            if student is None:
                continue
            student.name = student_data.name

        await session.flush()

        return {
            'id': db_course.id,
            'title': db_course.title,
            'students': [
                {'id': student.id, 'name': student.name}
                for student in db_course.students
            ],
        }


async def delete_course(course_id: UUID):
    async with get_session() as session:
        course = await _find(session, course_id)
        if course is None:
            return None
        course.is_deleted = True
        for student in course.students:
            student.is_deleted = True
        return True


async def _find(session, country_id: UUID):
    query = (
        select(CourseModel)
        .where(CourseModel.id == country_id)
        .where(CourseModel.is_deleted == False)
        .options(selectinload(CourseModel.students))
    )
    result = await session.execute(query)
    return result.scalar_one_or_none()








