import uuid
from typing import Optional, Any, List

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    id: Optional[int]
    username: str
    uid: Optional[str]
    nickname: Optional[str] = Field(max_length=20)
    mobile: str
    country: Optional[str]


class UserCreate(UserBase):
    password: Optional[str]
    regist_ip: Optional[str]


class User(UserBase):
    id: int
    avatar: Optional[str]
    bio: Optional[str] = Field(max_length=200)
    login_ip: Optional[str]


class Response(BaseModel):
    code: int
    msg: str
    data: Optional[User | List[User]]
