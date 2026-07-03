from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from src.router.healthcheck import router as healthcheck_router
from src.router.countries_capital_router import router as cc_router
from src.router.courses_students_router import router as sc_router
from src.router.books_authors_router import router as bs_router


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
    app.include_router(cc_router)
    app.include_router(sc_router)
    app.include_router(bs_router)
    return app
