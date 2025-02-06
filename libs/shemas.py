from pydantic import BaseModel, Field


class SuccessSchema(BaseModel):
    success: bool = True
    message: str


class UserAuthSchema(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    password: str = Field(min_length=8)