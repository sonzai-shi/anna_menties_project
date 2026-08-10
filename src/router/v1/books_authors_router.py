from uuid import UUID
from fastapi import APIRouter, status, HTTPException, Depends
from src.db import get_session
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.book import BookSchemaCreate, BookSchemaUpdate
import src.service.book_service as book_service

router = APIRouter()

@router.post('/books', status_code=status.HTTP_201_CREATED)
async def post_books(data: BookSchemaCreate, session: AsyncSession = Depends(get_session)):
    result = await book_service.post_books(data, session)
    return {'result': result}

@router.get('/books/{book_id}', status_code=status.HTTP_200_OK)
async def get_book(book_id: UUID, session: AsyncSession = Depends(get_session)):
    result = await book_service.get_book(book_id, session)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Book not found'
        )
    return {'result': result}


@router.get('/books', status_code=status.HTTP_200_OK)
async def get_books(offset: int, limit: int, session: AsyncSession = Depends(get_session)):
    result = await book_service.get_books(offset, limit, session)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Book not found'
        )
    return {'result': result}


@router.put('/books/{book_id}', status_code=status.HTTP_200_OK)
async def put_book(book_id: UUID, data: BookSchemaUpdate, session: AsyncSession = Depends(get_session)):
    result = await book_service.put_book(book_id, data, session)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Book not found'
        )
    return {'result': result}

@router.delete('/books/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: UUID, session: AsyncSession = Depends(get_session)):
    result = await book_service.delete_book(book_id, session)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Book not found'
        )
    return None