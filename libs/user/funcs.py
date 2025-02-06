
from django.contrib.auth.models import User

from libs.user.exceptions import UserExceptions


def create_user(
    username: str,
    password: str,
    **kwargs
) -> str:

    user = User.objects.filter(username=username).first()
    if user:
        raise UserExceptions(400, "Username already exists")

    User.objects.create_user(
        username=username,
        password=password,
        is_active=False
    )

    return "Success"