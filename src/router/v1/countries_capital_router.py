from uuid import UUID
from fastapi import APIRouter, status, HTTPException
import src.repositories.country_repository as cr
from src.schemas.country import CountrySchemaCreate

router = APIRouter()

@router.post("/country/", status_code=status.HTTP_201_CREATED)
async def post_country(data: CountrySchemaCreate):
    result = await cr.create_country(data)
    return {'Сообщение доставлено':'ok',
            'data': result}

@router.get("/country/{id_country}", status_code=status.HTTP_200_OK)
async def get_country(id_country: UUID):
    result = await cr.find_country(id_country)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Country not found'
        )
    return {'result' : result}

@router.put("/country/{id_country}", status_code=status.HTTP_200_OK)
async def put_country(data:CountrySchemaCreate, id_country: UUID ):
    result = await cr.update_country(data, id_country)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Country not found'
        )
    return {'result' : result}

@router.delete("/country/{id_country}", status_code=status.HTTP_204_NO_CONTENT)
async def del_country(id_country: UUID):
    result = await cr.delete_country(id_country)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Country not found'
        )
    return None