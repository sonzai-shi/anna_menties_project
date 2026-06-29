from uuid import UUID

from fastapi import APIRouter
from src.repositories.country_repository import create_country, find_country, update_country, delete_country
from src.schemas.country_schema import CountrySchemaCreate

router = APIRouter()

@router.post("/country/")
async def post_country(data: CountrySchemaCreate):
    country = await create_country(data)
    return {'Сообщение доставлено':'ok',
            'data': country}

@router.get("/country/{id_country}")
async def get_country(id_country: UUID):
    country = await find_country(id_country)
    return {'Результат' : country}

@router.put("/country")
async def put_country(data:CountrySchemaCreate):
    country = await update_country(data)
    return {'Результат' : country}

@router.delete("/country/{id_country}")
async def del_country(id_country: UUID):
    result = await delete_country(id_country)
    return {'Результат' : result}