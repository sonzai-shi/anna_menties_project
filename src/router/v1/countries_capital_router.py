from uuid import UUID
from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.service.country_service import CountryService
from src.db import get_session
from src.schemas.country import CountrySchemaCreate, CountrySchemaUpdate

router = APIRouter(prefix="/country")

@router.post("", status_code=status.HTTP_201_CREATED)
async def post_country(data: CountrySchemaCreate, session: AsyncSession = Depends(get_session)):
    country_service = CountryService(session)
    result = await country_service.create_country(data)
    return {'result' : result}

@router.get("/{id_country}")
async def get_country(id_country: UUID, session: AsyncSession = Depends(get_session)):
    country_service = CountryService(session)
    result = await country_service.read_country(id_country)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Country not found'
        )
    return {'result' : result}


@router.get("")
async def get_countries(offset: int, limit: int, session: AsyncSession = Depends(get_session)):
    country_service = CountryService(session)
    result = await country_service.read_countries(offset, limit)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Country not found'
        )
    return {'result' : result}


@router.put("/{id_country}")
async def put_country(id_country: UUID, data: CountrySchemaUpdate, session: AsyncSession = Depends(get_session)):
    country_service = CountryService(session)
    result = await country_service.update_country(id_country, data)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Country not found'
        )
    return {'result' : result}

@router.delete("/{id_country}", status_code=status.HTTP_204_NO_CONTENT)
async def del_country(id_country: UUID, session: AsyncSession = Depends(get_session)):
    country_service = CountryService(session)
    result = await country_service.delete_country(id_country)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Country not found'
        )
    return None