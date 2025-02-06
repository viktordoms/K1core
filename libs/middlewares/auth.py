
import typing as t

from django.utils.timezone import now
from django.http import JsonResponse
from django.contrib.auth import get_user_model

from K1core.settings import TIME_LIFE_API_KEY
from core.models import UserCredentials
from libs.auth.funcs import generate_api_key

User = get_user_model()

class APIKeyAuthMiddleware:
    ALLOWED_PATH_WITHOUT_KEY = (
        "/admin",
        "/api/auth",
        "/api/user"
    )

    def __init__(self, get_response):
        self.get_response = get_response
        self.credentials: t.Optional[UserCredentials] = None

    def __call__(self, request):
        if any(request.path.startswith(path) for path in self.ALLOWED_PATH_WITHOUT_KEY):
            return self.get_response(request)

        self.load_credentials(request)

        return self.get_response(request)

    def load_credentials(self, request):
        api_key = request.headers.get("API-Key")
        if not api_key:
            return JsonResponse({"error": "API key is required"}, status=401)

        try:
            self.credentials = UserCredentials.objects.select_related("user").get(api_key=api_key)
            if self.credentials.expired_at < now():
                self.credentials.expired_at += TIME_LIFE_API_KEY
                self.hash_key()
                self.credentials.save()

            request.user = self.credentials.user
        except UserCredentials.DoesNotExist:
            return JsonResponse({"error": "Invalid API key"}, status=403)

    def hash_key(self):
        self.credentials.api_key = generate_api_key(self.credentials.api_key)