from pydantic import BaseModel
from src.schemas.capital_schema import CapitalSchemaCreate


class CountrySchemaCreate(BaseModel):
    country_name: str
    capital: CapitalSchemaCreate

