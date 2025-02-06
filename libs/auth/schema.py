from datetime import datetime

from pydantic import Field, BaseModel


class ApiKeySchema(BaseModel):
    api_key: str = Field(min_length=8)
    expired_at: datetime