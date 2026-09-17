from uuid import UUID
from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.service.country_service import CountryService
from src.db import get_session, get_read_session
from src.schemas.country import CountrySchemaCreate, CountrySchemaUpdate

router = APIRouter(prefix="/country")


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_country(data: CountrySchemaCreate, session: AsyncSession = Depends(get_session)):
    country_service = CountryService(session)
    return await country_service.create_country(data)


@router.get("/{id_country}")
async def read_country(id_country: UUID, session: AsyncSession = Depends(get_read_session)):
    country_service = CountryService(session)
    return await country_service.read_country(id_country)


@router.get("")
async def read_countries(offset: int, limit: int, session: AsyncSession = Depends(get_read_session)):
    country_service = CountryService(session)
    return await country_service.read_countries(offset, limit)


@router.put("/{id_country}")
async def update_country(id_country: UUID, data: CountrySchemaUpdate, session: AsyncSession = Depends(get_session)):
    country_service = CountryService(session)
    return await country_service.update_country(id_country, data)


@router.delete("/{id_country}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_country(id_country: UUID, session: AsyncSession = Depends(get_session)):
    country_service = CountryService(session)
    await country_service.delete_country(id_country)
    return None