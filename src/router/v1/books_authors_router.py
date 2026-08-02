from uuid import UUID
from fastapi import APIRouter, status, HTTPException
from src.schemas.book import BookSchemaCreate, BookSchemaUpdate
import src.repositories.book_repository as br

router = APIRouter()

@router.post('/books', status_code=status.HTTP_201_CREATED)
async def post_books(data: BookSchemaCreate):
    result = await br.post_books(data)
    return {'result': result}

@router.get('/books/{book_id}', status_code=status.HTTP_200_OK)
async def get_book(book_id: UUID):
    result = await br.get_book(book_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Book not found'
        )
    return {'result': result}

@router.put('/books/{book_id}', status_code=status.HTTP_200_OK)
async def put_book(book_id: UUID, data: BookSchemaUpdate):
    result = await br.put_book(book_id, data)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Book not found'
        )
    return {'result': result}

@router.delete('/books/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: UUID):
    result = await br.delete_book(book_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Book not found'
        )
    return None