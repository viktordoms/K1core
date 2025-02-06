from abc import ABC
import typing as t
import requests
from fastapi import HTTPException
from django.core.cache import cache

from core.models import ExternalCredentials


class RestApiClientException(HTTPException):
    """
    Base exception for REST API client
    """
    pass


class BasicExternalRestApiClient(ABC):
    """
    Basic REST API client for external services.
    Consider using table ExternalCredentials to store credentials.
    The main idea is to store credentials in cache and db to avoid
    unnecessary requests to external services.
    """
    EXPIRED_CACHE_TIMEOUT = 60 * 60 * 24

    def __init__(
        self,
        api_key: t.Optional[str] = None,
        access_token: t.Optional[str] = None,
        test_mode: bool = False,
        base_url: t.Optional[str] = None,
        credentials_code: t.Optional[str] = None,
    ) -> None:

        if not any(
            (
                api_key,
                access_token,
                credentials_code,
            )
        ):
            raise RestApiClientException(
                status_code=400,
                detail="One the following parameters must be specified: `api_key`, `access_token`, `credentials_code`"
            )

        self.api_key = api_key
        self.access_token = access_token
        self.test_mode = test_mode
        self.base_url = base_url
        self.credentials_code = credentials_code
        self.credentials = None

        self.load_from_cache()

        # if credentials are not loaded from memcache, try to load them from db
        if not self.api_key and not self.base_url:
            self.load_credentials_from_db()
            if self.credentials:
                self.api_key = self.credentials.api_key
                self.access_token = self.credentials.access_token
                self.test_mode = self.credentials.test_mode

                if not self.base_url:
                    self.base_url = self.credentials.url

                self.update_cache()

    def load_from_cache(self) -> None:
        """
        Load credentials from cache. Update instance attributes.
        """
        if not self.credentials_code:
            return

        if not self.api_key:
            self.api_key = cache.get(f"{self.credentials_code}_api_key")
        if not self.base_url:
            self.base_url = cache.get(f"{self.credentials_code}_base_url")


    def load_credentials_from_db(self) -> None:
        """
        Load credentials from db. Update instance attribute for easy access and future updates.
        If credentials are not found, do nothing.
        """
        if not self.credentials_code:
            return

        self.credentials = ExternalCredentials.objects.filter(
                code=self.credentials_code
        ).first()

        if self.credentials is None:
            raise RestApiClientException(
                status_code=404,
                detail=f"Credential code ({self.credentials_code}) not found in database."
            )

    def update_cache(self) -> None:
        """
        Update credentials in cache
        """
        if not self.credentials_code:
            return

        if self.api_key:
            cache.set(f"{self.credentials_code}_api_key", self.api_key, self.EXPIRED_CACHE_TIMEOUT)
        if self.access_token:
            cache.set(f"{self.credentials_code}_access_token", self.access_token, self.EXPIRED_CACHE_TIMEOUT)
        if self.base_url:
            cache.set(f"{self.credentials_code}_base_url", self.base_url, self.EXPIRED_CACHE_TIMEOUT)


    def _send_request(
            self,
            method: str,
            endpoint: str,
            params: t.Optional[dict] = None,
            data: t.Optional[dict] = None,
            json: t.Optional[dict] = None,
            headers: t.Optional[dict] = None,
            **kwargs
    ) -> dict[str, t.Any]:

        headers: dict = headers
        url = f"{self.base_url}{endpoint}"

        response = requests.request(
            method,
            url,
            params=params,
            data=data,
            json=json,
            headers=headers,
            **kwargs
        )

        if response.status_code not in [200, 201]:
            data = response.json()
            raise RestApiClientException(
                status_code=response.status_code,
                detail="Fail",
            )

        return response.json()