from sqlalchemy.ext.asyncio import AsyncSession
from src.service.book_service import BookService
from src.db import get_session, get_read_session
from fastapi import Depends


def get_book_read_service(session: AsyncSession = Depends(get_read_session)) -> BookService:
    return BookService(session)


def get_book_write_service(session: AsyncSession = Depends(get_session)) -> BookService:
    return BookService(session)
