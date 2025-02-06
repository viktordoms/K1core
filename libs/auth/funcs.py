import hashlib
import typing as t
from datetime import datetime

from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password, make_password

from K1core.settings import LEN_API_KEY, TIME_LIFE_API_KEY
from core.models import UserCredentials
from libs.auth.exceptions import AuthNotFoundExceptions, AuthForbiddenExceptions


def login(
    username: str,
    password: str,
    **kwargs
) -> dict[str, t.Any]:

    user = User.objects.filter(username=username).first()
    if not user:
        raise AuthNotFoundExceptions(404,"Not found user with given username")

    if not check_password(password, user.password):
        raise AuthForbiddenExceptions(403, "Invalid password")

    if not user.is_active:
        raise AuthForbiddenExceptions(403, "Account is disabled")

    credentials, is_new = UserCredentials.objects.get_or_create(user=user)

    # if it's first login and not created credentials - hashed api-key by username & password
    # else -> hashed previous api-key
    to_hash = f"{username}:{password}" if is_new else credentials.api_key
    credentials.api_key = generate_api_key(to_hash)

    # update expire of api-key
    credentials.expired_at = datetime.now() + TIME_LIFE_API_KEY
    credentials.save()

    return {
        "api_key": credentials.api_key,
        "expired_at": credentials.expired_at
    }


def generate_api_key(
    to_hash: str,
    **kwargs
) -> str:
    encoded_api_key = to_hash.encode("utf-8")
    return hashlib.sha256(encoded_api_key).hexdigest()[:LEN_API_KEY]
