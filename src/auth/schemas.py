from typing import Optional

from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    name: str = Field(title="Name")
    number: str = Field(title="Number")
    password: str = Field(title="Password")

    # class Config:
    #     orm_mode = True


class UserLoginForm(BaseModel):
    username: str = Field(..., title='username', min_length=3, max_length=30)
    password: str = Field(..., title='password')
