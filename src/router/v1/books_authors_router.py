from uuid import UUID
from fastapi import APIRouter, status, Depends
from src.schemas.book import BookSchemaCreate, BookSchemaUpdate
from src.service.book_service import BookService
from src.dependencies.book import get_book_read_service, get_book_write_service

router = APIRouter(prefix='/book')


@router.post(path='', status_code=status.HTTP_201_CREATED)
async def create_books(
        data: BookSchemaCreate,
        book_service: BookService = Depends(get_book_write_service),
):
    return await book_service.create_books(data)


@router.get('/{book_id}')
async def read_book(
        book_id: UUID,
        book_service: BookService = Depends(get_book_read_service),
):
    return await book_service.read_book(book_id)


@router.get(path='')
async def read_books(
        offset: int,
        limit: int,
        book_service: BookService = Depends(get_book_read_service),
):
    return await book_service.read_books(offset, limit)


@router.put('/{book_id}')
async def update_book(
        book_id: UUID,
        data: BookSchemaUpdate,
        book_service: BookService = Depends(get_book_write_service),
):
    return await book_service.update_book(book_id, data)


@router.delete('/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
        book_id: UUID,
        book_service: BookService = Depends(get_book_write_service),
):
    await book_service.delete_book(book_id)
    return None
