from uuid import UUID
from fastapi import APIRouter, status, Depends
from src.service.country_service import CountryService
from src.schemas.country import CountrySchemaCreate, CountrySchemaUpdate
from src.dependencies.country import get_country_write_service, get_country_read_service

router = APIRouter(prefix="/country")


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_country(
        data: CountrySchemaCreate,
        country_service: CountryService = Depends(get_country_write_service),
):
    return await country_service.create_country(data)


@router.get("/{id_country}")
async def read_country(
        id_country: UUID,
        country_service: CountryService = Depends(get_country_read_service),
):
    return await country_service.read_country(id_country)


@router.get("")
async def read_countries(
        offset: int,
        limit: int,
        country_service: CountryService = Depends(get_country_read_service),
):
    return await country_service.read_countries(offset, limit)


@router.put("/{id_country}")
async def update_country(
        id_country: UUID,
        data: CountrySchemaUpdate,
        country_service: CountryService = Depends(get_country_write_service),
):
    return await country_service.update_country(id_country, data)


@router.delete("/{id_country}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_country(
        id_country: UUID,
        country_service: CountryService = Depends(get_country_write_service),
):
    await country_service.delete_country(id_country)
    return None
