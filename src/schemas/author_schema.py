from uuid import UUID

from pydantic import BaseModel


class AuthorSchemaCreate(BaseModel):
    name: str

class AuthorSchemaUpdate(BaseModel):
    id: UUID
    name: str