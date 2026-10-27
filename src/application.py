from email.utils import rfc2231_continuation
from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from src.router.healthcheck import router as healthcheck_router

from src.router.v1.books_authors_router import router as ba_router
from src.router.v1.countries_capital_router import router as cc_router
from src.router.v1.courses_students_router import router as cs_router

def get_v1_router() -> APIRouter:
    v1_router = APIRouter()
    v1_router.include_router(cs_router, prefix="/v1")
    v1_router.include_router(ba_router, prefix="/v1")
    v1_router.include_router(cc_router, prefix="/v1")
    return v1_router


def get_app() -> FastAPI:
    app = FastAPI(
        docs_url='/docs',
        openapi_url='/openapi.json',
        default_response_class=JSONResponse,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    app.include_router(healthcheck_router)
    app.include_router(get_v1_router())
    return app
