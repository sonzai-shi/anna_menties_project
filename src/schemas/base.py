from fastapi import HTTPException, status


def letter_only_str(value: str) -> str | None:
    if value is None:
        return value
    if not value.replace(' ', '').isalpha():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail='Use only letters.'
        )
    return value


def letter_only_list(value: list[str]) -> list[str] | None:
    if value is None:
        return value
    for genre in value:
        if not genre.replace(' ', '').isalpha():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail='Use only letters.'
            )
    return value


def not_empty_str(value: str) -> str | None:
    if value is None:
        return value
    if not value.replace(' ', ''):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f'The string cannot be empty.'
        )
    return value


def not_empty_list(value: list) -> list | None:
    if value is None:
        return value
    if not value:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f'The list must not be empty.'
        )
    return value



