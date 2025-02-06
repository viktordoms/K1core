from django.contrib.auth.models import AbstractUser, User
from django.db import models

from K1core.settings import LEN_API_KEY


class UserCredentials(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="credentials")
    api_key = models.CharField(null=False, blank=False, max_length=128)
    expired_at = models.DateTimeField(null=False, blank=False)

    class Meta:
        db_table = "user_credentials"


class ExternalCredentials(models.Model):
    code = models.CharField(null=False, blank=False, max_length=40)
    api_key = models.CharField(null=True, blank=True, max_length=256)
    access_token = models.CharField(null=True, blank=True, max_length=256)
    test_mode = models.BooleanField(default=False)
    base_url = models.URLField(null=False, blank=False)
    provider = models.ForeignKey("Provider", on_delete=models.CASCADE, related_name="credentials", null=True)

    class Meta:
        db_table = "external_credentials"


class Currency(models.Model):
    code = models.CharField(null=False, blank=False, max_length=28)
    name = models.CharField(null=False, blank=False, max_length=128)

    class Meta:
        db_table = "currency"

    def __str__(self):
        return f"{self.name} ({self.code})"


class Provider(models.Model):
    code = models.CharField(null=False, blank=False, max_length=28)
    name = models.CharField(null=False, blank=False, max_length=128)

    class Meta:
        db_table = "provider"

    def __str__(self):
        return f"{self.name} ({self.code})"


class Block(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="blocks")
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name="blocks")
    block_numbers = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(null=False, blank=False)
    stored_at = models.DateTimeField(auto_now_add=True)
    external_id = models.CharField(null=True, blank=True, max_length=256)

    class Meta:
        db_table = "block"

    def __str__(self):
        return f"{self.provider.code} ({self.currency.code}) - {self.block_numbers}"