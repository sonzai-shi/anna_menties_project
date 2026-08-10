from uuid import UUID
from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import src.service.country_service as country_service
from src.db import get_session
from src.schemas.country import CountrySchemaCreate, CountrySchemaUpdate

router = APIRouter()

@router.post("/country/", status_code=status.HTTP_201_CREATED)
async def post_country(data: CountrySchemaCreate, session: AsyncSession = Depends(get_session)):
    result = await country_service.create_country(data, session)
    return {'result' : result}

@router.get("/country/{id_country}", status_code=status.HTTP_200_OK)
async def get_country(id_country: UUID, session: AsyncSession = Depends(get_session)):
    result = await country_service.find_country(id_country, session)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Country not found'
        )
    return {'result' : result}


@router.get("/country", status_code=status.HTTP_200_OK)
async def get_countries(offset: int, limit: int, session: AsyncSession = Depends(get_session)):
    result = await country_service.find_countries(offset, limit, session)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Country not found'
        )
    return {'result' : result}


@router.put("/country/{id_country}", status_code=status.HTTP_200_OK)
async def put_country(id_country: UUID, data: CountrySchemaUpdate, session: AsyncSession = Depends(get_session)):
    result = await country_service.update_country(id_country, data, session)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Country not found'
        )
    return {'result' : result}

@router.delete("/country/{id_country}", status_code=status.HTTP_204_NO_CONTENT)
async def del_country(id_country: UUID, session: AsyncSession = Depends(get_session)):
    result = await country_service.delete_country(id_country, session)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Country not found'
        )
    return None