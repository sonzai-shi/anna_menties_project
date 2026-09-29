from fastapi import HTTPException


class ObjectNotFoundException(HTTPException):
    pass

class CursorException(HTTPException):
    pass
