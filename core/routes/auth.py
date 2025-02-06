from fastapi import APIRouter, Request

from libs.auth.schema import ApiKeySchema
from libs.auth import funcs
from libs.shemas import UserAuthSchema

auth_router = APIRouter(prefix="/api/auth")

@auth_router.post("/login", response_model=ApiKeySchema)
def login(schema: UserAuthSchema):
    return funcs.login(**schema.model_dump())
