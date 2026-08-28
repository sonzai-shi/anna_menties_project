from uuid import UUID
from fastapi import APIRouter, status, HTTPException, Depends
from src.db import get_session
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.book import BookSchemaCreate, BookSchemaUpdate
from src.service.book_service import BookService

router = APIRouter(prefix='/book')

@router.post(path='', status_code=status.HTTP_201_CREATED)
async def create_books(data: BookSchemaCreate, session: AsyncSession = Depends(get_session)):
    book_service = BookService(session)
    result = await book_service.create_books(data)
    return result

@router.get('/{book_id}')
async def read_book(book_id: UUID, session: AsyncSession = Depends(get_session)):
    book_service = BookService(session)
    result = await book_service.read_book(book_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Book not found'
        )
    return result


@router.get(path='')
async def read_books(offset: int, limit: int, session: AsyncSession = Depends(get_session)):
    book_service = BookService(session)
    result = await book_service.read_books(offset, limit)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Book not found'
        )
    return result


@router.put('/{book_id}')
async def update_book(book_id: UUID, data: BookSchemaUpdate, session: AsyncSession = Depends(get_session)):
    book_service = BookService(session)
    result = await book_service.update_book(book_id, data)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Book not found'
        )
    return result

@router.delete('/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: UUID, session: AsyncSession = Depends(get_session)):
    book_service = BookService(session)
    result = await book_service.delete_book(book_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Book not found'
        )
    return None