from fastapi import HTTPException

class AuthExceptions(HTTPException):
    """ Base exception for classes related to auth"""

class AuthNotFoundExceptions(AuthExceptions):
     """ Base not found exception for classes related to auth """

class AuthForbiddenExceptions(AuthExceptions):
    """ Base forbidden exception for classes related to auth """