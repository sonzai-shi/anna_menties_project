from pydantic import BaseModel


class CapitalSchemaCreate(BaseModel):
    capital_name: str

