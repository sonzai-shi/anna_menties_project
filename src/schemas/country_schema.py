from pydantic import BaseModel
from uuid import UUID

from src.schemas.capital_schema import CapitalSchemaCreate


class CountrySchemaCreate(BaseModel):
    country_name: str
    capital: CapitalSchemaCreate

# class CountrySchemaRead(BaseModel):
#     country_name: str
#     id: UUID
#     capital: CapitalSchemaCreate
