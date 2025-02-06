"""
ASGI config for K1core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from fastapi import FastAPI


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'K1core.settings')

django_app = get_asgi_application()

fastapi_app = FastAPI()

from core.routes import auth_router, user_router, blockchain_router
fastapi_app.include_router(auth_router)
fastapi_app.include_router(user_router)
fastapi_app.include_router(blockchain_router)

fastapi_app.mount("/", django_app)