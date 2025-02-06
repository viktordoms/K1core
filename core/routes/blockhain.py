from fastapi import APIRouter, Request


blockchain_router = APIRouter(prefix="/api/blockchain")

@blockchain_router.post("/", response_model="")
def get(schema):
    return None