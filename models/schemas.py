from pydantic import BaseModel
from pydantic import EmailStr
class User(BaseModel):
    """
    User model
    """
    name: str
    email: EmailStr
    location: str
    about: str
    password: str
    class Config:
        orm_mode = True

class LoginData(BaseModel):
    email: EmailStr
    password: str

class RefereshToken(BaseModel):
    refresh_token: str
    class Config:
        orm_mode = True

