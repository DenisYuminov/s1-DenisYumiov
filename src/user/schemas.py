from pydantic import BaseModel
from typing import Optional


class ProfileBase(BaseModel):
    username: str
    image: str


class ProfileCreate(ProfileBase):
    image: Optional[str]
    pass


class ProfileUpdate(ProfileBase):
    pass


class Profile(ProfileBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True