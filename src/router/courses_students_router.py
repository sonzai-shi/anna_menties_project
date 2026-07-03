from unittest import result
from uuid import UUID
from fastapi import APIRouter
from src.schemas.course_schema import CourseSchemaCreate, CourseSchemaUpdate
import src.repositories.corse_repository as cr

router = APIRouter()

@router.post("/course/")
async def post_course(data: CourseSchemaCreate):
    result = await cr.post_course(data)
    return {'result': result}

@router.get("/course/{course_id}")
async def get_course(course_id: UUID):
    course = await cr.get_course(course_id)
    return {'result': course}

@router.put("/course/{course_id}")
async def put_course(course_id: UUID, data: CourseSchemaUpdate):
    course = await cr.put_course(course_id, data)
    return {'result': course}

@router.delete("/course/{course_id}")
async def delete_course(course_id: UUID):
    result = await cr.delete_course(course_id)
    return {'result': result}