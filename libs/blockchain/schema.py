from datetime import datetime
import typing as t

from pydantic import Field, BaseModel


class CurrencySchema(BaseModel):
    id: int
    code: str
    name: str

class CurrencyListSchema(BaseModel):
    result: t.List[CurrencySchema]
    success: bool