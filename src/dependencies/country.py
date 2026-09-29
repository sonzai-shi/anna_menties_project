from src.service.country_service import CountryService
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_session, get_read_session


def get_country_read_service(session: AsyncSession = Depends(get_read_session)) -> CountryService:
    return CountryService(session)


def get_country_write_service(session: AsyncSession = Depends(get_session)) -> CountryService:
    return CountryService(session)
