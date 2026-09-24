from fastapi import HTTPException


class StringContainsNonLettersException(HTTPException):
    pass


class ListContainsNonLettersException(HTTPException):
    pass


class EmptyStringException(HTTPException):
    pass


class EmptyListException(HTTPException):
    pass
