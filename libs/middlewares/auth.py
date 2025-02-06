
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from django.utils.timezone import now
from django.db import close_old_connections
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async

from K1core.settings import TIME_LIFE_API_KEY
from core.models import UserCredentials
from libs.auth.funcs import generate_api_key

User = get_user_model()

class APIKeyAuthMiddleware(BaseHTTPMiddleware):
    ALLOWED_PATH_WITHOUT_KEY = ("/admin", "/api/auth", "/api/user")

    async def dispatch(self, request: Request, call_next):
        close_old_connections()

        if any(request.url.path.startswith(path) for path in self.ALLOWED_PATH_WITHOUT_KEY):
            return await call_next(request)

        api_key = request.headers.get("API-Key")
        if not api_key:
            return JSONResponse({"error": "API key is required"}, status_code=401)

        credentials = await self.get_credentials(api_key)
        if not credentials:
            return JSONResponse({"error": "Invalid API key"}, status_code=403)

        if credentials.expired_at < now():
            await self.update_api_key(credentials)

        request.state.user = credentials.user
        return await call_next(request)

    @sync_to_async
    def get_credentials(self, api_key):
        try:
            return UserCredentials.objects.select_related("user").get(api_key=api_key)
        except UserCredentials.DoesNotExist:
            return None

    @sync_to_async
    def update_api_key(self, credentials):
        """Оновлюємо термін дії API-ключа"""
        credentials.expired_at = now() + TIME_LIFE_API_KEY
        credentials.api_key = generate_api_key(credentials.api_key)
        credentials.save()
