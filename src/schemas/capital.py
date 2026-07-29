from pydantic import BaseModel, Field, field_validator


class CapitalSchemaCreate(BaseModel):
    capital_name: str = Field(min_length=1, max_length=50)
    mayor: str | None = Field(min_length=1, max_length=100)
    population: int = Field(ge=0)

    @field_validator('capital_name', 'mayor')
    @classmethod
    def letter_only(cls, v: str) -> str | None:
        if v is None:
            return v
        if not v.replace(' ', '').replace('-','').isalpha():
            raise ValueError('Используйте только буквы.')
        return v

    @field_validator('capital_name', 'mayor')
    @classmethod
    def not_empty(cls, v: str) -> str | None:
        if v is None:
            return v
        if not v.replace(' ', ''):
            raise ValueError('Строка не может быть пустой.')
        return v