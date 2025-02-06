
import typing as t

from pydantic import BaseModel, Field

from libs.shemas import (
    BasicDicSchema,
    BasicPaginateResponseSchema,
    BasicSearchSchema,
    BasicPaginateRequestSchema
)


class SearchBlocksSchema(BasicSearchSchema, BasicPaginateRequestSchema):
    provider_id: t.Optional[int] = Field(None)


class BlockSchema(BaseModel):
    id: t.Optional[int] = Field(None)
    currency: BasicDicSchema
    provider: BasicDicSchema
    block_numbers: int
    created_at: str
    stored_at: str


class ListOfBlocksSchema(BasicPaginateResponseSchema):
    results: t.List[BlockSchema]