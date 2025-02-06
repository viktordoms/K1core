
import typing as t
from pydantic import BaseModel, Field


class SuccessSchema(BaseModel):
    success: bool = True
    message: str


class UserAuthSchema(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    password: str = Field(min_length=8)


class BasicDicSchema(BaseModel):
    id: int
    code: str
    name: str


class BasicListOfDicSchema(BaseModel):
    result: t.List[BasicDicSchema]
    success: bool


class BasicSearchSchema(BaseModel):
    query: t.Optional[str] = Field(None)


class BasicPaginateRequestSchema(BaseModel):
    page: int = Field(default=1)
    on_page: int = Field(default=10)


class BasicPaginateResponseSchema(BasicPaginateRequestSchema):
    total: int = Field(default=1)