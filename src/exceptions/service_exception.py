from fastapi import HTTPException


class ObjectNotFoundException(HTTPException):
    pass
