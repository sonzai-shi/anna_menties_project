from src.models.capitals import CapitalModel
from src.models.countries import CountryModel
from src.schemas.country import (
    CountrySchemaCreate,
    CountrySchemaResponse,
    CountrySchemaPagination
)
from datetime import datetime
from uuid import UUID


def to_model(country_data: CountrySchemaCreate) -> CountryModel:
    country = CountryModel(
        name=country_data.name,
        president=country_data.president,
        population=country_data.population,
        currency=country_data.currency
    )
    capital = CapitalModel(
        name=country_data.capital.name,
        mayor=country_data.capital.mayor,
        population=country_data.capital.population,
    )
    country.capital = capital
    return country


def to_pagination(
        countries: list[CountryModel],
        limit: int,
        next_cursor_created_at: datetime | None,
        next_cursor_id: UUID | None,
) -> CountrySchemaPagination:
    return CountrySchemaPagination(
        items=[CountrySchemaResponse.model_validate(country) for country in countries],
        limit=limit,
        next_cursor_created_at=next_cursor_created_at,
        next_cursor_id=next_cursor_id,
    )
