from contextlib import asynccontextmanager
from email.utils import rfc2231_continuation

from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from redis.asyncio import Redis
from src.config import settings
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


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_client = Redis.from_url(
        settings.redis_url,
        decode_responses=True
    )
    app.state.redis_client = redis_client
    try:
        yield
    finally:
        await redis_client.aclose()


def get_app() -> FastAPI:
    app = FastAPI(
        docs_url='/docs',
        openapi_url='/openapi.json',
        default_response_class=JSONResponse,
        lifespan=lifespan,
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
