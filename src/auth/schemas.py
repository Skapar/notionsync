from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str


class User(BaseModel):
    id: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
