from uuid import UUID

from pydantic import BaseModel

class StudentSchemaCreate(BaseModel):
    name: str

class StudentSchemaUpdate(BaseModel):
    id: UUID
    name: str