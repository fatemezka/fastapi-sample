from pydantic import BaseModel
from typing import Optional
from app.database import MaritalStatus, Sex, LawyerPosition, EducationDegree


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


# class IReturnUserInfo(BaseModel):
#     id: int
#     username: str
#     name: str
#     family: str
#     phone_number: str
#     email: Optional[str] = None
#     marital_status: Optional[MaritalStatus] = None
#     age: Optional[int] = None
#     sex: Optional[Sex] = None
#     province_id: Optional[int] = None
#     city_id: Optional[int] = None
#     profile_photo: Optional[str] = None


# Lawyer
class IRegisterLawyer(BaseModel):
    username: str
    name: str
    family: str
    phone_number: str
    password: str
    age: int
    sex: Sex
    province_id: int
    city_id: int
    edu_degree: EducationDegree
    study_field: str
    license_code: str
    position: LawyerPosition
    experience_years: int
    biography: str
    email: Optional[str] = None
    marital_status: Optional[MaritalStatus] = None
    profile_photo: Optional[str] = None
    office_phone_number: Optional[str] = None
    office_address: Optional[str] = None


class ILogin(BaseModel):
    phone_number: str
    password: str
