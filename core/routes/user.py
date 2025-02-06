
from fastapi import APIRouter, Request

from libs.user.exceptions import UserExceptions
from libs.user import funcs
from libs.shemas import SuccessSchema, UserAuthSchema

user_router = APIRouter(prefix="/api/user")

@user_router.post("/", response_model=SuccessSchema)
def create(schema: UserAuthSchema) -> dict:
    return {
        "message": funcs.create_user(**schema.model_dump()),
        "success": True
    }
