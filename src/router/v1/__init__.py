from fastapi import APIRouter
from .courses_students_router import router as cs_router
from .books_authors_router import router as ba_router
from .countries_capital_router import router as cc_router

v1_router = APIRouter()
v1_router.include_router(cs_router, prefix="/v1")
v1_router.include_router(ba_router, prefix="/v1")
v1_router.include_router(cc_router, prefix="/v1")

