from fastapi import APIRouter

auth_router = APIRouter(prefix="/api/auth")

@auth_router.get("/login")
def login(request):
    pass