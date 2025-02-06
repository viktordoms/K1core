from fastapi import APIRouter, Request

from libs.blockchain.schema import SearchBlocksSchema, ListOfBlocksSchema, BlockSchema, BlockSpecificSearchSchema
from libs.shemas import BasicListOfDicSchema
from libs.blockchain import funcs

blockchain_router = APIRouter(prefix="/api/blockchain")

@blockchain_router.get("/currency", response_model=BasicListOfDicSchema)
def get_currencies():
    return {
        "result": funcs.get_all_currencies(),
        "success": True,
    }

@blockchain_router.get("/providers", response_model=BasicListOfDicSchema)
def get_currencies():
    return {
        "result": funcs.get_all_providers(),
        "success": True,
    }


@blockchain_router.post("/block/search", response_model=ListOfBlocksSchema)
def search_blocks(schema: SearchBlocksSchema):
    return funcs.search_blocks(**schema.model_dump())


@blockchain_router.post("/block", response_model=BlockSchema)
def search_blocks(schema: BlockSpecificSearchSchema):
    return funcs.search_block(**schema.model_dump())