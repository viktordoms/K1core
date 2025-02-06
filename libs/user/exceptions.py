from fastapi import HTTPException

class UserExceptions(HTTPException):
    """ Base exception for classes related to user """


class UserNotFoundException(UserExceptions):
    """ Base not found exception for classes related to user """
