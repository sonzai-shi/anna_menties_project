from src.models.capitals import CapitalModel
from src.models.countries import CountryModel
from src.schemas.country import(
    CountrySchemaCreate,
    CountrySchemaResponse,
    CountrySchemaUpdate,
    CountrySchemaPagination
)


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


def to_pagination(countries: list[CountryModel], offset, limit) -> CountrySchemaPagination:
    return CountrySchemaPagination(
        items=[CountrySchemaResponse.model_validate(country) for country in countries],
        offset=offset,
        limit=limit,
    )


def update_country(country: CountryModel, data: CountrySchemaUpdate) -> None:
    update_data = data.model_dump(exclude_unset=True)
    capital_data = update_data.pop('capital', None)

    for field, value in update_data.items():
        setattr(country, field, value)

    if capital_data is not None:
        for field, value in capital_data.items():
            setattr(country.capital, field, value)