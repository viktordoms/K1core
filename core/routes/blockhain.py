from fastapi import APIRouter, Request

from libs.blockchain.schema import CurrencyListSchema
from libs.blockchain import funcs

blockchain_router = APIRouter(prefix="/api/blockchain")

@blockchain_router.get("/currency", response_model=CurrencyListSchema)
def get_currencies():
    return {
        "result": funcs.get_all_currencies(),
        "success": True,
    }