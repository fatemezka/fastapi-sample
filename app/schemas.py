from pydantic import BaseModel
from typing import Optional
from app.database import MaritalStatus, Sex


# User
class IRegisterUser(BaseModel):
    username: str
    name: str
    family: str
    phone_number: str
    password: str
    email: Optional[str] = None
    marital_status: Optional[MaritalStatus] = None
    age: Optional[int] = None
    sex: Optional[Sex] = None
    province_id: Optional[int] = None
    city_id: Optional[int] = None
    profile_photo: Optional[str] = None


class ILoginUser(BaseModel):
    phone_number: str
    password: str


class IReturnUserInfo(BaseModel):
    id: int
    username: str
    name: str
    family: str
    phone_number: str
    email: Optional[str] = None
    marital_status: Optional[MaritalStatus] = None
    age: Optional[int] = None
    sex: Optional[Sex] = None
    province_id: Optional[int] = None
    city_id: Optional[int] = None
    profile_photo: Optional[str] = None
