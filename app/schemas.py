from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None


class UserResponse(UserBase):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True
