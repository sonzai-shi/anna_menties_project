from uuid import UUID
from fastapi import APIRouter, status, Depends
from src.service.country_service import CountryService
from src.schemas.country import (
    CountrySchemaCreate,
    CountrySchemaUpdate,
    CountrySchemaResponse,
    CountrySchemaPagination
)
from datetime import datetime
from src.dependencies.country import get_country_write_service, get_country_read_service

router = APIRouter(prefix="/country")


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_country(
        data: CountrySchemaCreate,
        country_service: CountryService = Depends(get_country_write_service),
) -> CountrySchemaResponse:
    return await country_service.create_country(data)


@router.get("/{id_country}")
async def read_country(
        id_country: UUID,
        country_service: CountryService = Depends(get_country_read_service),
) -> CountrySchemaResponse:
    return await country_service.read_country(id_country)


@router.get("")
async def read_countries(
        limit: int,
        cursor_created_at: datetime | None = None,
        cursor_id: UUID | None = None,
        country_service: CountryService = Depends(get_country_read_service),
) -> CountrySchemaPagination:
    return await country_service.read_countries(limit, cursor_created_at, cursor_id)


@router.put("/{id_country}")
async def update_country(
        id_country: UUID,
        data: CountrySchemaUpdate,
        country_service: CountryService = Depends(get_country_write_service),
) -> CountrySchemaResponse:
    return await country_service.update_country(id_country, data)


@router.delete("/{id_country}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_country(
        id_country: UUID,
        country_service: CountryService = Depends(get_country_write_service),
) -> None:
    await country_service.delete_country(id_country)
    return None
