from datetime import datetime

from pydantic import BaseModel, Field, PastDatetime


class BasicUserSchema(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    password: str = Field(min_length=8, exclude=True)
    first_name: str = None
    last_name: str = None
    email: str = None
    is_staff: bool = Field(default=False)
    is_active: bool = Field(default=True)
    date_joined: PastDatetime = None
    last_login: PastDatetime = None


