
from fastapi import APIRouter, Request

user_router = APIRouter(prefix="/api/user")

@user_router.post("/")
def registration(request: Request):
    pass