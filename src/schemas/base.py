from fastapi import HTTPException, status
import src.exceptions.schema_exception as se


def letter_only_str(value: str) -> str | None:
    if value is None:
        return value
    if not value.replace(' ', '').isalpha():
        raise se.StringContainsNonLettersException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f'The string: {value} must contain only letters.'
        )
    return value


def letter_only_list(value: list[str]) -> list[str] | None:
    if value is None:
        return value
    for genre in value:
        if not genre.replace(' ', '').isalpha():
            raise se.ListContainsNonLettersException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=f'The genre: {genre} must consist only of letters.'
            )
    return value


def not_empty_str(value: str) -> str | None:
    if value is None:
        return value
    if not value.replace(' ', ''):
        raise se.EmptyStringException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f'The string cannot be empty.'
        )
    return value


def not_empty_list(value: list) -> list | None:
    if value is None:
        return value
    if not value:
        raise se.EmptyListException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f'The list must not be empty.'
        )
    return value
