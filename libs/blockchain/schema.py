
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
    external_id: t.Optional[str] = Field(None)


class ListOfBlocksSchema(BasicPaginateResponseSchema):
    results: t.List[BlockSchema]


class BlockSpecificSearchSchema(BaseModel):
    currency_name: t.Optional[str] = Field(None)
    block_numbers: t.Optional[int] = Field(None)
    id: t.Optional[int] = Field(None)

