from uuid import UUID

from pydantic import BaseModel
from src.schemas.author import AuthorSchemaCreate, AuthorSchemaUpdate


class BookSchemaCreate(BaseModel):
    title: str
    authors: list[AuthorSchemaCreate]

class BookSchemaUpdate(BaseModel):
        id: UUID
        title: str
        authors: list[AuthorSchemaUpdate]

