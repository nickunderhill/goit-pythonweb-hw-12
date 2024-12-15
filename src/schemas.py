from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class ContactBase(BaseModel):
    name: str = Field(..., max_length=50)
    surname: str = Field(..., max_length=50)
    email: str = Field(..., max_length=50)
    phone: str = Field(..., max_length=15)
    birthday: date
    additional_info: Optional[str] = Field(None, max_length=255)

    model_config = ConfigDict(from_attributes=True)


class ContactCreate(ContactBase):
    pass


class ContactUpdate(ContactBase):
    pass


class ContactResponse(ContactBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class User(BaseModel):
    id: int
    username: str
    email: str
    avatar: str

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
