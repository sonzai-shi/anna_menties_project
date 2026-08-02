from uuid import UUID
from fastapi import APIRouter
from src.schemas.book import BookSchemaCreate, BookSchemaUpdate
import src.repositories.book_repository as br

router = APIRouter()

@router.post('/books')
async def post_books(data: BookSchemaCreate):
    result = await br.post_books(data)
    return {'result': result}

@router.get('/books/{book_id}')
async def get_book(book_id: UUID):
    book = await br.get_book(book_id)
    return {'result': book}

@router.put('/books/{book_id}')
async def put_book(book_id: UUID, data: BookSchemaUpdate):
    result = await br.put_book(book_id, data)
    return {'result': result}

@router.delete('/books/{book_id}')
async def delete_book(book_id: UUID):
    result = await br.delete_book(book_id)
    return {'result': result}