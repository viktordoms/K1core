from django.contrib.auth.models import AbstractUser, User
from django.db import models

from K1core.settings import LEN_API_KEY


class UserCredentials(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="credentials")
    api_key = models.CharField(null=False, blank=False, max_length=LEN_API_KEY)
    expired_at = models.DateTimeField(null=False, blank=False)

    class Meta:
        db_table = 'user_credentials'
